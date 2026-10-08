# -*- coding: utf-8 -*-
"""给PromptBlocks添加基于访问次数的Star引导弹窗"""

filepath = 'D:/jieyuexingchen/promptblocks/index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# ═══ 修改1: 在弹窗HTML加"不再提醒"按钮 ═══
old_html = """      <button class="star-later" onclick="closeStarModal()" data-i18n="later">下次再说</button>
    </div>
  </div>
</div>"""

new_html = """      <button class="star-later" onclick="closeStarModal()" data-i18n="later">下次再说</button>
      <button class="star-never" onclick="neverShowStarModal()" data-i18n="neverShow">不再提醒</button>
    </div>
  </div>
</div>"""

content = content.replace(old_html, new_html)
print("1. HTML: added 'neverShow' button")

# ═══ 修改2: 在CSS加 .star-never 样式 ═══
old_css = "  .star-modal-content .star-later:hover { border-color: var(--text-muted); color: var(--text-main); }"

new_css = """  .star-modal-content .star-later:hover { border-color: var(--text-muted); color: var(--text-main); }
  .star-modal-content .star-never {
    padding: 6px 16px; border-radius: 20px; border: none;
    background: transparent; color: var(--text-muted); font-size: 12px; cursor: pointer;
    transition: all 0.2s; opacity: 0.6; margin-top: 4px;
  }
  .star-modal-content .star-never:hover { opacity: 1; color: var(--text-muted); }"""

content = content.replace(old_css, new_css)
print("2. CSS: added .star-never style")

# ═══ 修改3: 替换JS逻辑——加访问次数追踪+自动弹窗 ═══
old_js = """var starShownCount = 0;
function showStarModal() {
  starShownCount++;
  if (starShownCount > 3) return;
  var modal = document.getElementById('starModal');
  if (modal) modal.classList.add('show');
}

function closeStarModal() {
  var modal = document.getElementById('starModal');
  if (modal) modal.classList.remove('show');
}"""

new_js = """var starShownCount = 0;
// 访问次数追踪 + 自动弹Star引导
(function() {
  var visits = parseInt(localStorage.getItem('pb_visit_count') || '0') + 1;
  localStorage.setItem('pb_visit_count', visits);
  var starDismissed = localStorage.getItem('pb_star_dismissed') === '1';
  // 第3次访问起，且未永久关闭，3秒后自动弹窗
  if (visits >= 3 && !starDismissed) {
    setTimeout(function() {
      var modal = document.getElementById('starModal');
      if (modal && !modal.classList.contains('show')) {
        modal.classList.add('show');
      }
    }, 3000);
  }
})();

function showStarModal() {
  starShownCount++;
  if (starShownCount > 3) return;
  var modal = document.getElementById('starModal');
  if (modal) modal.classList.add('show');
}

function closeStarModal() {
  var modal = document.getElementById('starModal');
  if (modal) modal.classList.remove('show');
}

function neverShowStarModal() {
  localStorage.setItem('pb_star_dismissed', '1');
  var modal = document.getElementById('starModal');
  if (modal) modal.classList.remove('show');
}"""

content = content.replace(old_js, new_js)
print("3. JS: added visit tracking + auto-show + neverShowStarModal")

# ═══ 修改4: i18n加 neverShow 翻译 ═══
# 中文
content = content.replace('"later": "下次再说"', '"later": "下次再说",\n    "neverShow": "不再提醒"')
# 英文
content = content.replace('"later": "Maybe later"', '"later": "Maybe later",\n    "neverShow": "Don\'t show again"')
print("4. i18n: added neverShow translations")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nDone! index.html updated successfully.")
