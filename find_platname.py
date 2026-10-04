import re

html_path = r"D:\jieyuexingchen\promptblocks\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all occurrences of platName
matches = [(m.start(), m.group()) for m in re.finditer(r'platName', content)]
print(f"Found {len(matches)} occurrences of 'platName':")
for pos, match in matches:
    # Get surrounding context (200 chars before and after)
    start = max(0, pos - 150)
    end = min(len(content), pos + 150)
    context = content[start:end].replace('\n', '\\n')
    line_num = content[:pos].count('\n') + 1
    print(f"\n--- Line {line_num}, char {pos} ---")
    print(context)

# Also find the renderPlatformFilters function
print("\n\n=== renderPlatformFilters function ===")
m = re.search(r'function\s+renderPlatformFilters.*?(?=\n\s*function\s+\w+|\n\s*</script>)', content, re.DOTALL)
if m:
    func_text = m.group()
    print(f"Length: {len(func_text)} chars")
    # Print first 500 chars
    print(func_text[:500])
    print("...")
    # Print around the map call
    map_idx = func_text.find('.map')
    if map_idx >= 0:
        print(f"\n--- Around .map call ---")
        print(func_text[max(0,map_idx-200):map_idx+400])
else:
    print("Function not found by regex, searching for 'renderPlatformFilters'")
    idx = content.find('renderPlatformFilters')
    if idx >= 0:
        chunk = content[idx:idx+1500]
        print(chunk)
