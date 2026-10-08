# -*- coding: utf-8 -*-
"""列出所有积木id和title，按分类"""
import json

with open('D:/jieyuexingchen/promptblocks/blocks.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for cat in data['categories']:
    print(f'\n=== {cat["id"]} ({cat["name"]}) - {len(cat["blocks"])}个 ===')
    for b in cat['blocks']:
        role = b.get('agentRole', '?')
        print(f'  {b["id"]:40s} | {b["title"]:20s} | role={role}')
