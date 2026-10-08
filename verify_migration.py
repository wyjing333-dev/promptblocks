# -*- coding: utf-8 -*-
"""验证迁移结果"""
import json

with open('D:/jieyuexingchen/promptblocks/blocks.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 看一个标准化后的积木
for cat in data['categories']:
    if cat['id'] == 'task':
        for b in cat['blocks']:
            if b['id'] == 'task-write-article':
                print('=== 示例: task-write-article ===')
                print(json.dumps(b, ensure_ascii=False, indent=2))
                print()
                break
    if cat['id'] == 'role':
        for b in cat['blocks']:
            if b['id'] == 'role-marketer':
                print('=== 示例: role-marketer ===')
                print(json.dumps(b, ensure_ascii=False, indent=2))
                print()
                break

# 统计新字段覆盖率
all_blocks = []
for cat in data['categories']:
    all_blocks.extend(cat.get('blocks', []))

new_fields = ['agentRole', 'inputs', 'prerequisites', 'outputFormat', 'qualityChecks', 'recommendedWith']
print(f'总积木: {len(all_blocks)}')
print()
print('新字段覆盖率:')
for field in new_fields:
    count = sum(1 for b in all_blocks if field in b)
    print(f'  {field}: {count}/{len(all_blocks)} ({count*100//len(all_blocks)}%)')

print()
print('outputFormat分布:')
from collections import Counter
fmt_counts = Counter(b.get('outputFormat', 'missing') for b in all_blocks)
for fmt, c in sorted(fmt_counts.items(), key=lambda x: -x[1]):
    print(f'  {fmt}: {c}个')

print()
print('agentRole分布:')
role_counts = Counter(b.get('agentRole', 'missing') for b in all_blocks)
for role, c in sorted(role_counts.items(), key=lambda x: -x[1]):
    print(f'  {role}: {c}个')

print()
print('qualityChecks示例:')
for b in all_blocks[:3]:
    checks = b.get('qualityChecks', [])
    print(f'  {b["id"]}: {len(checks)}项 - {checks[0] if checks else "无"}')
