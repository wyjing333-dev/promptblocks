"""
Add share link feature to index.html:
1. Add share button in output-actions area
2. Add loadFromURL() function to parse ?blocks=id1,id2
3. Add shareLink() function to generate share URL and copy to clipboard
4. Call loadFromURL() in init()
"""
import re

with open(r'D:\jieyuexingchen\promptblocks\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add share button next to copy button
old_output = '''      <button class="btn btn-secondary" onclick="resetAll()" style="padding:10px 14px" data-i18n="reset">重置</button>
    </div>'''

new_output = '''      <button class="btn btn-secondary" onclick="resetAll()" style="padding:10px 14px" data-i18n="reset">重置</button>
      <button class="btn btn-secondary" id="shareBtn" onclick="shareLink()" style="padding:10px 14px">
        <span>🔗</span> <span data-i18n="share">分享</span>
      </button>
    </div>'''

if old_output in content:
    content = content.replace(old_output, new_output, 1)
    print('1. Share button added')
else:
    print('1. Share button: target not found, trying regex...')
    # Try to find the reset button
    pattern = r'(<button class="btn btn-secondary" onclick="resetAll\(\)".*?data-i18n="reset">重置</button>)\s*(</div>)'
    match = re.search(pattern, content)
    if match:
        content = content[:match.start()] + new_output + content[match.end():]
        print('1. Share button added via regex')
    else:
        print('1. FAILED to add share button')

# 2. Add loadFromURL, shareLink functions and modify init()
# Find init() call at the end
old_init_end = '''init();
</script>'''

new_init_end = '''// ===== Share Link Feature =====
function loadFromURL() {
  var params = new URLSearchParams(window.location.search);
  var blockIds = params.get('blocks');
  var presetId = params.get('preset');
  var fixBlock = params.get('fix');
  var quick = params.get('quick');

  // If quick mode requested
  if (quick === '1') {
    setMode('quick');
  }

  // If preset specified
  if (presetId) {
    loadPreset(presetId);
    return;
  }

  // If blocks specified
  if (blockIds) {
    var ids = blockIds.split(',').filter(function(id) { return id.trim(); });
    assembled = [];
    ids.forEach(function(bid) {
      var found = findBlock(bid.trim());
      if (found) {
        assembled.push({ blockId: bid.trim(), categoryId: found.category.id, block: found.block });
      }
    });
    if (assembled.length > 0) {
      renderAssembly();
      renderPrompt();
    }
  }

  // If fix block specified (from scorer)
  if (fixBlock) {
    var found = findBlock(fixBlock.trim());
    if (found) {
      if (currentMode === 'quick') {
        setMode('assembly');
      }
      var existing = assembled.find(function(a) { return a.blockId === fixBlock.trim(); });
      if (!existing) {
        assembled.push({ blockId: fixBlock.trim(), categoryId: found.category.id, block: found.block });
        renderAssembly();
        renderPrompt();
      }
      // Scroll to assembly area
      setTimeout(function() {
        var panel = document.getElementById('assemblyPanel');
        if (panel) panel.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }, 300);
    }
  }
}

function shareLink() {
  var ids = [];
  if (currentMode === 'quick') {
    // For quick mode, share the text
    var text = quickText || '';
    if (!text) { showToast('拼装区为空，请先添加积木'); return; }
    var base = window.location.origin + window.location.pathname;
    var url = base + '?quick=1&text=' + encodeURIComponent(text.substring(0, 500));
    navigator.clipboard.writeText(url).then(function() {
      showToast('分享链接已复制！');
    }).catch(function() {
      var ta = document.createElement('textarea');
      ta.value = url; document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); showToast('分享链接已复制！'); } catch(e) { showToast('复制失败'); }
      document.body.removeChild(ta);
    });
    return;
  }
  if (assembled.length === 0) { showToast('拼装区为空，请先添加积木'); return; }
  assembled.forEach(function(a) { ids.push(a.blockId); });
  var base = window.location.origin + window.location.pathname;
  var url = base + '?blocks=' + ids.join(',');
  navigator.clipboard.writeText(url).then(function() {
    showToast('分享链接已复制！');
  }).catch(function() {
    var ta = document.createElement('textarea');
    ta.value = url; document.body.appendChild(ta); ta.select();
    try { document.execCommand('copy'); showToast('分享链接已复制！'); } catch(e) { showToast('复制失败'); }
    document.body.removeChild(ta);
  });
}

// Initialize - load data first, then init, then check URL params
function fullInit() {
  init();
  loadFromURL();
}

// Override the init call
loadData(fullInit);
</script>'''

if old_init_end in content:
    content = content.replace(old_init_end, new_init_end, 1)
    print('2. Share functions + loadFromURL added')
else:
    print('2. Target not found - trying to find init() call...')
    # Search for the pattern
    pattern = r'init\(\);\s*</script>'
    match = re.search(pattern, content)
    if match:
        content = content[:match.start()] + new_init_end + content[match.end():]
        print('2. Share functions added via regex')
    else:
        print('2. FAILED - could not find init() call')

# 3. Also need to handle the loadData(init) call that exists earlier
old_load_init = 'loadData(init);'
new_load_init = '// loadData(fullInit) is called at the end of the script'

if old_load_init in content:
    content = content.replace(old_load_init, new_load_init, 1)
    print('3. Replaced earlier loadData(init) call')
else:
    print('3. loadData(init) not found separately (may be handled by regex above)')

# 4. Add i18n keys for share
if '"share"' not in content.split('I18N')[1].split(';')[0] if 'I18N' in content else '':
    # Add to zh dict
    content = content.replace(
        "copyPrompt: '复制Prompt',",
        "copyPrompt: '复制Prompt', share: '分享',"
    )
    content = content.replace(
        "copyPrompt: 'Copy Prompt',",
        "copyPrompt: 'Copy Prompt', share: 'Share',"
    )
    print('4. i18n keys for share added')
else:
    print('4. i18n keys already exist')

with open(r'D:\jieyuexingchen\promptblocks\index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('\nDone!')
