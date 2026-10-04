"""
P1 three-in-one update:
1. Save Prompt (localStorage history) - save/load/delete
2. Light/Dark mode toggle - CSS variables + toggle button
3. PWA - manifest.json + service worker registration
"""
import re

with open(r'D:\jieyuexingchen\promptblocks\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# ========== P1-2: Light/Dark Mode ==========

# 2a. Add light theme CSS variables after dark theme :root
light_theme = '''
  /* Light Theme */
  [data-theme="light"] {
    --color-role: #4f46e5;
    --color-task: #db2777;
    --color-context: #059669;
    --color-constraints: #d97706;
    --color-format: #7c3aed;
    --color-examples: #0891b2;
    --color-industry: #ea580c;
    --bg-main: #f5f5f8;
    --bg-card: #ffffff;
    --bg-hover: #f0f0f5;
    --text-main: #1a1a2e;
    --text-muted: #6b7280;
    --border: #e0e0e8;
    --warn: #dc2626;
    --warn-bg: rgba(220,38,38,0.08);
    --info: #2563eb;
    --info-bg: rgba(37,99,235,0.08);
  }
  [data-theme="light"] .assembly-empty { background: #f8f8fc; }
  [data-theme="light"] .prompt-preview { background: #f8f8fc; }
  [data-theme="light"] .star-modal-content { background: #fff; }
  [data-theme="light"] .tutorial-card { background: #fff; }
  [data-theme="light"] .platform-btn { background: #f0f0f5; }
  [data-theme="light"] .mode-btn { background: #f0f0f5; }
  [data-theme="light"] input, [data-theme="light"] textarea { background: #f8f8fc; color: #1a1a2e; }
'''

# Find :root closing and add light theme
root_end = '    --info-bg: rgba(59,130,246,0.1);\n  }'
if root_end in content:
    content = content.replace(root_end, root_end + light_theme, 1)
    changes += 1
    print('2a. Light theme CSS added')
else:
    print('2a. root_end not found')

# 2b. Add theme toggle button in header (after langToggle)
old_lang = '<a class="tool-link" id="langToggle" href="javascript:void(0)" onclick="toggleLang()">🌐 EN</a>'
new_lang = '<a class="tool-link" id="langToggle" href="javascript:void(0)" onclick="toggleLang()">🌐 EN</a>\n    <a class="tool-link" id="themeToggle" href="javascript:void(0)" onclick="toggleTheme()" style="font-size:16px">🌙</a>'
if old_lang in content:
    content = content.replace(old_lang, new_lang, 1)
    changes += 1
    print('2b. Theme toggle button added')
else:
    print('2b. langToggle not found')

# 2c. Add theme toggle JS function before </script>
theme_js = '''
// ===== Theme Toggle =====
function applyTheme(theme) {
  if (theme === 'light') {
    document.documentElement.setAttribute('data-theme', 'light');
    var btn = document.getElementById('themeToggle');
    if (btn) btn.textContent = '☀️';
  } else {
    document.documentElement.removeAttribute('data-theme');
    var btn = document.getElementById('themeToggle');
    if (btn) btn.textContent = '🌙';
  }
}
function toggleTheme() {
  var current = document.documentElement.getAttribute('data-theme');
  var next = current === 'light' ? 'dark' : 'light';
  applyTheme(next);
  localStorage.setItem('pb_theme', next);
}
// Load saved theme
(function() {
  var saved = localStorage.getItem('pb_theme');
  if (saved) applyTheme(saved);
})();

'''

# ========== P1-1: Save Prompt (History) ==========

# 1a. Add save button in output-actions (after share button)
old_share_end = '<span data-i18n="share">分享</span>\n      </button>'
new_output = old_share_end + '\n      <button class="btn btn-secondary" id="saveBtn" onclick="savePrompt()" style="padding:10px 14px">\n        <span>💾</span> <span data-i18n="save">保存</span>\n      </button>'
if old_share_end in content:
    content = content.replace(old_share_end, new_output, 1)
    changes += 1
    print('1a. Save button added')
else:
    print('1a. share_end not found')

# 1b. Add history panel HTML (before sponsors div)
history_html = '''
<!-- History Panel -->
<div class="history-panel" id="historyPanel" style="display:none;position:fixed;bottom:0;right:0;width:360px;max-height:60vh;overflow-y:auto;background:var(--bg-card);border:1px solid var(--border);border-radius:12px 0 0 0;padding:16px;z-index:9999;box-shadow:-4px -4px 20px rgba(0,0,0,0.3);">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
    <h3 style="font-size:14px;color:var(--text-main)">📜 <span data-i18n="history">历史记录</span></h3>
    <button onclick="toggleHistory()" style="background:none;border:none;color:var(--text-muted);font-size:18px;cursor:pointer">✕</button>
  </div>
  <div id="historyList"></div>
</div>
<button id="historyToggle" onclick="toggleHistory()" style="position:fixed;bottom:20px;right:20px;width:44px;height:44px;border-radius:50%;background:linear-gradient(135deg,#6366f1,#8b5cf6);border:none;color:#fff;font-size:18px;cursor:pointer;box-shadow:0 4px 12px rgba(99,102,241,0.4);z-index:9998;display:flex;align-items:center;justify-content:center">📜</button>

'''
# Find sponsors div
sponsors_pattern = '<div class="sponsors">'
if sponsors_pattern in content:
    content = content.replace(sponsors_pattern, history_html + sponsors_pattern, 1)
    changes += 1
    print('1b. History panel HTML added')
else:
    print('1b. sponsors not found')

# 1c. Add save/history JS
history_js = '''
// ===== Save Prompt / History =====
function savePrompt() {
  var text = document.getElementById('promptPreview').textContent;
  if (!text || text.trim() === '') { showToast('拼装区为空'); return; }
  var ids = [];
  if (currentMode === 'assembly') {
    assembled.forEach(function(a) { ids.push(a.blockId); });
  }
  var entry = {
    id: Date.now(),
    text: text,
    blocks: ids,
    mode: currentMode,
    time: new Date().toLocaleString('zh-CN')
  };
  var history = JSON.parse(localStorage.getItem('pb_history') || '[]');
  history.unshift(entry);
  if (history.length > 20) history = history.slice(0, 20);
  localStorage.setItem('pb_history', JSON.stringify(history));
  showToast('已保存到历史记录');
  renderHistory();
}

function renderHistory() {
  var el = document.getElementById('historyList');
  if (!el) return;
  var history = JSON.parse(localStorage.getItem('pb_history') || '[]');
  if (history.length === 0) {
    el.innerHTML = '<div style="text-align:center;color:var(--text-muted);padding:20px;font-size:13px">暂无历史记录</div>';
    return;
  }
  el.innerHTML = history.map(function(item, i) {
    var preview = item.text.substring(0, 80) + (item.text.length > 80 ? '...' : '');
    return '<div style="padding:10px;border:1px solid var(--border);border-radius:8px;margin-bottom:8px;cursor:pointer" onclick="loadHistoryItem(' + i + ')" onmouseover="this.style.borderColor=\\'#6366f1\\'" onmouseout="this.style.borderColor=\\'var(--border)\\'">' +
      '<div style="font-size:12px;color:var(--text-muted);margin-bottom:4px">' + item.time + '</div>' +
      '<div style="font-size:12px;color:var(--text-main);line-height:1.5">' + escapeHtml(preview) + '</div>' +
      '<div style="margin-top:6px;display:flex;gap:6px;justify-content:flex-end">' +
      '<button onclick="event.stopPropagation();deleteHistoryItem(' + i + ')" style="font-size:11px;padding:2px 8px;border-radius:4px;border:1px solid var(--border);background:transparent;color:var(--text-muted);cursor:pointer">删除</button>' +
      '</div></div>';
  }).join('');
}

function loadHistoryItem(i) {
  var history = JSON.parse(localStorage.getItem('pb_history') || '[]');
  if (!history[i]) return;
  var item = history[i];
  if (item.mode === 'quick') {
    setMode('quick');
    quickText = item.text;
    var qi = document.getElementById('quickInput');
    if (qi) qi.value = quickText;
    updateQuickScore();
    renderPrompt();
  } else if (item.blocks && item.blocks.length > 0) {
    setMode('assembly');
    assembled = [];
    item.blocks.forEach(function(bid) {
      var found = findBlock(bid);
      if (found) assembled.push({ blockId: bid, categoryId: found.category.id, block: found.block });
    });
    renderAssembly();
    renderPrompt();
  } else {
    // Just load text
    var ta = document.createElement('textarea');
    ta.value = item.text; document.body.appendChild(ta); ta.select();
    document.execCommand('copy');
    document.body.removeChild(ta);
    showToast('已复制到剪贴板');
  }
  toggleHistory(false);
}

function deleteHistoryItem(i) {
  var history = JSON.parse(localStorage.getItem('pb_history') || '[]');
  history.splice(i, 1);
  localStorage.setItem('pb_history', JSON.stringify(history));
  renderHistory();
  showToast('已删除');
}

function toggleHistory(forceShow) {
  var panel = document.getElementById('historyPanel');
  if (!panel) return;
  if (forceShow === false) {
    panel.style.display = 'none';
  } else if (forceShow === true) {
    panel.style.display = 'block';
    renderHistory();
  } else {
    var cur = panel.style.display;
    panel.style.display = cur === 'none' ? 'block' : 'none';
    if (panel.style.display === 'block') renderHistory();
  }
}

'''

# 1d. Add i18n keys for save/history
content = content.replace("share: '分享',", "share: '分享', save: '保存', history: '历史记录',", 1)
content = content.replace("share: 'Share',", "share: 'Share', save: 'Save', history: 'History',", 1)
changes += 2
print('1d. i18n keys added')

# ========== P1-3: PWA ==========

# 3a. Add manifest link in head
manifest_meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
manifest_link = '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<link rel="manifest" href="manifest.json">\n<meta name="theme-color" content="#6366f1">\n<link rel="icon" href="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'><text y=\'.9em\' font-size=\'90\'>🧱</text></svg>">'
if manifest_meta in content:
    content = content.replace(manifest_meta, manifest_link, 1)
    changes += 1
    print('3a. PWA manifest link added')
else:
    print('3a. viewport meta not found')

# 3b. Add service worker registration JS
sw_js = '''
// ===== PWA Service Worker =====
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('sw.js').then(function(reg) {
      console.log('SW registered: ' + reg.scope);
    }).catch(function(err) {
      console.log('SW registration failed: ' + err);
    });
  });
}

'''

# ========== Combine all JS and insert before </script> ==========

# Find the last </script> tag
last_script = '</script>'
# Insert all JS before the last </script>
all_js = theme_js + history_js + sw_js

# Find the last occurrence of </script>
idx = content.rfind(last_script)
if idx != -1:
    content = content[:idx] + all_js + '\n' + content[idx:]
    changes += 1
    print('JS: All functions inserted before </script>')
else:
    print('JS: </script> not found')

# Write back
with open(r'D:\jieyuexingchen\promptblocks\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\nTotal changes: {changes}')
