# -*- coding: utf-8 -*-
"""Insert role-bar HTML into index.html"""

with open('D:/jieyuexingchen/promptblocks/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check if role-bar already exists
if 'role-bar' in content:
    print('role-bar already exists, skipping')
else:
    # Insert role-bar after platform-bar closing div, before dashboard
    old = '</div>\n\n<div class="dashboard" id="dashboard"></div>'
    new = '</div>\n\n<div class="role-bar" id="roleBar">\n  <span class="rlabel" data-i18n="roleFilter">角色：</span>\n  <div class="role-filters" id="roleFilters"></div>\n</div>\n\n<div class="dashboard" id="dashboard"></div>'
    
    if old in content:
        content = content.replace(old, new, 1)
        with open('D:/jieyuexingchen/promptblocks/index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print('✅ role-bar inserted successfully')
    else:
        # Try with \r\n
        old2 = '</div>\r\n\r\n<div class="dashboard" id="dashboard"></div>'
        if old2 in content:
            new2 = '</div>\r\n\r\n<div class="role-bar" id="roleBar">\r\n  <span class="rlabel" data-i18n="roleFilter">角色：</span>\r\n  <div class="role-filters" id="roleFilters"></div>\r\n</div>\r\n\r\n<div class="dashboard" id="dashboard"></div>'
            content = content.replace(old2, new2, 1)
            with open('D:/jieyuexingchen/promptblocks/index.html', 'w', encoding='utf-8') as f:
                f.write(content)
            print('✅ role-bar inserted (CRLF version)')
        else:
            print('❌ Could not find target text')
            # Show surrounding text for debugging
            idx = content.find('dashboard')
            if idx >= 0:
                print(f'Context around "dashboard": ...{repr(content[idx-60:idx+40])}...')

# Also check all other changes
checks = [
    ('面向角色的AI工作流平台', 'title/tagline'),
    ('renderRoleFilters', 'renderRoleFilters function'),
    ('setRole', 'setRole function'),
    ('ROLES', 'ROLES array'),
    ('activeRole', 'activeRole variable'),
    ('role-btn', 'role-btn CSS'),
    ('roleFilter', 'roleFilter i18n'),
    ('dashRoles', 'dashRoles i18n'),
    ('dashWorkflows', 'dashWorkflows i18n'),
    ('workflows.html', 'workflows link'),
]
print()
for pattern, desc in checks:
    found = pattern in content
    print(f'  {"✅" if found else "❌"} {desc}: {"found" if found else "MISSING"}')
