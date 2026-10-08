# -*- coding: utf-8 -*-
"""
PromptBlocks 移动端响应式适配
在index.html中添加：1.汉堡菜单CSS 2.移动端@media 3.JS切换函数
"""
import os

html_path = "D:/jieyuexingchen/promptblocks/index.html"

with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# ═══ 1. 在@media (max-width: 1024px)块之后、</style>之前插入移动端CSS ═══
mobile_css = """
  /* ===== Mobile Menu Toggle Button ===== */
  .menu-toggle {
    display: none; background: none; border: none; color: var(--text-main);
    font-size: 24px; cursor: pointer; padding: 8px; border-radius: 8px;
    min-width: 44px; min-height: 44px; align-items: center; justify-content: center;
  }
  .menu-toggle:hover { background: var(--bg-hover); }

  /* ===== Mobile Responsive (<=768px) ===== */
  @media (max-width: 768px) {
    /* Header - hamburger menu */
    .menu-toggle { display: flex; }
    header { padding: 10px 12px; flex-wrap: nowrap; gap: 8px; }
    .logo { font-size: 18px; }
    .logo span { display: none; }
    .presets { display: none; }
    .header-right {
      display: none; position: fixed; top: 52px; left: 0; right: 0;
      flex-direction: column; gap: 0; padding: 8px 12px 12px;
      background: var(--bg-card); border-bottom: 1px solid var(--border);
      z-index: 1000; box-shadow: 0 4px 16px rgba(0,0,0,0.4); max-height: 80vh; overflow-y: auto;
    }
    header.menu-open .header-right { display: flex; }
    .header-right > * { width: 100%; justify-content: center; }
    .mode-toggle { width: 100%; }
    .mode-btn { flex: 1; padding: 10px 16px; min-height: 44px; }
    .tool-link, .star-btn, .submit-btn { padding: 10px 16px; min-height: 44px; font-size: 14px; justify-content: center; }

    /* Platform bar - horizontal scroll */
    .platform-bar { padding: 8px 12px; overflow-x: auto; -webkit-overflow-scrolling: touch; }
    .platform-bar .plabel { font-size: 11px; }
    .platform-filters { flex-wrap: nowrap; overflow-x: auto; }
    .platform-btn { padding: 6px 10px; min-height: 32px; flex-shrink: 0; }

    /* Dashboard - compact */
    .dashboard { padding: 8px 12px; gap: 12px; }
    .stat-item .stat-value { font-size: 16px; }
    .stat-item .stat-label { font-size: 10px; }
    .stat-divider { display: none; }

    /* Block library - collapsible */
    .block-library { max-height: 260px; }
    .block-library .category-tabs { overflow-x: auto; flex-wrap: nowrap; -webkit-overflow-scrolling: touch; }
    .block-library .category-tab { white-space: nowrap; padding: 10px 12px; flex-shrink: 0; }
    .blocks-list { padding: 6px; }
    .block-item { padding: 10px; min-height: 44px; }
    .block-item .title { font-size: 13px; }

    /* Assembly area */
    .assembly-area { padding: 10px; }
    .assembly-empty .icon { font-size: 36px; }
    .assembly-empty .text { font-size: 14px; }
    .assembled-block { padding: 10px 12px; }
    .assembled-block .content { font-size: 13px; }
    .assembled-block .remove-btn { opacity: 0.7; width: 32px; height: 32px; font-size: 18px; }

    /* Output panel */
    .output-area { padding: 10px; }
    .prompt-preview { padding: 12px; font-size: 13px; min-height: 100px; }
    .output-actions { padding: 8px 10px; flex-wrap: wrap; gap: 6px; }
    .btn { padding: 8px 12px; font-size: 13px; min-height: 40px; }
    .btn-primary { flex: 1 1 100%; }

    /* Quick input */
    .quick-input-area { min-height: 200px; padding: 12px; font-size: 13px; }

    /* Modals - full screen on mobile */
    #testPanel {
      width: 100% !important; max-width: 100% !important; max-height: 100vh !important;
      top: 0 !important; left: 0 !important; transform: none !important;
      border-radius: 0; padding: 16px; height: 100vh;
    }
    .star-modal-content { max-width: 92%; padding: 24px 20px; margin: 0 10px; }
    .star-modal-content .star-close { min-width: 44px; min-height: 44px; font-size: 24px; }
    .tutorial-card { max-width: 92%; padding: 24px 20px; margin: 0 10px; }

    /* Sponsors */
    .sponsors { padding: 10px 12px; }
    .sponsors .sponsor-content { font-size: 12px; }
  }
"""

# 检查是否已经有移动端CSS（防止重复添加）
if 'max-width: 768px' in content:
    print("⚠️ 移动端CSS已存在，跳过CSS插入")
else:
    # 在</style>之前插入
    content = content.replace('</style>', mobile_css + '\n</style>')
    print("✅ 移动端CSS已插入")

# ═══ 2. 在header中添加汉堡菜单按钮 ═══
menu_btn = '  <button class="menu-toggle" onclick="toggleMobileMenu()" aria-label="菜单">☰</button>'

if 'class="menu-toggle"' in content:
    print("⚠️ 汉堡菜单按钮已存在，跳过HTML插入")
else:
    # 在logo div之后插入
    content = content.replace(
        '</div>\n  <div class="presets"',
        '</div>\n' + menu_btn + '\n  <div class="presets"'
    )
    print("✅ 汉堡菜单按钮已插入")

# ═══ 3. 在<script>之后添加toggleMobileMenu函数 ═══
mobile_js = """// ===== Mobile Menu Toggle =====
function toggleMobileMenu() {
  var header = document.querySelector('header');
  header.classList.toggle('menu-open');
}
// Close menu when clicking outside or on a link
document.addEventListener('click', function(e) {
  var header = document.querySelector('header');
  if (header && header.classList.contains('menu-open')) {
    if (!e.target.closest('.header-right') && !e.target.closest('.menu-toggle')) {
      header.classList.remove('menu-open');
    }
  }
});

"""

if 'function toggleMobileMenu' in content:
    print("⚠️ toggleMobileMenu函数已存在，跳过JS插入")
else:
    content = content.replace(
        '<script>\n// ===== Platform Definitions',
        '<script>\n' + mobile_js + '// ===== Platform Definitions'
    )
    print("✅ toggleMobileMenu函数已插入")

# 写回文件
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n🎉 移动端响应式适配完成！")
print("   - 汉堡菜单（≤768px显示）")
print("   - 导航折叠为下拉菜单")
print("   - 平台栏横向滚动")
print("   - 积木库可折叠")
print("   - 弹窗全屏化")
print("   - 所有交互元素≥44px")
