// Thin startup adapter; the shared Python handler owns kt info rendering.
import { spawn } from "node:child_process";
import { homedir } from "node:os";
import { join } from "node:path";

const BOOTSTRAP_MARKER = "Knowledge-tree startup:";

export const KnowledgeTreesPlugin = async ({ client, directory }) => {
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
    "experimental.chat.system.transform": async (input, output) => {
      // System context is rebuilt per model request. Keep one block in that
      // context, not a new conversation message or a repeated skill invocation.
      if (bootstrap && !output.system.some((text) => text.includes(BOOTSTRAP_MARKER))) {
        output.system.push(bootstrap);
      }
    },
    "experimental.session.compacting": async (_input, output) => {
      output.context.push("Preserve knowledge-tree initialization state: which roots were oriented, " +
        "what evidence was checked, and outstanding misses/captures. The harness supplies the kt info output " +
        "in system context after compaction; do not rerun completed startup checks " +
        "merely because a summary was created. Restore genuinely lost context and check changed scope within permissions.");
    },
  };
};
