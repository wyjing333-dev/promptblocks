import re

with open(r'D:\jieyuexingchen\promptblocks\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    # Assembly area
    ('<span id="centerTitle">拼装区</span> <span class="count" id="assemblyCount">0 个积木</span>',
     '<span id="centerTitle" data-i18n="assemblyArea">拼装区</span> <span class="count" id="assemblyCount">0 <span data-i18n="blocks">个积木</span></span>'),
    ('<button class="btn btn-secondary" style="padding:4px 12px;font-size:12px" onclick="clearAll()">清空</button>',
     '<button class="btn btn-secondary" style="padding:4px 12px;font-size:12px" onclick="clearAll()" data-i18n="clear">清空</button>'),
    # Output panel
    ('<div class="panel-header">生成的Prompt</div>',
     '<div class="panel-header" data-i18n="generatedPrompt">生成的Prompt</div>'),
    ('<div class="prompt-preview empty" id="promptPreview">从左侧选择积木，你的Prompt会在这里实时生成...</div>',
     '<div class="prompt-preview empty" id="promptPreview" data-i18n="promptPlaceholder">从左侧选择积木，你的Prompt会在这里实时生成...</div>'),
    # Copy/Reset buttons
    ('<span>📋</span> 复制Prompt', '<span>📋</span> <span data-i18n="copyPrompt">复制Prompt</span>'),
    ('<button class="btn btn-secondary" onclick="resetAll()" style="padding:10px 14px">重置</button>',
     '<button class="btn btn-secondary" onclick="resetAll()" style="padding:10px 14px" data-i18n="reset">重置</button>'),
    # Sponsors
    ('<div class="sponsor-label">赞助商</div>',
     '<div class="sponsor-label" data-i18n="sponsor">赞助商</div>'),
    ('<div class="sponsor-content">成为首个赞助商，共建 Prompt 积木生态 &middot; <a href="https://github.com/wyjing333-dev/promptblocks" target="_blank">联系我们</a></div>',
     '<div class="sponsor-content"><span data-i18n="sponsorContent">成为首个赞助商，共建 Prompt 积木生态</span> &middot; <a href="https://github.com/wyjing333-dev/promptblocks" target="_blank" data-i18n="contactUs">联系我们</a></div>'),
    # Toast
    ('<div class="toast" id="toast">已复制到剪贴板！</div>',
     '<div class="toast" id="toast" data-i18n="copied">已复制到剪贴板！</div>'),
    # Star modal
    ('<h3>觉得好用？给个Star吧！</h3>',
     '<h3 data-i18n="starTitle">觉得好用？给个Star吧！</h3>'),
    ('<p>PromptBlocks 是开源免费项目，你的 Star 是小猫持续更新的最大动力~</p>',
     '<p data-i18n="starDesc">PromptBlocks 是开源免费项目，你的 Star 是小猫持续更新的最大动力~</p>'),
    ('<a class="star-go" href="https://github.com/wyjing333-dev/promptblocks" target="_blank" onclick="closeStarModal()">⭐ 去 Star</a>',
     '<a class="star-go" href="https://github.com/wyjing333-dev/promptblocks" target="_blank" onclick="closeStarModal()">⭐ <span data-i18n="goStar">去 Star</span></a>'),
    ('<button class="star-later" onclick="closeStarModal()">下次再说</button>',
     '<button class="star-later" onclick="closeStarModal()" data-i18n="later">下次再说</button>'),
]

count = 0
for old, new in replacements:
    if old in content:
        content = content.replace(old, new, 1)
        count += 1
    else:
        # Check if already replaced
        if new not in content:
            print(f'NOT FOUND: {old[:60]}...')

with open(r'D:\jieyuexingchen\promptblocks\index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print(f'{count}/{len(replacements)} replacements applied')
