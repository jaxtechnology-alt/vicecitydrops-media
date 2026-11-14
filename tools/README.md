# Free fallback video pipeline (no vidIQ credits needed)

Used by the daily "Vice City Drops daily content" task when vidIQ credits run out.

1. Render a 1080x1920 vertical Short locally:
   `python3 tools/make_countdown.py tools/cfg/<name>.json` (see cfg/*.json for the scene/text format; needs Pillow + ffmpeg, font Poppins-Bold at /usr/share/fonts/truetype/google-fonts/ — fall back to DejaVuSans-Bold if missing).
2. Copy the mp4 into `videos/YYYY-MM-DD_<slug>.mp4`, commit and push to `main`.
3. Use the public URL in Metricool `media`:
   `https://raw.githubusercontent.com/jaxtechnology-alt/vicecitydrops-media/main/videos/<file>.mp4`
   (verified 14 Nov 2026: Metricool copies it to static.metricool.com).

Limits: the cloud environment cannot download stock footage or trailers, so these are graphics-style videos. Prefer vidIQ compose (real footage) whenever credits allow.
