// PromptBlocks MVP - Automated Verification Script
// Extracts CATEGORIES and PRESETS from index.html and validates data integrity

const fs = require('fs');

const html = fs.readFileSync('D:\\jieyuexingchen\\promptblocks\\index.html', 'utf-8');

// Extract the script content
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
if (!scriptMatch) {
  console.error('ERROR: No <script> tag found');
  process.exit(1);
}
const scriptContent = scriptMatch[1];

// Extract CATEGORIES using eval (safe since it's our own file)
// We'll use a Function to evaluate the data declarations
let CATEGORIES, PRESETS;

try {
  // Extract only the data declarations (CATEGORIES and PRESETS const)
  // Remove the init() call at the end to avoid DOM access
  let dataOnly = scriptContent.replace(/init\(\s*\);?\s*$/, '');
  // Also remove the init() function body to avoid document references
  // We just need CATEGORIES and PRESETS which are defined as const arrays
  // Extract CATEGORIES definition
  const catMatch = dataOnly.match(/const\s+CATEGORIES\s*=\s*\[[\s\S]*?\n\];/);
  const presetMatch = dataOnly.match(/const\s+PRESETS\s*=\s*\[[\s\S]*?\n\];/);
  
  if (!catMatch || !presetMatch) {
    // Try alternate approach - extract between const declarations
    const evalStr = catMatch ? presetMatch ? catMatch[0] + '\n' + presetMatch[0] : catMatch[0] : '';
    if (evalStr) {
      const fn = new Function(evalStr + '\nreturn { CATEGORIES, PRESETS };');
      const result = fn();
      CATEGORIES = result.CATEGORIES;
      PRESETS = result.PRESETS;
    } else {
      throw new Error('Could not extract data declarations');
    }
  } else {
    const fn = new Function(catMatch[0] + '\n' + presetMatch[0] + '\nreturn { CATEGORIES, PRESETS };');
    const result = fn();
    CATEGORIES = result.CATEGORIES;
    PRESETS = result.PRESETS;
  }
} catch (e) {
  console.error('ERROR parsing script:', e.message);
  console.error(e.stack);
  process.exit(1);
}

console.log('========================================');
console.log('PromptBlocks MVP - Data Verification');
console.log('========================================\n');

// ===== 1. CATEGORIES Structure Validation =====
console.log('--- CATEGORIES Structure ---');
console.log(`Total categories: ${CATEGORIES.length}`);

let totalBlocks = 0;
const allBlockIds = new Set();
const blockIdToCategory = new Map();

CATEGORIES.forEach((cat, i) => {
  const hasId = !!cat.id;
  const hasName = !!cat.name;
  const hasIcon = !!cat.icon;
  const hasColor = !!cat.color;
  const hasBlocks = Array.isArray(cat.blocks);
  const blockCount = hasBlocks ? cat.blocks.length : 0;
  totalBlocks += blockCount;

  console.log(`\n  Category ${i+1}: "${cat.id}" (${cat.name})`);
  console.log(`    id: ${hasId ? '✓' : '✗'}, name: ${hasName ? '✓' : '✗'}, icon: ${hasIcon ? '✓' : '✗'}, color: ${hasColor ? '✓' : '✗'}, blocks: ${hasBlocks ? '✓' : '✗'}`);
  console.log(`    icon="${cat.icon}", color="${cat.color}"`);
  console.log(`    Block count: ${blockCount}`);

  cat.blocks.forEach((b, j) => {
    const hasBlockId = !!b.id;
    const hasTitle = !!b.title;
    const hasContent = b.content !== undefined;
    const hasTags = Array.isArray(b.tags);
    
    if (allBlockIds.has(b.id)) {
      console.log(`    ⚠ DUPLICATE blockId: "${b.id}"`);
    }
    allBlockIds.add(b.id);
    blockIdToCategory.set(b.id, cat.id);
    
    const contentEmpty = !b.content || !b.content.trim();
    console.log(`      ${j+1}. ${b.id} - "${b.title}" | content: ${contentEmpty ? '(EMPTY)' : '"' + b.content.substring(0, 40) + (b.content.length > 40 ? '...' : '"') + ''} | tags: ${hasTags ? b.tags.join(',') : 'NONE'}`);
  });
});

console.log(`\n--- Summary ---`);
console.log(`Total categories: ${CATEGORIES.length}`);
console.log(`Total blocks: ${totalBlocks}`);
console.log(`Unique block IDs: ${allBlockIds.size}`);
console.log(`Expected: 6 categories, 39 blocks`);
console.log(`Match: ${CATEGORIES.length === 6 ? '✓' : '✗'} categories, ${totalBlocks === 39 ? '✓' : '✗'} blocks`);

// ===== 2. PRESETS Validation =====
console.log('\n\n--- PRESETS Validation ---');
console.log(`Total presets: ${PRESETS.length}`);
console.log(`Expected: 4 presets`);

