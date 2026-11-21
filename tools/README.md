# Free video pipeline (no vidIQ credits needed) — tested 14 Nov 2026

Reachable from Claude's cloud environment (Rudi allow-listed them): storage.googleapis.com, videos.pexels.com,
api.pexels.com, ai-music-tracks.s3.us-east-1.amazonaws.com, raw.githubusercontent.com / github.com.

## 1. Real-world stock footage (Pixabay, free, key stays in GitHub secret PIXABAY_API_KEY)
Push `requests/<name>.txt` (one search term per line, NEW filename each time). The `fetch-footage` GitHub Action
downloads 3 clips per term into `footage/<term_slug>_N.mp4` plus `footage/<term_slug>.json` (credits: user + page).
Wait ~60-90 s, `git pull`. Clips are 1280x720 landscape; centre-crop to 9:16. Credit Pixabay users in captions.

## 2. Rockstar trailer clips
`vidiq_video_upload` with uploadId 9abda3aa-c5a4-4203-8fd9-a817ce0f0fa2 (free, 0 credits) returns a fresh signed
storage.googleapis.com URL for the Launch Trailer (rz1B4B2yBZY). Download it, then NORMALISE first (its timestamps
are irregular, so seeks land on the wrong shot otherwise):
`ffmpeg -i trailer.mp4 -an -vf fps=30,scale=1920:-2 -c:v libx264 -preset veryfast -crf 18 clean.mp4`
Scene cuts in clean.mp4 (seconds): 2.0 | 6.3 | 9.3 | 11.23 | 13.53 | 14.5 | 20.5 | 25.7 | 27.17 | 28.73 | 32.13.
Verified safe shots (no guns): 0.5-1.9 "The Keys" sign; 3.0-6.2 marina aerial; 13.58-14.43 seaplane/water;
24.6-25.6 sunset skyline (faint logo); 25.78-27.1 Jason & Lucia in car. Avoid 19-21 and 27.2-29 (weapons).
Always check frames (ffmpeg -ss T -i file -frames:v 1) of the final render before posting. Max ~6 s Rockstar footage.

## 3. Render
Text cards: `tools/text_cards.py` (PIL, Poppins-Bold, colours #ff3caa #3cf0ff #ffd65a, outline #120830).
Per scene: `ffmpeg -ss S -t D -i clip -i card.png -filter_complex "[0:v]scale=-2:1920,crop=1080:1920,setsar=1,fps=30[b];[b][1:v]overlay=0:0,format=yuv420p" -an -c:v libx264 -preset veryfast -crf 19 sN.mp4`
Concat (`-f concat -c copy`), add music (download the .wav, `-ss 0..45`, afade in/out, `-shortest`).

## 4. Publish
Copy to `videos/YYYY-MM-DD_<slug>.mp4`, commit, push, then use
`https://raw.githubusercontent.com/jaxtechnology-alt/vicecitydrops-media/main/videos/<file>.mp4` as Metricool media.

Example: videos/2026-11-14_people-on-19-november.mp4 (Pixabay traffic/crowd/office -> trailer shots).

## 5. Keep footage fresh (free) — do this when a run has time, at least twice a week
Clips from only one trailer get repetitive. Import other OFFICIAL Rockstar trailers with `vidiq_video_upload`
(url = YouTube link; free, 0 credits; poll vidiq_job_poll): Trailer 2 https://www.youtube.com/watch?v=VQRLujxTm3c ,
Trailer 1 https://www.youtube.com/watch?v=QdBZY2fkU-0 . Download the returned videoUrl, normalise, run scene
detection (`ffmpeg -i clean.mp4 -vf "select='gt(scene,0.25)',showinfo" -an -f null - 2>&1 | grep -o "pts_time:[0-9.]*"`),
look at a frame from the middle of each shot, and ADD the uploadId plus the safe shot windows (no weapons, no story
spoilers) to section 2 above, then commit. Also save the uploadIds here so later runs can refresh the URLs.

## 6. Strategy
Read STRATEGY.md at the start of every run; the weekly review task keeps it up to date.

## 7. YouTube comment replies (free, YouTube Data API via GitHub Actions)
The `youtube-comments` workflow refreshes `comments/youtube.json` every 3 hours (fields: threadId, videoId, author,
text, published, likes, weReplied). To reply: `git pull`, pick threads with weReplied=false that are genuine,
write `replies/queue-YYYYMMDD-HHMM.json` = [{"parentId": "<threadId>", "text": "<reply>"}], commit, push.
The workflow posts each once and logs results in `replies/done.json` (never re-queue a parentId listed there).
Quota: ~198 replies/day max; keep it under 30 per run. To refresh comments immediately, push any queue file
(even `[]`). Secrets YT_CLIENT_ID / YT_CLIENT_SECRET / YT_REFRESH_TOKEN live only in GitHub.

## 8. Still manual / next free automations (weekly review 15 Nov 2026)
- vidIQ credits are 0 until 14 Dec; vidiq_video_upload (0 credits) still works, so footage rotation (section 5) stays free.
- Instagram + Facebook comment replies: free via Meta Graph API in a GitHub Action (same pattern as section 7) once a
  Page access token is stored as a GitHub secret. Needs Rudi to create a free Meta developer app; not done yet.
- TikTok comment replies: no free official API for this; leave manual.
- Own gameplay clips after launch would be the biggest originality win (Rudi recording on console); upload to footage/rudi/.

## 9. Music (choose per Short — added 21 Nov, Rudi: "include music as you decide")
Pick the track by mood, don't reuse the same track on consecutive Shorts:
- AI track (no credit needed): https://ai-music-tracks.s3.us-east-1.amazonaws.com/e681871f-2c0f-45cf-8a4b-7a09b3a14df0/fd2ea989-63f8-4af2-9615-3d89732ab881.wav (vary start 0-45 s).
- Kevin MacLeod tracks in `music/*.mp3` (CC BY 4.0, fetched by the `fetch-music` Action: push `music-requests/<new>.txt`
  with exact incompetech titles). MUST add the credit line from `music/<slug>.json` to the caption.
  Mood guide: sneaky/funny POV = Sneaky Snitch, Investigations; silly memes = Monkeys Spinning Monkeys, Fluffing a Duck,
  Pixel Peeker Polka; news/facts/tension = Cipher, Volatile Reaction, Hitman, Run Amok; deadpan "waiting" jokes = Local Forecast - Elevator.
- Trending sounds (e.g. "Suzuki") can't be added through Metricool or legally ripped: use our own track; note in the report
  that Rudi may swap the TikTok/IG sound by hand in-app if he wants the trend.
Mix music at about -14 dB under nothing (no voiceover), fade in 0.3 s and out 0.5 s.
