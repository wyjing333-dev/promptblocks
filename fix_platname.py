import re

html_path = r"D:\jieyuexingchen\promptblocks\index.html"
with open(html_path, 'r', encoding='utf-8') as f:
    content = f.read()

# The platName function to insert - goes right after the t() function
platName_func = """
function platName(p) {
  if (!p) return '';
  return (currentLang === 'en' && p.nameEn) ? p.nameEn : p.name;
}
"""

# Find the end of the t() function
# t() function starts at L562
t_func_pattern = r'(function t\(key\) \{\s*return \([^)]+\) \|\| key;\s*\})'
match = re.search(t_func_pattern, content)

if match:
    insert_pos = match.end()
    new_content = content[:insert_pos] + platName_func + content[insert_pos:]
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"SUCCESS: platName function inserted at char {insert_pos} (after t() function)")
    print(f"\nInserted function:")
    print(platName_func)
    
    # Verify: count occurrences now
    count = new_content.count('function platName')
    print(f"\nVerification: 'function platName' appears {count} time(s) in updated file")
else:
    print("ERROR: Could not find t() function with regex")
    print("Trying alternative approach...")
    
    # Find by line number
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'function t(key)' in line:
            print(f"Found 'function t(key)' at line {i+1}")
            # Find the closing brace
            brace_count = 0
            j = i
            while j < len(lines):
                brace_count += lines[j].count('{')
                brace_count -= lines[j].count('}')
                if brace_count <= 0 and j > i:
                    print(f"  Function ends at line {j+1}")
                    print(f"  Line {j+1}: {lines[j]}")
                    break
                j += 1
            break
