import urllib.request, json

for fname in ["blocks.json", "cases.json", "manifest.json", "sw.js"]:
    url = f"https://wyjing333-dev.github.io/promptblocks/{fname}"
    try:
        req = urllib.request.Request(url, headers={"Cache-Control": "no-cache"})
        resp = urllib.request.urlopen(req, timeout=10)
        data = resp.read()
        status = resp.status
        if fname.endswith(".json"):
            try:
                parsed = json.loads(data)
                keys = list(parsed.keys()) if isinstance(parsed, dict) else "array"
                print(f"{fname}: HTTP {status}, valid JSON, keys={keys}")
            except json.JSONDecodeError as e:
                print(f"{fname}: HTTP {status}, INVALID JSON: {e}")
        else:
            print(f"{fname}: HTTP {status}, {len(data)} bytes")
    except Exception as e:
        print(f"{fname}: FAILED - {e}")
