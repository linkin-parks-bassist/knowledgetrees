// Mock harness + real shared handler: no agent/model invocation.
import assert from "node:assert/strict";
import { mkdtemp, mkdir, copyFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { KnowledgeTreesPlugin } from "../tools/kt-opencode.mjs";

const temporary = await mkdtemp(join(tmpdir(), "kt-opencode-hooks-"));
try {
  process.env.KT_GLOBAL_ROOT = join(temporary, "global");
  process.env.KT_HOOK_STATE_DIR = join(temporary, "state");
  process.env.KT_HOOK_MIN_CALLS = "3";
  await mkdir(join(process.env.KT_GLOBAL_ROOT, ".tools"), { recursive: true });
  await copyFile(fileURLToPath(new URL("../tools/kt-hooks", import.meta.url)), join(process.env.KT_GLOBAL_ROOT, ".tools/kt-hooks"));
  const prompts = [];
  const plugin = await KnowledgeTreesPlugin({ directory: temporary,
    client: { session: { promptAsync: async (value) => { prompts.push(value); return {}; } } } });
  const model = { providerID: "local", modelID: "test-model" };
  await plugin["chat.message"]({ sessionID: "one", agent: "build", model },
                                { message: { tools: { edit: false } }, parts: [{ type: "text", text: "ordinary task" }] });
  const output = { title: "test", output: "failed command", metadata: { exit: 1 } };
  await plugin["tool.execute.after"]({ sessionID: "one", callID: "a", tool: "bash" }, output);
  assert.match(output.output, /check kt/);
  const terminal = (call, status = "completed") => ({ event: { type: "message.part.updated",
    properties: { part: { type: "tool", sessionID: "one", callID: call, state: { status, metadata: { exit: 0 } } } } } });
  await plugin.event(terminal("a")); // same call must not count twice
  const idle = { event: { type: "session.idle", properties: { sessionID: "one" } } };
  await plugin.event(idle);
  assert.equal(prompts.length, 1);
  assert.equal(prompts[0].body.parts[0].synthetic, true);
  assert.equal(prompts[0].body.agent, "build");
  assert.deepEqual(prompts[0].body.model, model);
  assert.deepEqual(prompts[0].body.tools, { edit: false });
  await plugin["chat.message"]({ sessionID: "one", agent: "build", model }, { parts: prompts[0].body.parts });
  for (const call of ["b", "c", "d", "e"]) await plugin.event(terminal(call));
  await plugin.event(idle);
  assert.equal(prompts.length, 1, "capture review must not recursively wake the agent");
  await plugin["chat.message"]({ sessionID: "one" }, { parts: [
    { type: "text", text: "next external task" }, { type: "text", text: "extra context", synthetic: true }] });
  await plugin.event(terminal("f", "error"));
  const system = { system: [] };
  await plugin["experimental.chat.system.transform"]({ sessionID: "one" }, system);
  assert.match(system.system[0], /check kt/);
  await plugin.event(idle);
  assert.equal(prompts.length, 2);
  await plugin.event({ event: { type: "session.idle", properties: { sessionID: "other" } } });
  assert.equal(prompts.length, 2);
  console.log("OpenCode adapter integration checks passed");
} finally {
  await rm(temporary, { recursive: true, force: true });
}
