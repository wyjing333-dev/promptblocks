# -*- coding: utf-8 -*-
"""Check blocks.json structure - find blocks within categories"""
import json, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
blocks_path = os.path.join(BASE, "blocks.json")

with open(blocks_path, "r", encoding="utf-8") as f:
    data = json.load(f)

categories = data.get("categories", [])
total_blocks = 0
for cat in categories:
    cat_blocks = cat.get("blocks", [])
    total_blocks += len(cat_blocks)
    print(f"\n=== {cat['id']} ({cat['name']}) - {len(cat_blocks)} blocks ===")
    for b in cat_blocks:
        print(f"  {b.get('id','?')}: {b.get('name','?')}")

print(f"\nTotal blocks: {total_blocks}")

# Print full structure of last block in last category
last_cat = categories[-1]
last_block = last_cat["blocks"][-1]
print(f"\n=== Full structure of last block ({last_block.get('id')}) ===")
print(json.dumps(last_block, ensure_ascii=False, indent=2))
