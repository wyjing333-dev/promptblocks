# PromptBlocks MCP Server

Use PromptBlocks block library directly in any MCP-compatible client (Claude Desktop, Cursor, VS Code, etc.).

## Quick Start

### 1. Install dependencies

```bash
cd mcp-server
npm install
```

### 2. Configure your MCP client

#### Claude Desktop

Edit `claude_desktop_config.json`:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "promptblocks": {
      "command": "node",
      "args": ["D:\\path\\to\\promptblocks\\mcp-server\\server.mjs"]
    }
  }
}
```

Restart Claude Desktop. You'll see the PromptBlocks tools available.

#### Cursor

Add to `.cursor/mcp.json` in your project:

```json
{
  "mcpServers": {
    "promptblocks": {
      "command": "node",
      "args": ["/path/to/promptblocks/mcp-server/server.mjs"]
    }
  }
}
```

#### VS Code (with MCP extension)

Add to settings:

```json
{
  "mcp.servers": {
    "promptblocks": {
      "command": "node",
      "args": ["/path/to/promptblocks/mcp-server/server.mjs"]
    }
  }
}
```

### 3. Use it!

In your MCP client, you can now:

- "List all PromptBlocks blocks in the role category"
- "Search for blocks about marketing"
- "Assemble a prompt using role-marketer, task-write-copy, and fmt-list"
- "Load the preset for Xiaohongshu product post"
- "Show me all available categories"

## Available Tools

| Tool | Description |
|------|-------------|
| `list_categories` | List all block categories (role, task, context, etc.) |
| `list_blocks` | List all blocks, optionally filtered by category and platform |
| `search_blocks` | Search blocks by keyword (matches title, content, tags) |
| `get_block` | Get full details of a single block by ID |
| `assemble_prompt` | Assemble a complete Prompt from block IDs |
| `list_presets` | List all preset templates |
| `load_preset` | Load a preset and get the assembled Prompt |

## Parameters

All tools accept an optional `lang` parameter (`"zh"` or `"en"`) to get results in Chinese or English.

## Block IDs

Use `list_categories` and `list_blocks` to discover available block IDs. Common patterns:

- Role blocks: `role-marketer`, `role-programmer`, `role-teacher`, etc.
- Task blocks: `task-write-article`, `task-analyze`, `task-code`, etc.
- Format blocks: `fmt-markdown`, `fmt-table`, `fmt-list`, etc.
- Preset IDs: `preset-xhs`, `preset-code`, `preset-video`, etc.

## Requirements

- Node.js 20+
- blocks.json in the parent directory (included with PromptBlocks)
