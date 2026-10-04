import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load blocks.json from parent directory
const blocksPath = join(__dirname, '..', 'blocks.json');
const data = JSON.parse(readFileSync(blocksPath, 'utf-8'));

const CATEGORIES = data.categories;
const PRESETS = data.presets;
const PLATFORMS = data.platforms;
const CONFLICT_PAIRS = data.conflictPairs;
const SOLO_CATEGORIES = data.soloCategories || ['format', 'examples'];

// Create MCP server
const server = new McpServer({
  name: 'promptblocks',
  version: '1.0.0',
});

// Helper: find block by ID across all categories
function findBlock(blockId) {
  for (const cat of CATEGORIES) {
    const block = cat.blocks.find(b => b.id === blockId);
    if (block) return { block, category: cat };
  }
  return null;
}

// Helper: check conflicts between selected block IDs
function checkConflicts(blockIds) {
  const conflicts = [];
  const ids = blockIds;
  for (const cp of CONFLICT_PAIRS) {
    if (ids.includes(cp.a) && ids.includes(cp.b)) {
      conflicts.push({ a: cp.a, b: cp.b, reason: cp.reason });
    }
  }
  // Check solo categories
  for (const catId of SOLO_CATEGORIES) {
    const cat = CATEGORIES.find(c => c.id === catId);
    if (!cat) continue;
    const selectedInCat = ids.filter(id => cat.blocks.some(b => b.id === id));
    if (selectedInCat.length > 1) {
      conflicts.push({
        a: selectedInCat[0],
        b: selectedInCat[1],
        reason: catId === 'format' ? 'Format conflict: pick only one output format' : 'Example conflict: pick only one example type'
      });
    }
  }
  return conflicts;
}

// ===== Tool 1: list_blocks =====
// List all blocks, optionally filtered by category
server.tool(
  'list_blocks',
  'List all PromptBlocks blocks, optionally filtered by category. Returns block id, title, content preview, tags, and platforms.',
  {
    category: z.string().optional().describe('Category ID to filter: role, task, context, constraints, format, examples, industry, decision'),
    platform: z.string().optional().describe('Platform ID to filter: all, chatgpt, claude, stepfun, gemini, wenxin, tongyi'),
    lang: z.string().optional().default('zh').describe('Language: zh or en')
  },
  async ({ category, platform, lang }) => {
    let cats = category ? CATEGORIES.filter(c => c.id === category) : CATEGORIES;
    const results = [];
    for (const cat of cats) {
      let blocks = cat.blocks;
      if (platform) {
        blocks = blocks.filter(b => b.platforms.includes('all') || b.platforms.includes(platform));
      }
      for (const b of blocks) {
        const title = lang === 'en' ? (b.titleEn || b.title) : b.title;
        const content = lang === 'en' ? (b.contentEn || b.content) : b.content;
        const catName = lang === 'en' ? (cat.nameEn || cat.name) : cat.name;
        results.push({
          id: b.id,
          title: title,
          category: catName,
          categoryId: cat.id,
          contentPreview: content.substring(0, 100) + (content.length > 100 ? '...' : ''),
          tags: b.tags,
          platforms: b.platforms,
          verified: b.verified,
          model: b.model
        });
      }
    }
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({ total: results.length, blocks: results }, null, 2)
      }]
    };
  }
);

// ===== Tool 2: search_blocks =====
// Search blocks by keyword (matches title, content, tags)
server.tool(
  'search_blocks',
  'Search PromptBlocks by keyword. Matches block title, content, and tags. Returns matching blocks with full content.',
  {
    keyword: z.string().describe('Search keyword (matches title, content, tags)'),
    lang: z.string().optional().default('zh').describe('Language: zh or en')
  },
  async ({ keyword, lang }) => {
    const kw = keyword.toLowerCase();
    const results = [];
    for (const cat of CATEGORIES) {
      for (const b of cat.blocks) {
        const title = lang === 'en' ? (b.titleEn || b.title) : b.title;
        const content = lang === 'en' ? (b.contentEn || b.content) : b.content;
        const catName = lang === 'en' ? (cat.nameEn || cat.name) : cat.name;
        const matchTitle = title.toLowerCase().includes(kw);
        const matchContent = content.toLowerCase().includes(kw);
        const matchTags = b.tags.some(t => t.toLowerCase().includes(kw));
        if (matchTitle || matchContent || matchTags) {
          results.push({
            id: b.id,
            title: title,
            category: catName,
            categoryId: cat.id,
            content: content,
            tags: b.tags,
            platforms: b.platforms,
            matchedBy: [matchTitle ? 'title' : null, matchContent ? 'content' : null, matchTags ? 'tags' : null].filter(Boolean)
          });
        }
      }
    }
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({ keyword, total: results.length, results }, null, 2)
      }]
    };
  }
);

