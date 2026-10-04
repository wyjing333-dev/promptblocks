import urllib.request, json

# Test local server
print("=== Local Server Test (port 9999) ===")
try:
    resp = urllib.request.urlopen("http://localhost:9999/", timeout=5)
    html = resp.read().decode("utf-8")
    print(f"index.html: HTTP {resp.status}, {len(html)} bytes")
    
    # Check for JS bracket balance
    import re
    scripts = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', html, re.DOTALL)
    print(f"Found {len(scripts)} inline script blocks")
    for i, script in enumerate(scripts):
        opens = script.count('{')
        closes = script.count('}')
        po = script.count('(')
        pc = script.count(')')
        bo = script.count('[')
        bc = script.count(']')
        status = "OK" if opens == closes and po == pc and bo == bc else "MISMATCH"
        print(f"  Script {i+1}: {{}}={opens}/{closes}, ()={po}/{pc}, []={bo}/{bc}, len={len(script)} [{status}]")
        if status == "MISMATCH":
            print(f"    WARNING: Bracket mismatch detected!")

except Exception as e:
    print(f"FAILED: {e}")

# Test blocks.json
print("\n=== blocks.json ===")
try:
    resp2 = urllib.request.urlopen("http://localhost:9999/blocks.json", timeout=5)
    data2 = resp2.read().decode("utf-8")
    parsed = json.loads(data2)
    print(f"HTTP {resp2.status}, valid JSON, categories={len(parsed.get('categories',[]))}")
except Exception as e:
    print(f"FAILED: {e}")

# Test cases.json
print("\n=== cases.json ===")
try:
    resp3 = urllib.request.urlopen("http://localhost:9999/cases.json", timeout=5)
    data3 = resp3.read().decode("utf-8")
    try:
        parsed3 = json.loads(data3)
        print(f"HTTP {resp3.status}, valid JSON")
    except json.JSONDecodeError as e:
        print(f"HTTP {resp3.status}, INVALID JSON: {e}")
        lines = data3.split('\n')
        err_line = int(str(e).split('line')[1].split()[0]) if 'line' in str(e) else 1
        start = max(0, err_line-3)
        end = min(len(lines), err_line+3)
        for li in range(start, end):
            marker = ">>>" if li == err_line-1 else "   "
            print(f"{marker} L{li+1}: {lines[li][:120]}")
except Exception as e:
    print(f"FAILED: {e}")

# Now open browser
print("\n=== Opening Browser ===")
import webbrowser
webbrowser.open("http://localhost:9999/")
print("Browser opened to http://localhost:9999/")
