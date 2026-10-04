import re

html_path = r"D:\jieyuexingchen\promptblocks\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find PLATFORMS definition
print("=== PLATFORMS definition ===")
m = re.search(r'var\s+PLATFORMS\s*=\s*\[', content)
if m:
    start = m.start()
    # Find matching closing bracket
    bracket_count = 0
    i = m.end() - 1
    while i < len(content):
        if content[i] == '[':
            bracket_count += 1
        elif content[i] == ']':
            bracket_count -= 1
            if bracket_count == 0:
                break
        i += 1
    platforms_text = content[start:i+1]
    print(platforms_text[:1000])
    print(f"\n... total length: {len(platforms_text)} chars")
    
    # Check if platforms have 'name' field
    names = re.findall(r"name['\"]?\s*:", platforms_text)
    print(f"\n'name' fields found: {len(names)}")
    
    # Check for name_zh, name_en etc
    name_fields = re.findall(r'name\w*["\']?\s*:', platforms_text)
    print(f"All name* fields: {name_fields}")
else:
    print("PLATFORMS not found as 'var PLATFORMS = ['")
    # Try alternate patterns
    for pattern in ['PLATFORMS', 'platforms']:
        idx = content.find(pattern)
        if idx >= 0:
            print(f"\nFound '{pattern}' at char {idx}:")
            print(content[idx:idx+200])

# Search for any function that might be the intended platName
print("\n\n=== Searching for platform name functions ===")
for pattern in [r'function\s+platName', r'function\s+getPlat', r'function\s+platformName', r'platName\s*=']:
    matches = list(re.finditer(pattern, content))
    print(f"'{pattern}': {len(matches)} matches")
    for m in matches:
        print(f"  at char {m.start()}: {content[m.start():m.start()+100]}")

# Search for how other render functions get platform names
print("\n\n=== renderPlatformTags function ===")
m2 = re.search(r'function\s+renderPlatformTags.*?(?=\n\s*function\s+\w+|\n\s*</script>)', content, re.DOTALL)
if m2:
    print(m2.group()[:500])
