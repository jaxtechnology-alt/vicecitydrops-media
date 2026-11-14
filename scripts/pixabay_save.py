import json, sys, urllib.request
slug = sys.argv[1]
hits = json.load(open('/tmp/r.json')).get('hits', [])[:3]
credits = []
for i, h in enumerate(hits):
    v = h['videos'].get('medium') or h['videos'].get('small')
    if not v or not v.get('url'):
        continue
    out = f"footage/{slug}_{i+1}.mp4"
    urllib.request.urlretrieve(v['url'], out)
    credits.append({"file": out, "user": h.get('user'), "page": h.get('pageURL'),
                    "tags": h.get('tags'), "duration": h.get('duration')})
json.dump(credits, open(f"footage/{slug}.json", "w"), indent=1)
print(slug, len(credits), "clips")
