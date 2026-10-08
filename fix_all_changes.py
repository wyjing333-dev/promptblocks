# -*- coding: utf-8 -*-
"""Fix all missing changes in index.html - comprehensive patch"""

with open('D:/jieyuexingchen/promptblocks/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

changes = 0

# 1. Add role-btn CSS after platform-btn.active
if 'role-btn' not in content:
    old_css = '.platform-btn.active { background: rgba(99,102,241,0.15); border-color: #6366f1; color: #a5b4fc; font-weight: 600; }'
    new_css = old_css + """
  /* Role Filter Bar */
  .role-bar {
    padding: 8px 24px; background: var(--bg-card); border-bottom: 1px solid var(--border);
    display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
  }
  .role-bar .rlabel { font-size: 12px; color: var(--text-muted); margin-right: 4px; white-space: nowrap; }
  .role-filters { display: flex; gap: 6px; flex-wrap: wrap; }
  .role-btn {
    padding: 4px 12px; border-radius: 16px; border: 1px solid var(--border);
    background: transparent; color: var(--text-muted); font-size: 12px;
    cursor: pointer; transition: all 0.2s; white-space: nowrap;
  }
  .role-btn:hover { border-color: #ec4899; color: #f9a8d4; }
  .role-btn.active { background: rgba(236,72,153,0.15); border-color: #ec4899; color: #f9a8d4; font-weight: 600; }"""
    if old_css in content:
        content = content.replace(old_css, new_css, 1)
        changes += 1
        print('✅ Added role-btn CSS')
    else:
        print('❌ Cannot find platform-btn.active CSS')

# 2. Add ROLES array and activeRole variable
if 'ROLES' not in content:
    old_data = "var activePlatform = 'all';\nvar assembled = [];"
    if old_data in content:
        new_data = """var activePlatform = 'all';
var activeRole = 'all';
var assembled = [];

// Role definitions
var ROLES = [
  { id: 'all', name: '全部角色', nameEn: 'All Roles', icon: '\\u{1f465}' },
  { id: 'pm', name: '产品经理', nameEn: 'PM', icon: '\\u{1f4cb}' },
  { id: 'researcher', name: '调研员', nameEn: 'Researcher', icon: '\\u{1f50d}' },
  { id: 'developer', name: '程序员', nameEn: 'Developer', icon: '\\u{1f4bb}' },
  { id: 'tester', name: '测试员', nameEn: 'Tester', icon: '\\u{1f9ea}' },
  { id: 'designer', name: '设计师', nameEn: 'Designer', icon: '\\u{1f3a8}' },
  { id: 'marketer', name: '运营官', nameEn: 'Marketer', icon: '\\u{1f4e3}' },
  { id: 'general', name: '通用', nameEn: 'General', icon: '\\u{1f527}' }
];"""
        content = content.replace(old_data, new_data, 1)
        changes += 1
        print('✅ Added ROLES array')
    else:
        # Try CRLF
        old_data2 = "var activePlatform = 'all';\r\nvar assembled = [];"
        if old_data2 in content:
            new_data2 = new_data.replace('\n', '\r\n')
            content = content.replace(old_data2, new_data2, 1)
            changes += 1
            print('✅ Added ROLES array (CRLF)')
        else:
            print('❌ Cannot find data loading section')

# 3. Add renderRoleFilters to init
if 'renderRoleFilters' not in content:
    old_init = "renderPlatformFilters();\n  renderCategoryTabs();"
    new_init = "renderPlatformFilters();\n  renderRoleFilters();\n  renderCategoryTabs();"
    if old_init in content:
        content = content.replace(old_init, new_init, 1)
        changes += 1
        print('✅ Added renderRoleFilters to init')
    elif old_init.replace('\n', '\r\n') in content:
        content = content.replace(old_init.replace('\n', '\r\n'), new_init.replace('\n', '\r\n'), 1)
        changes += 1
        print('✅ Added renderRoleFilters to init (CRLF)')
    else:
        print('❌ Cannot find init function')

# 4. Add renderRoleFilters and setRole functions after setPlatform
if 'function renderRoleFilters' not in content:
    old_setplat = "function setPlatform(pid) {\n  activePlatform = pid;\n  renderPlatformFilters();\n  renderCategoryTabs();\n  renderBlocks();\n}"
    new_setplat = """function setPlatform(pid) {
  activePlatform = pid;
  renderPlatformFilters();
  renderCategoryTabs();
  renderBlocks();
}

function renderRoleFilters() {
  var el = document.getElementById('roleFilters');
  if (!el) return;
  el.innerHTML = ROLES.map(function(r) {
    return '<button class="role-btn' + (r.id === activeRole ? ' active' : '') + '" onclick="setRole(\\'' + r.id + '\\')">' + r.icon + ' ' + (currentLang === 'en' && r.nameEn ? r.nameEn : r.name) + '</button>';
  }).join('');
}

function setRole(rid) {
  activeRole = rid;
  renderRoleFilters();
  renderCategoryTabs();
  renderBlocks();
}"""
    if old_setplat in content:
        content = content.replace(old_setplat, new_setplat, 1)
        changes += 1
        print('✅ Added renderRoleFilters and setRole functions')
    elif old_setplat.replace('\n', '\r\n') in content:
        content = content.replace(old_setplat.replace('\n', '\r\n'), new_setplat.replace('\n', '\r\n'), 1)
        changes += 1
        print('✅ Added renderRoleFilters and setRole functions (CRLF)')
    else:
        print('❌ Cannot find setPlatform function')

# 5. Add renderRoleFilters to toggleLang
if 'renderRoleFilters' not in content or content.count('renderRoleFilters') < 3:
    old_lang = "renderDashboard();\n  renderCategoryTabs();\n  renderBlocks();"
    new_lang = "renderDashboard();\n  renderCategoryTabs();\n  renderRoleFilters();\n  renderBlocks();"
    if old_lang in content:
        content = content.replace(old_lang, new_lang, 1)
        changes += 1
        print('✅ Added renderRoleFilters to toggleLang')
    elif old_lang.replace('\n', '\r\n') in content:
        content = content.replace(old_lang.replace('\n', '\r\n'), new_lang.replace('\n', '\r\n'), 1)
        changes += 1
        print('✅ Added renderRoleFilters to toggleLang (CRLF)')
    else:
        print('⚠️ toggleLang section not found (might already have renderRoleFilters)')

# 6. Update renderDashboard with role count and workflow count
if 'dashRoles' not in content:
    # Find the renderDashboard function and replace it
    import re
    old_dash = re.search(r'function renderDashboard\(\).*?\n\}', content, re.DOTALL)
    if old_dash:
        new_dash = """function renderDashboard() {
  var totalBlocks = 0;
  var roleSet = {};
  CATEGORIES.forEach(function(c) { c.blocks.forEach(function(b) {
    totalBlocks++;
    if (b.agentRole) roleSet[b.agentRole] = true;
  }); });
  var roleCount = Object.keys(roleSet).length;
  var el = document.getElementById('dashboard');
  el.innerHTML =
    '<div class="stat-item"><div class="stat-value">' + totalBlocks + '</div><div class="stat-label">' + t('dashBlocks') + '</div></div>' +
    '<div class="stat-divider"></div>' +
    '<div class="stat-item"><div class="stat-value">' + roleCount + '</div><div class="stat-label">' + t('dashRoles') + '</div></div>' +
    '<div class="stat-divider"></div>' +
    '<div class="stat-item"><div class="stat-value">4</div><div class="stat-label">' + t('dashWorkflows') + '</div></div>' +
    '<div class="stat-divider"></div>' +
    '<div class="stat-item"><div class="stat-value">' + CATEGORIES.length + '</div><div class="stat-label">' + t('dashCategories') + '</div></div>' +
    '<div class="stat-divider"></div>' +
    '<div class="stat-item"><div class="stat-value">' + (PLATFORMS.length - 1) + '</div><div class="stat-label">' + t('dashPlatforms') + '</div></div>' +
    '<div class="stat-divider"></div>' +
    '<div class="stat-item"><div class="stat-value">' + PRESETS.length + '</div><div class="stat-label">' + t('dashPresets') + '</div></div>' +
    '<div class="stat-divider"></div>' +
    '<div class="stat-item"><div class="stat-value" style="font-size:14px">开源</div><div class="stat-label"><a class="stat-link" href="https://github.com/wyjing333-dev/promptblocks" target="_blank">GitHub 项目</a></div></div>';
}"""
        content = content[:old_dash.start()] + new_dash + content[old_dash.end():]
        changes += 1
        print('✅ Updated renderDashboard')
    else:
        print('❌ Cannot find renderDashboard function')

# 7. Add i18n keys for dashboard
if 'dashRoles' not in content:
    old_i18n_zh = "aiPlatform: 'AI 平台：',\n    roleFilter: '角色：',"
    new_i18n_zh = "aiPlatform: 'AI 平台：',\n    roleFilter: '角色：',\n    dashBlocks: '积木总数', dashRoles: '角色', dashWorkflows: '工作流', dashCategories: '分类', dashPlatforms: '适配平台', dashPresets: '预设模板',"
    if old_i18n_zh in content:
        content = content.replace(old_i18n_zh, new_i18n_zh, 1)
        changes += 1
        print('✅ Added zh i18n keys')
    elif old_i18n_zh.replace('\n', '\r\n') in content:
        content = content.replace(old_i18n_zh.replace('\n', '\r\n'), new_i18n_zh.replace('\n', '\r\n'), 1)
        changes += 1
        print('✅ Added zh i18n keys (CRLF)')
    else:
        # Try without roleFilter
        old_i18n_zh2 = "aiPlatform: 'AI 平台：',"
        if old_i18n_zh2 in content:
            new_i18n_zh2 = "aiPlatform: 'AI 平台：',\n    roleFilter: '角色：',\n    dashBlocks: '积木总数', dashRoles: '角色', dashWorkflows: '工作流', dashCategories: '分类', dashPlatforms: '适配平台', dashPresets: '预设模板',"
            content = content.replace(old_i18n_zh2, new_i18n_zh2, 1)
            changes += 1
            print('✅ Added zh i18n keys (no existing roleFilter)')
        else:
            print('❌ Cannot find zh i18n section')

# 8. Add en i18n keys
if content.count('dashRoles') < 2:
    old_i18n_en = "aiPlatform: 'AI Platform: ',"
    if old_i18n_en in content:
        # Check if roleFilter already exists in en
        if "roleFilter: 'Role: '" in content:
            old_i18n_en2 = "aiPlatform: 'AI Platform: ',\n    roleFilter: 'Role: ',"
            new_i18n_en2 = "aiPlatform: 'AI Platform: ',\n    roleFilter: 'Role: ',\n    dashBlocks: 'Blocks', dashRoles: 'Roles', dashWorkflows: 'Workflows', dashCategories: 'Categories', dashPlatforms: 'Platforms', dashPresets: 'Presets',"
            if old_i18n_en2 in content:
                content = content.replace(old_i18n_en2, new_i18n_en2, 1)
            elif old_i18n_en2.replace('\n', '\r\n') in content:
                content = content.replace(old_i18n_en2.replace('\n', '\r\n'), new_i18n_en2.replace('\n', '\r\n'), 1)
        else:
            new_i18n_en = "aiPlatform: 'AI Platform: ',\n    roleFilter: 'Role: ',\n    dashBlocks: 'Blocks', dashRoles: 'Roles', dashWorkflows: 'Workflows', dashCategories: 'Categories', dashPlatforms: 'Platforms', dashPresets: 'Presets',"
            content = content.replace(old_i18n_en, new_i18n_en, 1)
        changes += 1
        print('✅ Added en i18n keys')
    else:
        print('❌ Cannot find en i18n section')

# 9. Add role filter to renderBlocks
if 'agentRole' not in content or content.count('agentRole') < 2:
    # Find renderBlocks and add role filter
    old_render = """  var filtered = activePlatform === 'all'
    ? cat.blocks
    : cat.blocks.filter(function(b) { return b.platforms.indexOf('all') !== -1 || b.platforms.indexOf(activePlatform) !== -1; });"""
    new_render = """  var filtered = cat.blocks;
  if (activePlatform !== 'all') {
    filtered = filtered.filter(function(b) { return b.platforms.indexOf('all') !== -1 || b.platforms.indexOf(activePlatform) !== -1; });
  }
  if (activeRole !== 'all') {
    filtered = filtered.filter(function(b) { return b.agentRole === activeRole; });
  }"""
    if old_render in content:
        content = content.replace(old_render, new_render, 1)
        changes += 1
        print('✅ Added role filter to renderBlocks')
    elif old_render.replace('\n', '\r\n') in content:
        content = content.replace(old_render.replace('\n', '\r\n'), new_render.replace('\n', '\r\n'), 1)
        changes += 1
        print('✅ Added role filter to renderBlocks (CRLF)')
    else:
        # Try the original version without ternary
        old_render2 = "var filtered = activePlatform === 'all'\n    ? cat.blocks\n    : cat.blocks.filter(function(b) { return b.platforms.indexOf('all') !== -1 || b.platforms.indexOf(activePlatform) !== -1; });"
        if old_render2 in content:
            content = content.replace(old_render2, new_render, 1)
            changes += 1
            print('✅ Added role filter to renderBlocks (v2)')
        else:
            print('❌ Cannot find renderBlocks filter section')

# 10. Add role tag in block items
if "roleTag" not in content:
    old_tags = "b.tags.map(function(t) { return '<span class=\"tag\">' + t + '</span>'; }).join('')"
    new_tags = "var roleTag = b.agentRole && b.agentRole !== 'general' ? '<span class=\"tag\" style=\"background:rgba(236,72,153,0.12);color:#f9a8d4;\">' + b.agentRole + '</span>' : '';\n      '<div class=\"tags\">' + roleTag + b.tags.map(function(t) { return '<span class=\"tag\">' + t + '</span>'; }).join('')"
    if old_tags in content:
        # Actually need to add roleTag before the tags div
        old_block = "'<div class=\"tags\">' + b.tags.map"
        new_block = "var roleTag = b.agentRole && b.agentRole !== 'general' ? '<span class=\"tag\" style=\"background:rgba(236,72,153,0.12);color:#f9a8d4;\">' + b.agentRole + '</span>' : '';\n      '<div class=\"tags\">' + roleTag + b.tags.map"
        if old_block in content:
            content = content.replace(old_block, new_block, 1)
            changes += 1
            print('✅ Added role tag in block items')
        elif old_block.replace('\n', '\r\n') in content:
            content = content.replace(old_block.replace('\n', '\r\n'), new_block.replace('\n', '\r\n'), 1)
            changes += 1
            print('✅ Added role tag in block items (CRLF)')
        else:
            print('⚠️ Could not add roleTag to block items (non-critical)')

# 11. Add mobile responsive for role-bar
if 'role-bar' in content and '.role-bar' in content and 'role-bar' not in content.split('@media')[1] if '@media' in content else True:
    old_mobile = "    .stat-item .stat-value { font-size: 16px; }"
    new_mobile = "    .stat-item .stat-value { font-size: 16px; }\n    .role-bar { padding: 6px 12px; gap: 6px; }\n    .platform-bar { padding: 6px 12px; }"
    if old_mobile in content and '.role-bar' not in content.split('@media (max-width: 768px)')[1].split('}')[0] if '@media (max-width: 768px)' in content else False:
        content = content.replace(old_mobile, new_mobile, 1)
        changes += 1
        print('✅ Added mobile responsive for role-bar')
    else:
        # Just check if role-bar mobile already there
        if 'role-bar' in content and content.count('role-bar') >= 3:
            print('✅ role-bar mobile CSS already present')
        else:
            print('⚠️ Could not add mobile CSS (non-critical)')

# Write back
with open('D:/jieyuexingchen/promptblocks/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f'\n✅ Total changes: {changes}')

# Final verification
final_checks = [
    ('renderRoleFilters', 'renderRoleFilters function'),
    ('setRole', 'setRole function'),
    ('ROLES', 'ROLES array'),
    ('activeRole', 'activeRole variable'),
    ('role-btn', 'role-btn CSS'),
    ('dashRoles', 'dashRoles i18n'),
    ('dashWorkflows', 'dashWorkflows i18n'),
    ('agentRole', 'agentRole in renderBlocks'),
    ('role-bar', 'role-bar HTML'),
    ('面向角色', 'title positioning'),
]
print('\nFinal verification:')
for pattern, desc in final_checks:
    found = pattern in content
    count = content.count(pattern)
    print(f'  {"✅" if found else "❌"} {desc}: {"found" if found else "MISSING"} ({count}x)')
