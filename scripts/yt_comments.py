"""YouTube comment helper for GitHub Actions (free YouTube Data API).
fetch: list recent comment threads on the channel -> comments/youtube.json (1 quota unit per call)
post:  post replies from replies/*.json [{"parentId": "...", "text": "..."}] (50 units each), log to replies/done.json
Secrets used (set by Rudi, never stored in the repo): YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN.
"""
import json, os, sys, glob, urllib.request, urllib.parse
CHANNEL = "UCpe0qLGvJgkxnV84NvU3KpA"
API = "https://www.googleapis.com/youtube/v3"

def token():
    data = urllib.parse.urlencode({"client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    return json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", data))["access_token"]

def call(tok, method, path, params=None, body=None):
    url = f"{API}/{path}?" + urllib.parse.urlencode(params or {})
    req = urllib.request.Request(url, method=method, headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"},
                                 data=json.dumps(body).encode() if body else None)
    return json.load(urllib.request.urlopen(req))

def fetch(tok):
    r = call(tok, "GET", "commentThreads", {"part": "snippet,replies", "allThreadsRelatedToChannelId": CHANNEL,
                                             "maxResults": 100, "order": "time"})
    out = []
    for t in r.get("items", []):
        s = t["snippet"]; top = s["topLevelComment"]["snippet"]
        replies = [c["snippet"] for c in t.get("replies", {}).get("comments", [])]
        out.append({"threadId": t["id"], "videoId": s.get("videoId"), "author": top.get("authorDisplayName"),
                    "text": top.get("textOriginal"), "published": top.get("publishedAt"), "likes": top.get("likeCount"),
                    "weReplied": any(c.get("authorChannelId", {}).get("value") == CHANNEL for c in replies)})
    json.dump(out, open("comments/youtube.json", "w"), indent=1, ensure_ascii=False)
    print(len(out), "threads")

def post(tok):
    done = json.load(open("replies/done.json")) if os.path.exists("replies/done.json") else []
    seen = {d["parentId"] for d in done}
    for f in sorted(glob.glob("replies/queue*.json")):
        for item in json.load(open(f)):
            if item["parentId"] in seen:
                continue
            try:
                call(tok, "POST", "comments", {"part": "snippet"}, {"snippet": {"parentId": item["parentId"], "textOriginal": item["text"]}})
                done.append({**item, "status": "posted"})
            except Exception as e:
                done.append({**item, "status": f"error: {e}"})
            seen.add(item["parentId"])
        os.remove(f)
    json.dump(done, open("replies/done.json", "w"), indent=1, ensure_ascii=False)

if __name__ == "__main__":
    if not all(os.environ.get(k) for k in ("YT_CLIENT_ID","YT_CLIENT_SECRET","YT_REFRESH_TOKEN")):
        print("YouTube secrets not set yet; skipping"); sys.exit(0)
    t = token()
    {"fetch": fetch, "post": post}[sys.argv[1]](t)
