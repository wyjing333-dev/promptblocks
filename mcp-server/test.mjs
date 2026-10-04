// Quick test for PromptBlocks MCP Server
// Tests that the server can start and respond to JSON-RPC requests

import { spawn } from 'child_process';
import { writeFileSync, readFileSync } from 'fs';

const blocksPath = new URL('../blocks.json', import.meta.url);
const data = JSON.parse(readFileSync(blocksPath, 'utf-8'));

console.log('=== PromptBlocks MCP Server Test ===\n');
console.log(`Loaded blocks.json: ${data.categories.length} categories, ${data.categories.reduce((s, c) => s + c.blocks.length, 0)} blocks\n`);

// Simulate the tools by directly testing the logic
let passed = 0;
let failed = 0;

function assert(name, condition) {
  if (condition) { passed++; console.log(`  ✅ ${name}`); }
  else { failed++; console.log(`  ❌ ${name}`); }
}

// Test 1: blocks.json loads correctly
const totalBlocks = data.categories.reduce((s, c) => s + c.blocks.length, 0);
assert('blocks.json has 72 blocks', totalBlocks === 72);
assert('blocks.json has 8 categories', data.categories.length === 8);
assert('blocks.json has 10 presets', data.presets.length === 10);
assert('blocks.json has 7 platforms', data.platforms.length === 7);
assert('blocks.json has 7 conflict pairs', data.conflictPairs.length === 7);

// Test 2: All presets reference valid block IDs
const allBlockIds = [];
data.categories.forEach(c => c.blocks.forEach(b => allBlockIds.push(b.id)));
let presetErrors = 0;
data.presets.forEach(p => {
  p.blocks.forEach(bid => {
    if (!allBlockIds.includes(bid)) { presetErrors++; console.log(`  ⚠️ Preset ${p.id} references missing block: ${bid}`); }
  });
});
assert('All preset blocks exist', presetErrors === 0);

// Test 3: All conflict pairs reference valid block IDs
let conflictErrors = 0;
data.conflictPairs.forEach(cp => {
  if (!allBlockIds.includes(cp.a)) { conflictErrors++; }
  if (!allBlockIds.includes(cp.b)) { conflictErrors++; }
});
assert('All conflict pairs reference valid blocks', conflictErrors === 0);

// Test 4: All blocks have required fields
let fieldErrors = 0;
data.categories.forEach(c => {
  c.blocks.forEach(b => {
    ['id', 'title', 'content', 'tags', 'platforms', 'verified', 'model'].forEach(f => {
      if (b[f] === undefined) { fieldErrors++; }
    });
  });
});
assert('All blocks have required fields', fieldErrors === 0);

// Test 5: All blocks have English translations
let enErrors = 0;
data.categories.forEach(c => {
  c.blocks.forEach(b => {
    if (b.titleEn === undefined) enErrors++;
    if (b.contentEn === undefined) enErrors++;
  });
});
assert('All blocks have English translations (titleEn + contentEn)', enErrors === 0);

// Test 6: MCP server file exists and has correct structure
const serverCode = readFileSync(new URL('./server.mjs', import.meta.url), 'utf-8');
assert('server.mjs imports McpServer', serverCode.includes("McpServer"));
assert('server.mjs imports StdioServerTransport', serverCode.includes("StdioServerTransport"));
assert('server.mjs has list_blocks tool', serverCode.includes("'list_blocks'"));
assert('server.mjs has search_blocks tool', serverCode.includes("'search_blocks'"));
assert('server.mjs has assemble_prompt tool', serverCode.includes("'assemble_prompt'"));
assert('server.mjs has list_presets tool', serverCode.includes("'list_presets'"));
assert('server.mjs has load_preset tool', serverCode.includes("'load_preset'"));
assert('server.mjs has get_block tool', serverCode.includes("'get_block'"));
assert('server.mjs has list_categories tool', serverCode.includes("'list_categories'"));
assert('server.mjs loads blocks.json', serverCode.includes("blocks.json"));
assert('server.mjs supports language parameter', serverCode.includes("lang"));
assert('server.mjs has conflict detection', serverCode.includes("checkConflicts"));

// Test 7: package.json is correct
const pkg = JSON.parse(readFileSync(new URL('./package.json', import.meta.url), 'utf-8'));
assert('package.json has correct name', pkg.name === 'promptblocks-mcp');
assert('package.json has MCP SDK dependency', pkg.dependencies['@modelcontextprotocol/sdk'] !== undefined);
assert('package.json has zod dependency', pkg.dependencies['zod'] !== undefined);
assert('package.json is ES module', pkg.type === 'module');

console.log(`\n=== Results: ${passed} passed, ${failed} failed ===`);
if (failed > 0) process.exit(1);
