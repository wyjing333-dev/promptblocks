import json

with open(r'D:\jieyuexingchen\promptblocks\blocks.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

cats = data.get('categories', [])
total = 0
for c in cats:
    count = len(c['blocks'])
    total += count
    print(f"\n[{c['id']}] {c['name']} ({c.get('nameEn','')}) - {count} blocks:")
    for b in c['blocks']:
        print(f"  - {b['id']}: {b['title']}")

print(f"\n=== Total: {len(cats)} categories, {total} blocks ===")

# Show presets
presets = data.get('presets', [])
if presets:
    print(f"\nPresets ({len(presets)}):")
    for p in presets:
        print(f"  - {p.get('id','?')}: {p.get('title', p.get('name',''))}")
