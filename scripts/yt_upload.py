"""Upload Shorts to our YouTube channel (free YouTube Data API, ~1600 quota units each, ~6/day max).
Input: yt-uploads/*.json = [{"file": "videos/x.mp4", "title": "...", "description": "...", "tags": [...],
  "publishAt": "2026-11-24T14:00:00Z" (optional; uploads private and YouTube makes it public then)}]
Log: yt-uploads/done.json (never re-queue a file listed there)."""
import json, os, glob, sys, uuid, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
from yt_comments import token
tok = token(); log = json.load(open("yt-uploads/done.json")) if os.path.exists("yt-uploads/done.json") else []
done = {d["file"] for d in log if d.get("ok")}
for f in sorted(glob.glob("yt-uploads/*.json")):
    if f.endswith("done.json"): continue
    for it in json.load(open(f)):
        if it["file"] in done: print("SKIP already uploaded", it["file"]); continue
        status = {"privacyStatus": "private" if it.get("publishAt") else "public", "selfDeclaredMadeForKids": False}
        if it.get("publishAt"): status["publishAt"] = it["publishAt"]
        meta = {"snippet": {"title": it["title"], "description": it.get("description", ""), "tags": it.get("tags", []), "categoryId": "20"}, "status": status}
        b = uuid.uuid4().hex
        body = (f"--{b}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n{json.dumps(meta)}\r\n--{b}\r\nContent-Type: video/mp4\r\n\r\n").encode() \
               + open(it["file"], "rb").read() + f"\r\n--{b}--\r\n".encode()
        req = urllib.request.Request("https://www.googleapis.com/upload/youtube/v3/videos?uploadType=multipart&part=snippet,status",
              data=body, method="POST", headers={"Authorization": f"Bearer {tok}", "Content-Type": f"multipart/related; boundary={b}"})
        try:
            r = json.load(urllib.request.urlopen(req, timeout=300))
            log.append({"file": it["file"], "ok": True, "videoId": r["id"], "url": f"https://www.youtube.com/shorts/{r['id']}", "status": r["status"]}); print("OK", it["file"], r["id"])
        except Exception as e:
            body = getattr(e, "read", lambda: b"")().decode()[:400]
            log.append({"file": it["file"], "ok": False, "error": f"{e} {body}"}); print("FAIL", it["file"], e, body)
    os.remove(f)
json.dump(log, open("yt-uploads/done.json", "w"), indent=1)
