# -*- coding: utf-8 -*-
"""检查blocks.json完整结构 - 积木在categories[].blocks里"""
import json
from collections import Counter

with open('D:/jieyuexingchen/promptblocks/blocks.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

cats = data['categories']
print(f'分类数: {len(cats)}')
print()

all_blocks = []
for cat in cats:
    blocks = cat.get('blocks', [])
    print(f'{cat["id"]} ({cat["name"]}): {len(blocks)}个积木')
    all_blocks.extend(blocks)
    if blocks:
        print(f'  字段: {list(blocks[0].keys())}')
        # 看第一个积木
        b = blocks[0]
        print(f'  示例: {b.get("id","?")} - {b.get("title","?")}')
        print(f'    content_len={len(b.get("content",""))}')
        print(f'    tags={b.get("tags",[])}')
        print(f'    platforms={b.get("platforms",[])}')
        has_en = 'titleEn' in b and 'contentEn' in b
        print(f'    has_en={has_en}')
    print()

print(f'总积木数: {len(all_blocks)}')
print()

# 检查所有积木的字段完整性
field_counts = Counter()
for b in all_blocks:
    for k in b.keys():
        field_counts[k] += 1

print('字段覆盖率:')
for field, count in sorted(field_counts.items(), key=lambda x: -x[1]):
    print(f'  {field}: {count}/{len(all_blocks)} ({count*100//len(all_blocks)}%)')
