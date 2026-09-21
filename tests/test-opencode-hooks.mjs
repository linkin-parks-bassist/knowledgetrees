// Mock harness + real shared handler: no agent/model invocation.
import assert from "node:assert/strict";
import { mkdtemp, mkdir, copyFile, rm, writeFile } from "node:fs/promises";
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
  await copyFile(fileURLToPath(new URL("../tools/kt", import.meta.url)), join(process.env.KT_GLOBAL_ROOT, ".tools/kt"));
  process.env.KT_CONFIG = join(temporary, "access-config.json");
  await writeFile(process.env.KT_CONFIG, JSON.stringify({ roots: { global: { path: process.env.KT_GLOBAL_ROOT, access: "allow" } } }));
  await mkdir(join(process.env.KT_GLOBAL_ROOT, "how/to/use"), { recursive: true });
  await copyFile(fileURLToPath(new URL("../example/how/to/use/knowledgetrees.md", import.meta.url)),
    join(process.env.KT_GLOBAL_ROOT, "how/to/use/knowledgetrees.md"));
  await mkdir(join(temporary, ".knowledge/where/am"), { recursive: true });
  await writeFile(join(temporary, ".knowledge/where/am/i.md"), "Project orientation fixture");
  const plugin = await KnowledgeTreesPlugin({ directory: temporary, client: {} });
  assert.equal(plugin["tool.execute.before"], undefined);
  const startup = { system: ["existing harness instructions"] };
  await plugin["experimental.chat.system.transform"]({ sessionID: "one" }, startup);
  assert.equal(startup.system[0], "existing harness instructions");
  assert.match(startup.system[1], /Knowledge-tree startup: `kt info` output follows/);
  assert.match(startup.system[1], /Project orientation fixture/);
  assert.match(startup.system[1], /final proof summary/);
  assert.match(startup.system[1], /global:how\/to\/use\/knowledgetrees.md/);
  await plugin["experimental.chat.system.transform"]({ sessionID: "one" }, startup);
  assert.equal(startup.system.length, 2, "no duplicate bootstrap blocks in assembled context");
  const rebuilt = { system: [] };
  await plugin["experimental.chat.system.transform"]({ sessionID: "two" }, rebuilt);
  assert.equal(rebuilt.system[0], startup.system[1], "fresh requests and sessions retain the procedure");
  const compacted = { context: ["existing compaction context"] };
  await plugin["experimental.session.compacting"]({ sessionID: "one" }, compacted);
  assert.match(compacted.context[1], /initialization state/);
  assert.equal(compacted.context[0], "existing compaction context");
  assert.equal(plugin["chat.message"], undefined);
  assert.equal(plugin["tool.execute.after"], undefined);
  assert.equal(plugin.event, undefined);
  console.log("OpenCode adapter integration checks passed");
} finally {
  await rm(temporary, { recursive: true, force: true });
}
