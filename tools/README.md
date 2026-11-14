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
