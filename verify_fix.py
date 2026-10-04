import urllib.request, json, re

# Verify the fix
print("=== Verifying fix ===")
resp = urllib.request.urlopen("http://localhost:9999/", timeout=5)
html = resp.read().decode("utf-8")
print(f"index.html: HTTP {resp.status}, {len(html)} bytes")

# Check platName is now defined
if "function platName" in html:
    print("platName function: DEFINED ✓")
else:
    print("platName function: NOT FOUND ✗")

# Check platName usage still exists
usage_count = html.count("platName(p)")
print(f"platName(p) usage: {usage_count} occurrences")

# Check brackets still match
opens = html.count('{')
closes = html.count('}')
print(f"Curly braces: {opens} open / {closes} close = {'OK' if opens==closes else 'MISMATCH'}")

# Now open browser
import webbrowser
webbrowser.open("http://localhost:9999/")
print("\nBrowser opened to http://localhost:9999/")
print("Please check if the page loads correctly now!")
