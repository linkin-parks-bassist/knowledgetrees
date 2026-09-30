// Thin adapter; the shared Python handler owns kt info rendering and maintenance turns.
import { spawn } from "node:child_process";
import { homedir } from "node:os";
import { join } from "node:path";

const BOOTSTRAP_MARKER = "Knowledge-tree startup:";

export const KnowledgeTreesPlugin = async ({ client, directory }) => {
  const agents = new Map();
  const models = new Map();
  const turns = new Map();
  const handler = join(process.env.KT_GLOBAL_ROOT || join(homedir(), ".knowledge"), ".tools", "kt-hooks");
  const run = (event, payload) => new Promise((resolve) => {
    const child = spawn(process.env.KT_HOOK_PYTHON || "python3", [handler, "opencode", event], {
      cwd: directory, stdio: ["pipe", "pipe", "pipe"],
    });
    let output = "";
    const timer = setTimeout(() => { child.kill(); resolve({}); }, 5000);
    child.stdout.on("data", (chunk) => { output += chunk; });
    child.stderr.on("data", (chunk) => { console.error(String(chunk).trim()); });
    child.on("error", (error) => { clearTimeout(timer); console.error("kt-hooks:", error.message); resolve({}); });
    child.on("close", () => {
      clearTimeout(timer);
      try { resolve(JSON.parse(output)); } catch { resolve({}); }
    });
    child.stdin.on("error", () => {});
    child.stdin.end(JSON.stringify(payload));
  });
  // Both harnesses receive the complete kt info output from the shared handler.
  const startup = await run("start", { source: "startup", cwd: directory });
  const bootstrap = startup.additionalContext;
  return {
    "chat.message": async (input, output) => {
      // Remember the session's agent and model so the maintenance turn runs with them.
      const agent = input.agent || output.message?.agent;
      const model = input.model || output.message?.model;
      if (agent) agents.set(input.sessionID, agent);
      if (model) models.set(input.sessionID, model);
      // A real user message starts a new turn; the synthetic maintenance prompt does not.
      const texts = (output.parts || []).filter((part) => part.type === "text");
      if (!(texts.length > 0 && texts.every((part) => part.synthetic))) turns.set(input.sessionID, []);
    },
    "experimental.chat.system.transform": async (input, output) => {
      // System context is rebuilt per model request. Keep one block in that
      // context, not a new conversation message or a repeated skill invocation.
      if (bootstrap && !output.system.some((text) => text.includes(BOOTSTRAP_MARKER))) {
        output.system.push(bootstrap);
      }
    },
    "experimental.session.compacting": async (_input, output) => {
      output.context.push("Preserve knowledge-tree initialization state: which roots were oriented, " +
        "what evidence was checked, and any unresolved frontier gaps. The harness supplies the kt info output " +
        "in system context after compaction; do not rerun completed startup checks " +
        "merely because a summary was created. Restore genuinely lost context and check changed scope within permissions.");
    },
    event: async ({ event }) => {
      if (event.type === "message.part.updated") {
        // Record each finished call so the handler can tell whether the turn maintained the tree.
        const part = event.properties.part;
        if (part.type === "tool" && ["completed", "error"].includes(part.state?.status)) {
          if (!turns.has(part.sessionID)) turns.set(part.sessionID, []);
          turns.get(part.sessionID).push({ name: part.tool, input: part.state.input ?? "" });
        }
      } else if (event.type === "session.idle") {
        const session = event.properties.sessionID;
        const reminder = await run("stop", { sessionID: session, tools: turns.get(session) ?? [] });
        if (reminder.decision !== "block") return;
        try {
          const result = await client.session.promptAsync({ path: { id: session }, query: { directory },
            body: { ...(agents.has(session) ? { agent: agents.get(session) } : {}),
              ...(models.has(session) ? { model: models.get(session) } : {}),
              parts: [{ type: "text", text: reminder.reason, synthetic: true }] }, throwOnError: true });
          if (result?.error) throw new Error("maintenance reminder could not be delivered");
        } catch (error) { console.error("kt-hooks:", error.message); }
      } else if (event.type === "session.deleted") {
        agents.delete(event.properties.info.id);
        models.delete(event.properties.info.id);
        turns.delete(event.properties.info.id);
      }
    },
  };
};
