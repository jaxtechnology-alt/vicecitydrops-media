"""Turn a day's carousel slides into a 9:16 Reel (1080x1920 MP4).

Usage: python3 reel.py 2026-11-24 [music/mixkit_xxx.mp3]
Reads out/<date>-N.jpg, writes out/<date>-reel.mp4.
Music: Mixkit Stock Music Free License (commercial use OK, no credit needed).
"""
import glob, os, random, subprocess, sys, tempfile
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NAVY, BLUE = (15, 30, 58), (143, 179, 240)
W, H = 1080, 1920
TRACKS = ["mixkit_synthwave_131", "mixkit_synthwave_159", "mixkit_synthwave_173",
          "mixkit_hip-hop_224", "mixkit_hip-hop_235", "mixkit_hip-hop_257"]


def font(size, bold=True):
    for p in ["/usr/share/fonts/opentype/inter/Inter-Bold.otf" if bold else "/usr/share/fonts/opentype/inter/Inter-Regular.otf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def frame(slide_path, out_path):
    bg = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(bg)
    logo = Image.open(os.path.join(HERE, "assets/logo.jpg")).convert("RGB").resize((96, 96))
    bg.paste(logo, (90, 150))
    d.text((210, 160), "JAX TECH", font=font(52), fill="white")
    d.text((210, 220), "Business VoIP · crystal-clear calls", font=font(30, False), fill=BLUE)
    s = Image.open(slide_path).convert("RGB").resize((1000, 1250))
    bg.paste(s, (40, 300))
    msg = "021 002 5637  ·  jaxtech.co.za"
    tw = d.textlength(msg, font=font(44))
    d.rounded_rectangle([(W - tw) / 2 - 40, 1610, (W + tw) / 2 + 40, 1710], radius=50, fill=BLUE)
    d.text(((W - tw) / 2, 1630), msg, font=font(44), fill=NAVY)
    bg.save(out_path, quality=95)


def main():
    date = sys.argv[1]
    slides = sorted(glob.glob(os.path.join(HERE, f"out/{date}-[0-9]*.jpg")),
                    key=lambda p: int(p.rsplit("-", 1)[1].split(".")[0]))
    if len(slides) < 2:
        sys.exit("need at least 2 slides")
    track = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "music", random.choice(TRACKS) + ".mp3")
    tmp = tempfile.mkdtemp()
    durs = [3.2] + [2.8] * (len(slides) - 2) + [3.6]
    inputs, fparts = [], []
    for i, (sp, du) in enumerate(zip(slides, durs)):
        fp = os.path.join(tmp, f"f{i}.jpg"); frame(sp, fp)
        inputs += ["-loop", "1", "-t", str(du + 0.4), "-i", fp]
        # gentle push-in on each slide
        fparts.append(f"[{i}:v]scale=1188:2112,zoompan=z='min(zoom+0.0009,1.06)':d={int((du+0.4)*30)}:"
                      f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps=30,setsar=1,format=yuv420p[v{i}]")
    chain, last, off = [], "v0", 0.0
    for i in range(1, len(slides)):
        off += durs[i - 1]
        out = f"x{i}"
        chain.append(f"[{last}][v{i}]xfade=transition=slideleft:duration=0.4:offset={off:.2f}[{out}]")
        last = out
    total = sum(durs)
    a = len(slides)
    filt = ";".join(fparts + chain) + f";[{a}:a]atrim=0:{total},afade=t=in:d=0.5,afade=t=out:st={total-1.2}:d=1.2,volume=0.8[a]"
    out = os.path.join(HERE, f"out/{date}-reel.mp4")
    cmd = ["ffmpeg", "-y", *inputs, "-ss", "8", "-i", track, "-filter_complex", filt,
           "-map", f"[{last}]", "-map", "[a]", "-t", f"{total:.2f}", "-c:v", "libx264", "-preset", "veryfast",
           "-crf", "21", "-pix_fmt", "yuv420p", "-r", "30", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True, capture_output=True)
    print(out, os.path.basename(track))


if __name__ == "__main__":
    main()
