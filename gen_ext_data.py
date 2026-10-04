"""
Generate chrome-extension/blocks-data.js from blocks.json
"""
import json

with open(r'D:\jieyuexingchen\promptblocks\blocks.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

categories = data.get('categories', [])
blocks_flat = []

for cat in categories:
    for block in cat.get('blocks', []):
        blocks_flat.append({
            'id': block['id'],
            'title': block.get('titleEn') or block.get('title', ''),
            'content': block.get('contentEn') or block.get('content', ''),
            'categoryId': cat['id']
        })

cat_list = [{'id': c['id'], 'name': c.get('nameEn') or c.get('name', ''), 'icon': c.get('icon', '')} for c in categories]

js_content = '// Auto-generated from blocks.json - do not edit manually\n'
js_content += '// PromptBlocks Chrome Extension Data\n\n'
js_content += 'window.PB_CATEGORIES = ' + json.dumps(cat_list, ensure_ascii=False) + ';\n'
js_content += 'window.PB_BLOCKS = ' + json.dumps(blocks_flat, ensure_ascii=False) + ';\n'

with open(r'D:\jieyuexingchen\promptblocks\chrome-extension\blocks-data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f'Generated blocks-data.js: {len(blocks_flat)} blocks, {len(cat_list)} categories')
