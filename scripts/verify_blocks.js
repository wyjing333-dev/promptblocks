// PromptBlocks 积木回归测试脚本
// 用法: node scripts/verify_blocks.js
// 检测每个积木的内容完整性、结构合法性、常见Prompt反模式

const fs = require('fs');
const path = require('path');

// 读取 index.html 并提取 CATEGORIES 数据
function loadBlocks() {
  const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf-8');
  // 提取 CATEGORIES 到 PRESETS 之间的 JS 代码
  const match = html.match(/var CATEGORIES = \[([\s\S]*?)\];\s*\n\s*var PRESETS/);
  if (!match) {
    console.error('[ERROR] 无法从 index.html 提取 CATEGORIES 数据');
    process.exit(1);
  }
  // 用 eval 解析（本地脚本，安全可控）
  const CATEGORIES = eval('[' + match[1] + ']');
  return CATEGORIES;
}

function runTests() {
  const CATEGORIES = loadBlocks();
  let totalBlocks = 0;
  let totalErrors = 0;
  let totalWarnings = 0;
  const errors = [];
  const warnings = [];

  console.log('═══════════════════════════════════════════');
  console.log('  PromptBlocks 积木回归测试');
  console.log('  测试日期: ' + new Date().toISOString().split('T')[0]);
  console.log('═══════════════════════════════════════════\n');

  CATEGORIES.forEach(function(cat) {
    console.log('📁 ' + cat.icon + ' ' + cat.name + ' (' + cat.blocks.length + ' 个积木)');
    console.log('   ────────────────────────────────');

    cat.blocks.forEach(function(b) {
      totalBlocks++;
      var blockErrors = [];
      var blockWarnings = [];

      // 1. 必填字段检查
      var requiredFields = ['id', 'title', 'content', 'tags', 'platforms', 'verified', 'model'];
      requiredFields.forEach(function(f) {
        if (b[f] === undefined || b[f] === null) {
          blockErrors.push('缺少必填字段: ' + f);
        }
      });

      // 2. ID 唯一性（跨分类检查在后面）
      if (!b.id || typeof b.id !== 'string') {
        blockErrors.push('ID 无效');
      }

      // 3. 内容检查（ex-none 允许空内容）
      if (b.id !== 'ex-none' && (!b.content || b.content.trim().length < 10)) {
        blockWarnings.push('内容过短（<10字符）: "' + (b.content || '') + '"');
      }

      // 4. platforms 合法性
      var validPlatforms = ['all', 'chatgpt', 'claude', 'stepfun', 'gemini', 'wenxin', 'tongyi'];
      if (b.platforms && Array.isArray(b.platforms)) {
        b.platforms.forEach(function(p) {
          if (validPlatforms.indexOf(p) === -1) {
            blockErrors.push('未知平台标识: ' + p);
          }
        });
      } else {
        blockErrors.push('platforms 不是数组');
      }

      // 5. verified 日期格式
      if (b.verified && !/^\d{4}-\d{2}-\d{2}$/.test(b.verified)) {
        blockWarnings.push('verified 日期格式不规范: ' + b.verified);
      }

      // 6. 模型版本检查
      if (b.model && b.model.indexOf('GPT-4o') === -1 && b.model.indexOf('Claude') === -1 && b.model.indexOf('Step') === -1) {
        blockWarnings.push('model 字段可能未包含主流模型: ' + b.model);
      }

      // 7. Prompt 反模式检测
      if (b.content) {
        // 检查是否有过于模糊的指令
        if (/帮我看看|帮我弄一下|随便写写/.test(b.content)) {
          blockWarnings.push('指令过于模糊（"帮我看看"等）');
        }
        // 检查是否有矛盾指令
        if (/不要.*要.*同时|禁止.*允许/.test(b.content)) {
          blockWarnings.push('可能存在矛盾指令');
        }
        // 检查中文标点混用
        if (/[。；，]/.test(b.content) && /[.;,]/.test(b.content) && !/JSON|Markdown|API|Python|JavaScript|React/.test(b.content)) {
          blockWarnings.push('中英文标点混用');
        }
      }

      // 8. tags 检查
      if (!b.tags || !Array.isArray(b.tags) || b.tags.length === 0) {
        blockWarnings.push('没有标签');
      }

      // 输出结果
      var status = blockErrors.length > 0 ? '❌' : blockWarnings.length > 0 ? '⚠️' : '✅';
      var detail = b.title + ' (' + b.id + ')';
      if (blockErrors.length > 0) {
        detail += ' → 错误: ' + blockErrors.join('; ');
        blockErrors.forEach(function() { totalErrors++; });
        errors.push({ id: b.id, errors: blockErrors });
      }
      if (blockWarnings.length > 0) {
        detail += ' → 警告: ' + blockWarnings.join('; ');
        blockWarnings.forEach(function() { totalWarnings++; });
        warnings.push({ id: b.id, warnings: blockWarnings });
      }
      console.log('   ' + status + ' ' + detail);
    });
    console.log('');
  });

  // 9. ID 全局唯一性检查
  var allIds = [];
  CATEGORIES.forEach(function(cat) {
    cat.blocks.forEach(function(b) { allIds.push(b.id); });
  });
  var dupIds = allIds.filter(function(id, i) { return allIds.indexOf(id) !== i; });
  if (dupIds.length > 0) {
    console.log('❌ 发现重复 ID: ' + dupIds.join(', '));
    totalErrors += dupIds.length;
  }

  // 10. 冲突规则检查（CONFLICT_PAIRS 引用积木是否存在）
  var html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf-8');
  var conflictMatch = html.match(/var CONFLICT_PAIRS = \[([\s\S]*?)\];/);
  if (conflictMatch) {
    var conflictPairs = eval('[' + conflictMatch[1] + ']');
    conflictPairs.forEach(function(cp) {
      if (allIds.indexOf(cp.a) === -1) {
        console.log('❌ 冲突规则引用了不存在的积木: ' + cp.a);
        totalErrors++;
      }
      if (allIds.indexOf(cp.b) === -1) {
        console.log('❌ 冲突规则引用了不存在的积木: ' + cp.b);
        totalErrors++;
      }
    });
  }

  // 11. 预设模板引用积木检查
  var presetMatch = html.match(/var PRESETS = \[([\s\S]*?)\];/);
  if (presetMatch) {
    var presets = eval('[' + presetMatch[1] + ']');
    presets.forEach(function(p) {
      p.blocks.forEach(function(bid) {
        if (allIds.indexOf(bid) === -1) {
          console.log('❌ 预设模板 "' + p.name + '" 引用了不存在的积木: ' + bid);
          totalErrors++;
        }
      });
    });
  }

  // 12. 验证日期过期检查（超过90天未验证）
  var today = new Date();
  CATEGORIES.forEach(function(cat) {
    cat.blocks.forEach(function(b) {
      if (b.verified) {
        var verifiedDate = new Date(b.verified);
        var daysDiff = Math.floor((today - verifiedDate) / (1000 * 60 * 60 * 24));
        if (daysDiff > 90) {
          console.log('⚠️ ' + b.id + ' 已 ' + daysDiff + ' 天未验证，可能因模型更新失效');
          totalWarnings++;
        }
      }
    });
  });

  // 汇总
  console.log('═══════════════════════════════════════════');
  console.log('  测试汇总');
  console.log('═══════════════════════════════════════════');
  console.log('  总积木数: ' + totalBlocks);
  console.log('  分类数: ' + CATEGORIES.length);
  console.log('  错误数: ' + totalErrors);
  console.log('  警告数: ' + totalWarnings);
  console.log('  结果: ' + (totalErrors === 0 ? '✅ 全部通过' : '❌ 有错误需修复'));
  console.log('═══════════════════════════════════════════');

  if (totalErrors > 0) process.exit(1);
}

runTests();
