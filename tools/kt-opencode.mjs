// Thin harness adapter; the shared Python handler owns reminders and counters.
import { spawn } from "node:child_process";
import { homedir } from "node:os";
import { join } from "node:path";
import { readFile } from "node:fs/promises";

const BOOTSTRAP_MARKER = "Knowledge-tree harness bootstrap (already loaded)";

export const KnowledgeTreesPlugin = async ({ client, directory }) => {
  const pending = new Map();
  const agents = new Map();
  const models = new Map();
  const toolsets = new Map();
  const handler = join(process.env.KT_GLOBAL_ROOT || join(homedir(), ".knowledge"), ".tools", "kt-hooks");
  let bootstrap;
  try {
    const source = await readFile(join(process.env.KT_GLOBAL_ROOT || join(homedir(), ".knowledge"),
      "how/to/use/knowledgetrees.md"), "utf8");
    const body = source.replace(/^---\r?\n[\s\S]*?\r?\n---(?:\r?\n|$)/, "").trim();
    if (!body || Buffer.byteLength(source) > 65536) throw new Error("empty or oversized bootstrap procedure");
    bootstrap = `${BOOTSTRAP_MARKER}\n` +
      "The harness has loaded the canonical knowledge-tree procedure below. Do not invoke the bootstrap skill to load it again. " +
      "Before substantive work in a fresh session, perform its root discovery, evidence checks, and orientation. " +
      "Do not repeat completed startup work on ordinary turns or task boundaries. After compaction, retain completed initialization " +
      "and checked knowledge; restore only genuinely lost context or changed scope. Focused skills still apply when triggered. " +
      "Current higher-authority instructions and permissions govern; this context grants no access or execution authority.\n\n" + body;
  } catch (error) {
    console.error("kt-hooks: bootstrap procedure unavailable:", error.code || error.message);
  }
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
  const remember = (session, result) => {
    if (result.additionalContext) pending.set(session, result.additionalContext);
  };
  return {
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
        "what evidence was checked, and outstanding misses/captures. The harness supplies the canonical procedure " +
        "in system context after compaction; do not reinvoke the bootstrap skill or rerun completed startup checks " +
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
