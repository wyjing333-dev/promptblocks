# -*- coding: utf-8 -*-
"""验证工作流引用的积木id都存在"""
import json

with open('D:/jieyuexingchen/promptblocks/blocks.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
with open('D:/jieyuexingchen/promptblocks/workflows.json', 'r', encoding='utf-8') as f:
    workflows = json.load(f)

# 收集所有积木id
all_ids = set()
for cat in data['categories']:
    for b in cat.get('blocks', []):
        all_ids.add(b['id'])

print(f'积木总数: {len(all_ids)}')
print(f'工作流数: {len(workflows)}')
print()

all_valid = True
for wf in workflows:
    print(f'{wf["icon"]} {wf["name"]} ({len(wf["steps"])}步)')
    for step in wf['steps']:
        bid = step['blockId']
        exists = bid in all_ids
        status = '✅' if exists else '❌'
        print(f'  {status} Step{step["step"]}: {step["name"]} -> {bid}')
        if not exists:
            all_valid = False
    print()

print('结果:', '✅ 全部引用有效' if all_valid else '❌ 有无效引用')
