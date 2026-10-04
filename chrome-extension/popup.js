// PromptBlocks Chrome Extension - Popup Logic
var BLOCKS = [];
var CATEGORIES = [];
var selected = [];
var activeCat = 'all';

function init() {
  // Load blocks data
  BLOCKS = window.PB_BLOCKS || [];
  CATEGORIES = window.PB_CATEGORIES || [];
  
  document.getElementById('blockCount').textContent = BLOCKS.length;
  
  // Render category tabs
  var catTabs = document.getElementById('catTabs');
  var tabsHtml = '<button class="cat-tab active" onclick="setCat(\'all\')">全部</button>';
  CATEGORIES.forEach(function(c) {
    tabsHtml += '<button class="cat-tab" onclick="setCat(\'' + c.id + '\')">' + c.icon + ' ' + c.name + '</button>';
  });
  catTabs.innerHTML = tabsHtml;
  
  renderBlocks();
  
  // Search
  document.getElementById('searchInput').addEventListener('input', function() {
    renderBlocks();
  });
}

function setCat(catId) {
  activeCat = catId;
  var tabs = document.querySelectorAll('.cat-tab');
  tabs.forEach(function(t) { t.classList.remove('active'); });
  event.target.classList.add('active');
  renderBlocks();
}

function renderBlocks() {
  var query = document.getElementById('searchInput').value.toLowerCase();
  var list = document.getElementById('blockList');
  var filtered = BLOCKS.filter(function(b) {
    var matchCat = activeCat === 'all' || b.categoryId === activeCat;
    var matchSearch = !query || b.title.toLowerCase().indexOf(query) >= 0 || b.content.toLowerCase().indexOf(query) >= 0;
    return matchCat && matchSearch;
  });
  
  if (filtered.length === 0) {
    list.innerHTML = '<div style="text-align:center;padding:20px;color:#8888a0;font-size:12px">无匹配积木</div>';
    return;
  }
  
  list.innerHTML = filtered.map(function(b) {
    var cat = CATEGORIES.find(function(c) { return c.id === b.categoryId; });
    var catName = cat ? cat.icon + ' ' + cat.name : '';
    return '<div class="block-item" onclick="addBlock(\'' + b.id + '\')">' +
      '<div class="block-title">' + b.title + '</div>' +
      '<div class="block-cat">' + catName + '</div>' +
    '</div>';
  }).join('');
}

function addBlock(blockId) {
  var block = BLOCKS.find(function(b) { return b.id === blockId; });
  if (!block) return;
  selected.push(block);
  renderAssembled();
}

function removeBlock(index) {
  selected.splice(index, 1);
  renderAssembled();
}

function renderAssembled() {
  var area = document.getElementById('assembledArea');
  var count = document.getElementById('selectedCount');
  count.textContent = selected.length;
  
  if (selected.length === 0) {
    area.innerHTML = '<span style="font-size:11px;color:#8888a0">从上方选择积木添加到拼装区</span>';
    document.getElementById('preview').textContent = '';
    return;
  }
  
  area.innerHTML = selected.map(function(b, i) {
    return '<span class="assembled-chip">' + b.title + ' <span class="remove" onclick="removeBlock(' + i + ')">✕</span></span>';
  }).join('');
  
  // Generate preview
  var text = selected.map(function(b) { return b.content; }).join('\n\n');
  document.getElementById('preview').textContent = text;
}

function copyPrompt() {
  if (selected.length === 0) return;
  var text = selected.map(function(b) { return b.content; }).join('\n\n');
  navigator.clipboard.writeText(text).then(function() {
    var btn = document.getElementById('copyBtn');
    var orig = btn.textContent;
    btn.textContent = '已复制!';
    setTimeout(function() { btn.textContent = orig; }, 1500);
  });
}

function insertToPage() {
  if (selected.length === 0) return;
  var text = selected.map(function(b) { return b.content; }).join('\n\n');
  
  // Send to content script
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    chrome.tabs.sendMessage(tabs[0].id, { action: 'insertPrompt', text: text }, function(response) {
      if (response && response.success) {
        var btn = document.getElementById('insertBtn');
        var orig = btn.textContent;
        btn.textContent = '已插入!';
        setTimeout(function() { btn.textContent = orig; }, 1500);
      } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(text).then(function() {
          var btn = document.getElementById('insertBtn');
          var orig = btn.textContent;
          btn.textContent = '已复制(插入失败)';
          setTimeout(function() { btn.textContent = orig; }, 2000);
        });
      }
    });
  });
}

function clearAll() {
  selected = [];
  renderAssembled();
}

init();
