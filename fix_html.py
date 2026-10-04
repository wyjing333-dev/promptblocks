import re

with open(r'D:\jieyuexingchen\promptblocks\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find loadData(init); and function renderPresets
start_marker = 'loadData(init);'
end_marker = 'function renderPresets() {'

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx == -1 or end_idx == -1:
    print(f'Marker not found. start={start_idx}, end={end_idx}')
    exit(1)

# Keep everything up to and including loadData(init); + newline, then function renderPresets
new_content = content[:start_idx + len(start_marker)] + '\n\n' + content[end_idx:]

with open(r'D:\jieyuexingchen\promptblocks\index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

# Verify
with open(r'D:\jieyuexingchen\promptblocks\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f'Done. File now has {len(lines)} lines.')

# Show context around the join point
for i, line in enumerate(lines):
    if 'loadData(init)' in line:
        for j in range(max(0,i-2), min(len(lines), i+5)):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
