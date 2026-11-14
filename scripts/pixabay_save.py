import json, sys, urllib.request
slug = sys.argv[1]
hits = json.load(open('/tmp/r.json')).get('hits', [])[:3]
credits = []
for i, h in enumerate(hits):
    v = h['videos'].get('medium') or h['videos'].get('small')
    if not v or not v.get('url'):
        continue
    out = f"footage/{slug}_{i+1}.mp4"
    req = urllib.request.Request(v['url'], headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36', 'Referer': 'https://pixabay.com/'})
    with urllib.request.urlopen(req) as r, open(out, 'wb') as fh:
        fh.write(r.read())
    credits.append({"file": out, "user": h.get('user'), "page": h.get('pageURL'),
                    "tags": h.get('tags'), "duration": h.get('duration')})
json.dump(credits, open(f"footage/{slug}.json", "w"), indent=1)
print(slug, len(credits), "clips")
