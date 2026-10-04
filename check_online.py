import urllib.request

url = "https://wyjing333-dev.github.io/promptblocks/index.html"
req = urllib.request.Request(url, headers={"Cache-Control": "no-cache"})
content = urllib.request.urlopen(req).read().decode("utf-8")
lines = content.split("\n")

keywords = ["getRegistrations", "unregister", "fetch('blocks.json')", "loadData(fullInit)", "v2"]
for i, line in enumerate(lines):
    for kw in keywords:
        if kw in line:
            print(f"L{i+1}: {line.strip()[:100]}")

print(f"\nTotal lines: {len(lines)}")
print(f"Has getRegistrations: {'getRegistrations' in content}")
print(f"Has unregister: {'unregister' in content}")
