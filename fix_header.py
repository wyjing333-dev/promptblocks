import re

with open(r'D:\jieyuexingchen\promptblocks\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix header-right section
old_header = '''      <button class="mode-btn active" id="modeAssembly" onclick="setMode('assembly')">🧱 拼装</button>
      <button class="mode-btn" id="modeQuick" onclick="setMode('quick')">⚡ 快捷</button>
    </div>
    <a class="tool-link" href="block-recommender.html">🧩 推荐器</a>
    <a class="tool-link" href="prompt-scorer.html">🔍 评分器</a>
    <a class="star-btn" href="https://github.com/wyjing333-dev/promptblocks" target="_blank">⭐ Star</a>
    <a class="submit-btn" href="https://github.com/wyjing333-dev/promptblocks/issues/new?labels=submit-block&template=submit-block.md&title=%E6%8F%90%E4%BA%A4%E6%96%B0%E7%A7%AF%E6%9C%A8" target="_blank">➕ 提交积木</a>'''

new_header = '''      <button class="mode-btn active" id="modeAssembly" onclick="setMode('assembly')">🧱 <span data-i18n="modeAssembly">拼装</span></button>
      <button class="mode-btn" id="modeQuick" onclick="setMode('quick')">⚡ <span data-i18n="modeQuick">快捷</span></button>
    </div>
    <a class="tool-link" href="block-recommender.html">🧩 <span data-i18n="recommender">推荐器</span></a>
    <a class="tool-link" href="cases.html">📊 <span data-i18n="cases">效果案例</span></a>
    <a class="tool-link" href="prompt-scorer.html">🔍 <span data-i18n="scorer">评分器</span></a>
    <a class="tool-link" href="https://github.com/wyjing333-dev/promptblocks/tree/master/mcp-server" target="_blank">🔌 MCP</a>
    <a class="star-btn" href="https://github.com/wyjing333-dev/promptblocks" target="_blank">⭐ Star</a>
    <a class="tool-link" href="javascript:void(0)" onclick="startTutorial()">📖 <span data-i18n="tutorial">教程</span></a>
    <a class="tool-link" id="langToggle" href="javascript:void(0)" onclick="toggleLang()">🌐 EN</a>
    <a class="submit-btn" href="https://github.com/wyjing333-dev/promptblocks/issues/new?labels=submit-block&template=submit-block.md&title=%E6%8F%90%E4%BA%A4%E6%96%B0%E7%A7%AF%E6%9C%A8" target="_blank">➕ <span data-i18n="submitBlock">提交积木</span></a>'''

if old_header in content:
    content = content.replace(old_header, new_header)
    with open(r'D:\jieyuexingchen\promptblocks\index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Header replaced successfully!')
else:
    # Try to find the header section with regex
    pattern = r'<button class="mode-btn active".*?提交积木</a>'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        print(f'Found header with regex at position {match.start()}-{match.end()}')
        print(f'First 200 chars: {match.group()[:200]}')
        content = content[:match.start()] + new_header + content[match.end():]
        with open(r'D:\jieyuexingchen\promptblocks\index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print('Header replaced via regex!')
    else:
        print('Header not found! Trying line-by-line...')
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'modeAssembly' in line:
                print(f'Line {i+1}: {line[:100]}')
            if '提交积木' in line:
                print(f'Line {i+1}: {line[:100]}')
            if 'MCP' in line:
                print(f'Line {i+1} MCP: {line[:100]}')
