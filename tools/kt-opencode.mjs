// Thin harness adapter; the shared Python handler owns reminders and counters.
import { spawn } from "node:child_process";
import { homedir } from "node:os";
import { join } from "node:path";

const BOOTSTRAP_MARKER = "Knowledge-tree startup:";
const FILTERED_KT_BOOT = /(?:^|[;&\n])\s*kt\s+(?:boot|init)\b[^\n;]*?\s+\|(?!\|)/m;

export const KnowledgeTreesPlugin = async ({ client, directory }) => {
  const pending = new Map();
  const agents = new Map();
  const models = new Map();
  const toolsets = new Map();
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
  // Both harnesses receive the complete kt boot output from the shared handler.
  const startup = await run("start", { source: "startup", cwd: directory });
  const bootstrap = startup.additionalContext;
  const remember = (session, result) => {
    if (result.additionalContext) pending.set(session, result.additionalContext);
  };
  return {
    "tool.execute.before": async (input, output) => {
      const command = output.args?.command;
      if (input.tool !== "bash" || typeof command !== "string") return;
      if (FILTERED_KT_BOOT.test(command)) {
        throw new Error("Read kt boot/init output directly and completely; retry without the pipe.");
      }
    },
    "chat.message": async (input, output) => {
      const agent = input.agent || output.message?.agent;
      const model = input.model || output.message?.model;
      if (agent) agents.set(input.sessionID, agent);
      if (model) models.set(input.sessionID, model);
      if (output.message?.tools) toolsets.set(input.sessionID, output.message.tools);
      const texts = output.parts.filter((p) => p.type === "text");
      await run("prompt", { sessionID: input.sessionID,
        prompt: texts.map((p) => p.text).join("\n"),
        synthetic: texts.length > 0 && texts.every((p) => p.synthetic) });
    },
    "tool.execute.after": async (input, output) => {
      const result = await run("after", { sessionID: input.sessionID, callID: input.callID,
        toolName: input.tool, result: { metadata: output.metadata, output: output.output } });
      if (result.additionalContext) output.output += "\n\n" + result.additionalContext;
    },
    "experimental.chat.system.transform": async (input, output) => {
      // System context is rebuilt per model request. Keep one block in that
      // context, not a new conversation message or a repeated skill invocation.
      if (bootstrap && !output.system.some((text) => text.includes(BOOTSTRAP_MARKER))) {
        output.system.push(bootstrap);
      }
      if (pending.has(input.sessionID)) {
        output.system.push(pending.get(input.sessionID));
        pending.delete(input.sessionID);
      }
    },
    "experimental.session.compacting": async (_input, output) => {
      output.context.push("Preserve knowledge-tree initialization state: which roots were oriented, " +
        "what evidence was checked, and outstanding misses/captures. The harness supplies the kt boot output " +
        "in system context after compaction; do not rerun completed startup checks " +
        "merely because a summary was created. Restore genuinely lost context and check changed scope within permissions.");
    },
    event: async ({ event }) => {
      if (event.type === "message.part.updated") {
        const part = event.properties.part;
        if (part.type === "tool" && ["completed", "error"].includes(part.state.status)) {
          const result = await run(part.state.status === "error" ? "failed" : "after", {
            sessionID: part.sessionID, callID: part.callID,
            result: { status: part.state.status, metadata: part.state.metadata, output: part.state.output },
          });
          remember(part.sessionID, result);
        }
      } else if (event.type === "session.idle") {
        const session = event.properties.sessionID;
        const review = await run("stop", { sessionID: session });
        if (review.decision === "block") {
          try {
            const result = await client.session.promptAsync({ path: { id: session }, query: { directory },
              body: { ...(agents.has(session) ? { agent: agents.get(session) } : {}),
                ...(models.has(session) ? { model: models.get(session) } : {}),
                ...(toolsets.has(session) ? { tools: toolsets.get(session) } : {}),
                parts: [{ type: "text", text: review.reason, synthetic: true }] }, throwOnError: true });
            if (result.error) throw new Error("capture review could not be delivered");
          } catch (error) { console.error("kt-hooks:", error.message); }
        }
      } else if (event.type === "session.deleted") {
        pending.delete(event.properties.info.id);
        agents.delete(event.properties.info.id);
        models.delete(event.properties.info.id);
        toolsets.delete(event.properties.info.id);
      }
    },
  };
};
