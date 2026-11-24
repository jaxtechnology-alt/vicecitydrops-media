"""Set privacy on our own YouTube videos (free YouTube Data API, same secrets as yt_comments.py).
Input: yt-actions/*.json = [{"videoId": "...", "privacyStatus": "private|unlisted|public"}]. Log: yt-actions/done.json"""
import json, os, glob, sys
sys.path.insert(0, os.path.dirname(__file__))
from yt_comments import token, call
tok = token(); log = json.load(open("yt-actions/done.json")) if os.path.exists("yt-actions/done.json") else []
for f in sorted(glob.glob("yt-actions/*.json")):
    if f.endswith("done.json"): continue
    for it in json.load(open(f)):
        try:
            r = call(tok, "PUT", "videos", {"part": "status"}, {"id": it["videoId"], "status": {"privacyStatus": it["privacyStatus"], "selfDeclaredMadeForKids": False}})
            log.append({**it, "ok": True, "now": r["status"]["privacyStatus"]}); print("OK", it)
        except Exception as e:
            body = getattr(e, "read", lambda: b"")().decode()[:300]
            log.append({**it, "ok": False, "error": str(e) + " " + body}); print("FAIL", it, e, body)
    os.remove(f)
json.dump(log, open("yt-actions/done.json", "w"), indent=1)
