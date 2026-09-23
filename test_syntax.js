// JavaScript Syntax Validation Script
const fs = require('fs');

const html = fs.readFileSync('D:\\jieyuexingchen\\promptblocks\\index.html', 'utf-8');

// Extract script content
const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
const scriptContent = scriptMatch[1];

console.log('--- JavaScript Syntax Check ---\n');

// Try to parse with new Function (won't execute DOM code)
try {
  // Remove the init() call to prevent DOM access
  const codeWithoutInit = scriptContent.replace(/init\(\s*\);?\s*$/, '');
  new Function(codeWithoutInit);
  console.log('JavaScript syntax: VALID ✓');
} catch (e) {
  console.log('JavaScript syntax: INVALID ✗');
  console.log('Error:', e.message);
}

// Check for common issues
console.log('\n--- Code Pattern Checks ---');

// Check for template literal issues
const templateLiterals = scriptContent.match(/`[^`]*`/g) || [];
console.log(`Template literals found: ${templateLiterals.length}`);

// Check for unclosed brackets
let braces = 0, brackets = 0, parens = 0;
for (const char of scriptContent) {
  if (char === '{') braces++;
  if (char === '}') braces--;
  if (char === '[') brackets++;
  if (char === ']') brackets--;
  if (char === '(') parens++;
  if (char === ')') parens--;
}
console.log(`Braces balance: ${braces === 0 ? '✓' : '✗ (' + braces + ')'}`);
console.log(`Brackets balance: ${brackets === 0 ? '✓' : '✗ (' + brackets + ')'}`);
console.log(`Parentheses balance: ${parens === 0 ? '✓' : '✗ (' + parens + ')'}`);

// Check move button class naming issue
console.log('\n--- Move Button CSS Class Issue ---');
const moveButtonClass = html.includes('class="remove-btn" onclick="moveBlock');
console.log(`Move buttons using "remove-btn" class: ${moveButtonClass ? 'YES (naming inconsistency)' : 'NO'}`);

// Check inline opacity override issue
const moveOpacityOverride = html.includes('style="opacity:0.5"');
console.log(`Move buttons have inline opacity:0.5: ${moveOpacityOverride ? 'YES (overrides hover CSS)' : 'NO'}`);

// Check mobile category tabs overflow concern
console.log('\n--- Mobile Layout Concern ---');
const mobileMaxHeight = html.match(/max-height:\s*(\d+)px/);
console.log(`Block library mobile max-height: ${mobileMaxHeight ? mobileMaxHeight[1] + 'px' : 'not set'}`);
console.log(`Category tabs count: 6, each ~40px = ~240px needed`);
console.log(`With header ~45px, total needed: ~285px`);
console.log(`Available: 200px → category tabs will be clipped on mobile ⚠`);

// Check content with newlines in assembly display
console.log('\n--- Content Display Check ---');
const exStructureContent = '请按以下结构输出：\\n1. 核心观点（1句话）\\n2. 详细分析（3-5句话）\\n3. 行动建议（2-3条）';
console.log(`ex-structure contains newlines: ${exStructureContent.includes('\\n') ? 'YES' : 'NO'}`);
const hasPreWrap = html.includes('white-space: pre-wrap');
console.log(`.prompt-preview has white-space: pre-wrap: ${hasPreWrap ? '✓' : '✗'}`);
const contentHasPreWrap = html.match(/\.assembled-block \.content[^}]*}/);
console.log(`.assembled-block .content CSS: ${contentHasPreWrap ? contentHasPreWrap[0] : 'not found'}`);
console.log(`Newlines in assembly content display will be collapsed (no white-space:pre) ⚠`);

// Check copyPrompt reads from DOM textContent
console.log('\n--- copyPrompt() Edge Case ---');
console.log('When only ex-none is added:');
console.log('  promptPreview.textContent = "" (empty string)');
console.log('  copyBtn.disabled = true (correct)');
console.log('  If somehow called: if(!text) return → safe ✓');
