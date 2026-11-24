"""Set privacy on our own YouTube videos (free YouTube Data API, same secrets as yt_comments.py).
Input: yt-actions/*.json = [{"videoId": "...", "privacyStatus": "private|unlisted|public"} or {"videoId": "...", "appendDescription": "text"}]. Log: yt-actions/done.json"""
import json, os, glob, sys
sys.path.insert(0, os.path.dirname(__file__))
from yt_comments import token, call
tok = token(); log = json.load(open("yt-actions/done.json")) if os.path.exists("yt-actions/done.json") else []
for f in sorted(glob.glob("yt-actions/*.json")):
    if f.endswith("done.json"): continue
    for it in json.load(open(f)):
        try:
            if it.get("appendDescription"):
                v = call(tok, "GET", "videos", {"part": "snippet", "id": it["videoId"]})["items"][0]["snippet"]
                if it["appendDescription"] not in v.get("description", ""):
                    body = {"id": it["videoId"], "snippet": {"title": v["title"], "categoryId": v["categoryId"], "tags": v.get("tags", []),
                            "description": v.get("description", "") + "\n\n" + it["appendDescription"]}}
                    call(tok, "PUT", "videos", {"part": "snippet"}, body)
                log.append({**it, "ok": True}); print("OK desc", it["videoId"])
                if "privacyStatus" not in it: continue
            r = call(tok, "PUT", "videos", {"part": "status"}, {"id": it["videoId"], "status": {"privacyStatus": it["privacyStatus"], "selfDeclaredMadeForKids": False}})
            log.append({**it, "ok": True, "now": r["status"]["privacyStatus"]}); print("OK", it)
        except Exception as e:
            body = getattr(e, "read", lambda: b"")().decode()[:300]
            log.append({**it, "ok": False, "error": str(e) + " " + body}); print("FAIL", it, e, body)
    os.remove(f)
json.dump(log, open("yt-actions/done.json", "w"), indent=1)
