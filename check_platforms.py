import json

with open(r"D:\jieyuexingchen\promptblocks\blocks.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=== Platform objects in blocks.json ===")
for p in data.get('platforms', []):
    print(json.dumps(p, ensure_ascii=False))

print(f"\n=== Total platforms: {len(data.get('platforms', []))} ===")