// ===== Tool 3: assemble_prompt =====
// Assemble a complete prompt from block IDs
server.tool(
  'assemble_prompt',
  'Assemble a complete Prompt from block IDs. Blocks are concatenated in order. Returns the assembled prompt text. Also checks for conflicts.',
  {
    block_ids: z.array(z.string()).describe('Array of block IDs to assemble (e.g. ["role-marketer", "task-write-copy", "fmt-list"])'),
    lang: z.string().optional().default('zh').describe('Language: zh or en'),
    include_meta: z.boolean().optional().default(false).describe('If true, include block metadata (category, title) as comments')
  },
  async ({ block_ids, lang, include_meta }) => {
    const parts = [];
    const missing = [];
    const usedBlocks = [];
    for (const bid of block_ids) {
      const found = findBlock(bid);
      if (!found) {
        missing.push(bid);
        continue;
      }
      const { block, category } = found;
      const title = lang === 'en' ? (block.titleEn || block.title) : block.title;
      const content = lang === 'en' ? (block.contentEn || block.content) : block.content;
      const catName = lang === 'en' ? (category.nameEn || category.name) : category.name;
      usedBlocks.push({ id: bid, title, category: catName });
      if (content && content.trim()) {
        if (include_meta) {
          parts.push(`# ${catName} > ${title}\n${content}`);
        } else {
          parts.push(content);
        }
      }
    }
    const conflicts = checkConflicts(block_ids);
    const prompt = parts.join('\n\n');
    const result = {
      prompt: prompt,
      blockCount: usedBlocks.length,
      missingBlocks: missing.length > 0 ? missing : undefined,
      conflicts: conflicts.length > 0 ? conflicts : undefined,
      blocks: usedBlocks
    };
    return {
      content: [{
        type: 'text',
        text: JSON.stringify(result, null, 2)
      }]
    };
  }
);

// ===== Tool 4: list_presets =====
// List all preset templates
server.tool(
  'list_presets',
  'List all preset templates. Each preset is a pre-configured combination of blocks for a specific use case.',
  {
    lang: z.string().optional().default('zh').describe('Language: zh or en')
  },
  async ({ lang }) => {
    const results = PRESETS.map(p => {
      const name = lang === 'en' ? (p.nameEn || p.name) : p.name;
      const blocks = p.blocks.map(bid => {
        const found = findBlock(bid);
        if (!found) return { id: bid, title: '(missing)', category: '' };
        const title = lang === 'en' ? (found.block.titleEn || found.block.title) : found.block.title;
        const catName = lang === 'en' ? (found.category.nameEn || found.category.name) : found.category.name;
        return { id: bid, title, category: catName };
      });
      return { id: p.id, name, blockCount: blocks.length, blocks };
    });
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({ total: results.length, presets: results }, null, 2)
      }]
    };
  }
);

// ===== Tool 5: load_preset =====
// Load a preset and generate the assembled prompt
server.tool(
  'load_preset',
  'Load a preset template by ID and get the assembled Prompt. Returns the full prompt text ready to use.',
  {
    preset_id: z.string().describe('Preset ID (e.g. "preset-xhs", "preset-code", "preset-video")'),
    lang: z.string().optional().default('zh').describe('Language: zh or en')
  },
  async ({ preset_id, lang }) => {
    const preset = PRESETS.find(p => p.id === preset_id);
    if (!preset) {
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({ error: `Preset not found: ${preset_id}`, available: PRESETS.map(p => p.id) }, null, 2)
        }]
      };
    }
    const parts = [];
    const blockInfo = [];
    for (const bid of preset.blocks) {
      const found = findBlock(bid);
      if (!found) continue;
      const content = lang === 'en' ? (found.block.contentEn || found.block.content) : found.block.content;
      const title = lang === 'en' ? (found.block.titleEn || found.block.title) : found.block.title;
      const catName = lang === 'en' ? (found.category.nameEn || found.category.name) : found.category.name;
      blockInfo.push({ id: bid, title, category: catName });
      if (content && content.trim()) {
        parts.push(content);
      }
    }
    const conflicts = checkConflicts(preset.blocks);
    const presetName = lang === 'en' ? (preset.nameEn || preset.name) : preset.name;
    const prompt = parts.join('\n\n');
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          presetId: preset_id,
          presetName: presetName,
          prompt: prompt,
          blockCount: blockInfo.length,
          conflicts: conflicts.length > 0 ? conflicts : undefined,
          blocks: blockInfo
        }, null, 2)
      }]
    };
  }
);

// ===== Tool 6: get_block =====
// Get full details of a single block
server.tool(
  'get_block',
  'Get full details of a single block by ID. Returns title, full content, tags, platforms, and verification info.',
  {
    block_id: z.string().describe('Block ID (e.g. "role-marketer", "task-write-article")'),
    lang: z.string().optional().default('zh').describe('Language: zh or en')
  },
  async ({ block_id, lang }) => {
    const found = findBlock(block_id);
    if (!found) {
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({ error: `Block not found: ${block_id}` }, null, 2)
        }]
      };
    }
    const { block, category } = found;
    const title = lang === 'en' ? (block.titleEn || block.title) : block.title;
    const content = lang === 'en' ? (block.contentEn || block.content) : block.content;
    const catName = lang === 'en' ? (category.nameEn || category.name) : category.name;
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          id: block.id,
          title: title,
          content: content,
          category: catName,
          categoryId: category.id,
          tags: block.tags,
          platforms: block.platforms,
          verified: block.verified,
          model: block.model
        }, null, 2)
      }]
    };
  }
);

// ===== Tool 7: list_categories =====
// List all categories with block counts
server.tool(
  'list_categories',
  'List all block categories with descriptions and block counts.',
  {
    lang: z.string().optional().default('zh').describe('Language: zh or en')
  },
  async ({ lang }) => {
    const results = CATEGORIES.map(c => ({
      id: c.id,
      name: lang === 'en' ? (c.nameEn || c.name) : c.name,
      icon: c.icon,
      blockCount: c.blocks.length,
      blockIds: c.blocks.map(b => b.id)
    }));
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({ total: results.length, categories: results }, null, 2)
      }]
    };
  }
);

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
console.error('PromptBlocks MCP Server running on stdio');