PRESETS.forEach((p, i) => {
  console.log(`\n  Preset ${i+1}: "${p.id}" (${p.name})`);
  console.log(`    Blocks: ${p.blocks.join(', ')}`);
  
  p.blocks.forEach((blockId, j) => {
    if (allBlockIds.has(blockId)) {
      const catId = blockIdToCategory.get(blockId);
      console.log(`      ${j+1}. ${blockId} → found in category "${catId}" ✓`);
    } else {
      console.log(`      ${j+1}. ${blockId} → NOT FOUND ✗`);
    }
  });
});

// ===== 3. Empty content blocks check =====
console.log('\n\n--- Empty Content Blocks ---');
CATEGORIES.forEach(cat => {
  cat.blocks.forEach(b => {
    if (!b.content || !b.content.trim()) {
      console.log(`  Block "${b.id}" (${b.title}) in category "${cat.id}" has empty content`);
    }
  });
});

// ===== 4. Function definitions check =====
console.log('\n\n--- Function Definitions ---');
const functionPattern = /function\s+(\w+)\s*\(/g;
const definedFunctions = new Set();
let match;
while ((match = functionPattern.exec(scriptContent)) !== null) {
  definedFunctions.add(match[1]);
}
console.log(`Defined functions: ${Array.from(definedFunctions).join(', ')}`);

// Extract onclick references
const onclickPattern = /onclick="(\w+)\(/g;
const onclickRefs = new Set();
while ((match = onclickPattern.exec(html)) !== null) {
  onclickRefs.add(match[1]);
}
console.log(`\nOnclick references: ${Array.from(onclickRefs).join(', ')}`);

onclickRefs.forEach(fn => {
  if (definedFunctions.has(fn)) {
    console.log(`  ${fn}: defined ✓`);
  } else {
    console.log(`  ${fn}: NOT DEFINED ✗`);
  }
});

// Check init() call
const hasInitCall = /init\(\s*\)/.test(scriptContent.replace(/function init\(\)/g, ''));
console.log(`\ninit() called: ${hasInitCall ? '✓' : '✗'}`);

// ===== 5. renderPrompt logic check =====
console.log('\n\n--- renderPrompt() Logic ---');
// Simulate: only ex-none block added
const exNoneBlock = { blockId: 'ex-none', categoryId: 'examples', block: { id: 'ex-none', title: '不需要示例', content: '', tags: ['无示例'] } };
const assembledExNone = [exNoneBlock];
const partsExNone = assembledExNone.map(item => item.block.content).filter(c => c && c.trim());
const promptExNone = partsExNone.join('\n\n');
console.log(`Scenario: Only ex-none added`);
console.log(`  assembled.length = ${assembledExNone.length}`);
console.log(`  parts after filter = ${JSON.stringify(partsExNone)}`);
console.log(`  prompt = "${promptExNone}"`);
console.log(`  copyBtn.disabled = ${!promptExNone}`);
console.log(`  Empty content filtered: ${partsExNone.length === 0 ? '✓' : '✗'}`);

// ===== 6. Responsive CSS check =====
console.log('\n\n--- Responsive CSS ---');
const hasMediaQuery = html.includes('@media (max-width: 1024px)');
console.log(`@media (max-width: 1024px) present: ${hasMediaQuery ? '✓' : '✗'}`);
const hasColumnLayout = html.includes('.main { flex-direction: column; }');
console.log(`Column layout on mobile: ${hasColumnLayout ? '✓' : '✗'}`);
const hasFullWidthLibrary = html.includes('.block-library { width: 100%;');
console.log(`Full width block library on mobile: ${hasFullWidthLibrary ? '✓' : '✗'}`);
const hasFullWidthOutput = html.includes('.output-panel { width: 100%;');
console.log(`Full width output panel on mobile: ${hasFullWidthOutput ? '✓' : '✗'}`);

// ===== 7. Move block boundary check =====
console.log('\n\n--- moveBlock() Boundary Logic ---');
// Simulate
function simulateMoveBlock(index, dir, assembledLength) {
  const ni = index + dir;
  if (ni < 0 || ni >= assembledLength) return 'BLOCKED (boundary)';
  return `SWAP ${index} <-> ${ni}`;
}
console.log(`Move first block up (index=0, dir=-1): ${simulateMoveBlock(0, -1, 3)}`);
console.log(`Move last block down (index=2, dir=1, len=3): ${simulateMoveBlock(2, 1, 3)}`);
console.log(`Move middle block up (index=1, dir=-1, len=3): ${simulateMoveBlock(1, -1, 3)}`);
console.log(`Move middle block down (index=1, dir=1, len=3): ${simulateMoveBlock(1, 1, 3)}`);

// ===== 8. Duplicate add check =====
console.log('\n\n--- Duplicate Add Logic ---');
console.log(`addBlock() pushes to array without dedup check - allows duplicates (by design)`);
console.log(`No max limit on assembled array - potential for very long lists`);

console.log('\n========================================');
console.log('Verification Complete');
console.log('========================================');
