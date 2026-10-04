import re

html_path = r"D:\jieyuexingchen\promptblocks\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find ALL occurrences of PLATFORMS
print("=== ALL occurrences of PLATFORMS ===")
for m in re.finditer(r'PLATFORMS', content):
    pos = m.start()
    line = content[:pos].count('\n') + 1
    ctx = content[max(0,pos-80):pos+80].replace('\n','|')
    print(f"  L{line}: ...{ctx}...")

# Find i18n related functions
print("\n=== i18n / t() function ===")
for pattern in [r'function\s+t\b', r'var\s+lang\s*=', r'currentLang', r'i18n', r'function\s+getLang', r'function\s+setLang']:
    matches = list(re.finditer(pattern, content))
    print(f"'{pattern}': {len(matches)} matches")
    for m in matches[:3]:
        pos = m.start()
        line = content[:pos].count('\n') + 1
        print(f"  L{line}: {content[pos:pos+120]}")

# Find the actual platform data - maybe it's in a different format
print("\n=== Searching for platform data (chatgpt, claude, etc) ===")
for kw in ['chatgpt', 'ChatGPT', 'claude', 'Claude', 'gemini', 'Gemini', 'wenxin', '文心']:
    idx = content.find(kw)
    if idx >= 0:
        line = content[:idx].count('\n') + 1
        print(f"  '{kw}' at L{line}: {content[max(0,idx-50):idx+100]}")
    else:
        print(f"  '{kw}': NOT FOUND")

# Find the git diff to see what changed - look for the i18n section
print("\n=== Looking for i18n translations section ===")
m = re.search(r'(var\s+i18n|var\s+translations|var\s+I18N|var\s+MESSAGES)', content)
if m:
    pos = m.start()
    print(f"Found at char {pos}, L{content[:pos].count(chr(10))+1}")
    print(content[pos:pos+500])
else:
    print("No i18n variable found")
    # Search for lang
    for m2 in re.finditer(r'lang', content):
        pos = m2.start()
        line = content[:pos].count('\n') + 1
        ctx = content[max(0,pos-40):pos+40]
        if 'language' in ctx.lower() or 'lang ==' in ctx or 'lang =' in ctx:
            print(f"  L{line}: {ctx}")
