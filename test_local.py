import urllib.request, json, re

# Test local server
print("=== Local Server Test ===")
try:
    resp = urllib.request.urlopen("http://localhost:8765/", timeout=5)
    html = resp.read().decode("utf-8")
    print(f"HTTP {resp.status}, {len(html)} bytes")
    
    # Check if there's an obvious error in the HTML
    if len(html) < 100:
        print("WARNING: HTML too short!")
        print(html[:200])
    else:
        # Check for common JS issues
        # Find all <script> blocks without src attribute
        scripts = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', html, re.DOTALL)
        print(f"Found {len(scripts)} inline script blocks")
        
        # Try to find syntax issues - check for unclosed brackets in key functions
        for i, script in enumerate(scripts):
            # Count brackets
            opens = script.count('{')
            closes = script.count('}')
            parens_open = script.count('(')
            parens_close = script.count(')')
            brackets_open = script.count('[')
            brackets_close = script.count(']')
            print(f"Script {i+1}: {{}}={opens}/{closes}, ()={parens_open}/{parens_close}, []={brackets_open}/{brackets_close}, len={len(script)}")
            if opens != closes:
                print(f"  WARNING: Mismatched curly braces! {opens} open vs {closes} close")
            if parens_open != parens_close:
                print(f"  WARNING: Mismatched parens! {parens_open} open vs {parens_close} close")
            if brackets_open != brackets_close:
                print(f"  WARNING: Mismatched brackets! {brackets_open} open vs {brackets_close} close")
        
        # Check for the error message in HTML
        if "数据加载失败" in html:
            idx = html.index("数据加载失败")
            print(f"\nError message found at char {idx}:")
            print(html[max(0,idx-100):idx+200])
except Exception as e:
    print(f"FAILED: {e}")

# Also check blocks.json locally
print("\n=== Local blocks.json Test ===")
try:
    resp2 = urllib.request.urlopen("http://localhost:8765/blocks.json", timeout=5)
    data2 = resp2.read().decode("utf-8")
    parsed = json.loads(data2)
    print(f"HTTP {resp2.status}, valid JSON, categories={len(parsed.get('categories',[]))}")
except Exception as e:
    print(f"FAILED: {e}")

# Check cases.json
print("\n=== Local cases.json Test ===")
try:
    resp3 = urllib.request.urlopen("http://localhost:8765/cases.json", timeout=5)
    data3 = resp3.read().decode("utf-8")
    try:
        parsed3 = json.loads(data3)
        print(f"HTTP {resp3.status}, valid JSON")
    except json.JSONDecodeError as e:
        print(f"HTTP {resp3.status}, INVALID JSON: {e}")
        # Show the problematic area
        lines = data3.split('\n')
        err_line = int(str(e).split('line')[1].split()[0]) if 'line' in str(e) else 1
        start = max(0, err_line-3)
        end = min(len(lines), err_line+3)
        for li in range(start, end):
            marker = ">>>" if li == err_line-1 else "   "
            print(f"{marker} L{li+1}: {lines[li][:120]}")
except Exception as e:
    print(f"FAILED: {e}")
