"""Download NCS (NoCopyrightSounds) tracks for our Shorts. Usage: python3 scripts/ncs_fetch.py <requests file>
Each line: a search term or an ncs.io track URL. Saves music/ncs_<slug>.mp3 + .json with the official credit text.
NCS policy: free for independent creators on YouTube/IG/TikTok/FB incl. monetised; Shorts/Reels/TikTok need no credit,
long videos need the credit in the description (we add it anyway). Never upload the music on its own."""
import re, sys, json, os, urllib.request, urllib.parse, html
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
def get(u): return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()
os.makedirs("music", exist_ok=True)
for line in open(sys.argv[1]):
    q = line.strip()
    if not q: continue
    try:
        if q.startswith("http"): page_url = q
        else:
            s = get("https://ncs.io/music-search?q=" + urllib.parse.quote(q)).decode("utf8", "ignore")
            links = re.findall(r'href="(/[A-Za-z0-9_\-]+)"[^>]*>\s*<img', s) or re.findall(r'data-url="([^"]+)"', s)
            m = re.search(r'data-url="(https?://[^"]+\.mp3[^"]*)"[^>]*data-track="([^"]*)"[^>]*data-artistraw="([^"]*)"', s)
            print("SEARCH", q, "links:", links[:5], "player:", m.groups() if m else None)
            page_url = "https://ncs.io" + links[0] if links and links[0].startswith("/") else None
        mp3 = title = None
        if page_url:
            p = get(page_url).decode("utf8", "ignore")
            cands = re.findall(r'https?://[^"\' ]+\.mp3[^"\' ]*', p) + ["https://ncs.io" + x for x in re.findall(r'href="(/track/download/[^"]+)"', p)]
            print("PAGE", page_url, "mp3 candidates:", cands[:4])
            t = re.search(r'<title>([^<]+)</title>', p); title = html.unescape(t.group(1)).strip() if t else q
            mp3 = cands[-1] if any("/track/download/" in c for c in cands) else (cands[0] if cands else None)
        if not mp3 and not q.startswith("http") and m: mp3, title = m.group(1), f"{m.group(3)} - {m.group(2)}"
        if not mp3: print("FAILED no mp3 for", q); continue
        slug = "ncs_" + re.sub(r'[^a-z0-9]+', '_', (page_url or q).rstrip('/').split('/')[-1].lower()).strip('_')
        data = get(mp3)
        if len(data) < 200000: print("FAILED too small", q, len(data)); continue
        open(f"music/{slug}.mp3", "wb").write(data)
        credit = f"Song: {title.replace(' | NCS', '').replace(' - NCS', '')} [NCS Release] | Music provided by NoCopyrightSounds | Free Download/Stream: {page_url or 'https://ncs.io'}"
        json.dump({"title": title, "source": mp3, "page": page_url, "license": "NCS usage policy (free for creators, credit)", "credit": credit}, open(f"music/{slug}.json", "w"))
        print("OK", slug, len(data))
    except Exception as e:
        print("FAILED", q, e)
