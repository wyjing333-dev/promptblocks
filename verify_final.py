# -*- coding: utf-8 -*-
import json
from collections import Counter
with open('D:/jieyuexingchen/promptblocks/blocks.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
all_blocks = []
for cat in data['categories']:
    all_blocks.extend(cat.get('blocks', []))
print(f'JSON valid! total={len(all_blocks)}, cats={len(data["categories"])}, presets={len(data["presets"])}, platforms={len(data["platforms"])}')
print()
roles = Counter(b.get('agentRole', '?') for b in all_blocks)
print('Role distribution:')
for r, c in sorted(roles.items(), key=lambda x: -x[1]):
    print(f'  {r}: {c}')
