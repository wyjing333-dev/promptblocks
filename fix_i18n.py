# -*- coding: utf-8 -*-
"""修复i18n: 添加 neverShow 翻译"""

filepath = 'D:/jieyuexingchen/promptblocks/index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 找到现有的 i18n 键值
import re

# 找到中文 i18n 行: goStar: '去 Star', later: '下次再说',
zh_old = "goStar: '去 Star', later: '下次再说',"
zh_new = "goStar: '去 Star', later: '下次再说', neverShow: '不再提醒',"
if zh_old in content:
    content = content.replace(zh_old, zh_new)
    print("✅ 中文i18n: neverShow 已添加")
else:
    print("❌ 中文i18n: 找不到目标字符串")

# 找到英文 i18n 行: goStar: 'Star on GitHub', later: 'Maybe later',
en_old = "goStar: 'Star on GitHub', later: 'Maybe later',"
en_new = "goStar: 'Star on GitHub', later: 'Maybe later', neverShow: \"Don't show again\","
if en_old in content:
    content = content.replace(en_old, en_new)
    print("✅ 英文i18n: neverShow 已添加")
else:
    print("❌ 英文i18n: 找不到目标字符串")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nDone!")
