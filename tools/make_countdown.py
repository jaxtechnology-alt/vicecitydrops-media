import math, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, DUR = 1080, 1920, 30, 10.0
N = int(FPS * DUR)
BOLD = "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf"
INTER = "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf"

def lerp(a, b, t): return a + (b - a) * t
def ease(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3
def mix(c1, c2, t): return tuple(int(lerp(a, b, t)) for a, b in zip(c1, c2))

def background():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    top, mid, low = (18, 8, 48), (196, 40, 120), (255, 150, 60)
    horizon = 1180
    for y in range(H):
        if y < horizon:
            t = y / horizon
            c = mix(top, mid, t / 0.7) if t < 0.7 else mix(mid, low, (t - 0.7) / 0.3)
        else:
            t = (y - horizon) / (H - horizon)
            c = mix((40, 12, 70), (8, 4, 20), t)
        d.line([(0, y), (W, y)], fill=c)
    # sun with retro stripes
    sun = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sun)
    cx, cy, r = W // 2, 1040, 330
    for y in range(cy - r, horizon):
        dy = y - cy
        if abs(dy) > r: continue
        half = int(math.sqrt(r * r - dy * dy))
        t = (y - (cy - r)) / (2 * r)
        col = mix((255, 230, 120), (255, 60, 140), t)
        gap = y > cy - 40 and ((y - cy) // 14) % 3 == 0
        if not gap:
            sd.line([(cx - half, y), (cx + half, y)], fill=col + (255,))
    glow = sun.filter(ImageFilter.GaussianBlur(60))
    img.paste(glow, (0, 0), glow)
    img.paste(sun, (0, 0), sun)
    # perspective grid on the "sea"
    d = ImageDraw.Draw(img)
    for i in range(-14, 15):
        d.line([(W // 2 + i * 40, horizon), (W // 2 + i * 260, H)], fill=(255, 70, 170), width=2)
    y, step = horizon, 8
    while y < H:
        d.line([(0, y), (W, y)], fill=(255, 70, 170), width=2)
        step *= 1.25; y += int(step)
    # palm silhouettes
    def palm(x0, base, height, lean, scale):
        pts = []
        for i in range(31):
            t = i / 30
            pts.append((x0 + lean * t * t, base - height * t))
        for i in range(len(pts) - 1):
            w = int(lerp(34, 16, i / 30) * scale)
            d.line([pts[i], pts[i + 1]], fill=(14, 4, 26), width=w)
        tx, ty = pts[-1]
        for a in range(0, 360, 40):
            ang = math.radians(a + 10)
            L = 230 * scale
            ex, ey = tx + math.cos(ang) * L, ty + math.sin(ang) * L * 0.55 + 60 * scale
            mx, my = tx + math.cos(ang) * L * 0.5, ty + math.sin(ang) * L * 0.3 - 30 * scale
            perp = (-math.sin(ang) * 22 * scale, math.cos(ang) * 22 * scale)
            d.polygon([(tx, ty), (mx + perp[0], my + perp[1]), (ex, ey), (mx - perp[0], my - perp[1])], fill=(14, 4, 26))
    palm(120, H + 40, 1300, 140, 1.1)
    palm(990, H + 40, 1100, -160, 0.95)
    palm(860, H + 40, 760, -60, 0.7)
    # vignette
    v = Image.new("L", (W, H), 0)
    ImageDraw.Draw(v).ellipse([-300, -200, W + 300, H + 200], fill=255)
    v = v.filter(ImageFilter.GaussianBlur(200))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    return Image.composite(img, dark, v)

BG = background()

def text_layer(lines, alpha, scale=1.0, y_shift=0):
    """lines: list of (text, font_path, size, color, y)"""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld, gd = ImageDraw.Draw(layer), ImageDraw.Draw(glow)
    for text, fp, size, color, y, has_glow in lines:
        f = ImageFont.truetype(fp, int(size * scale))
        bw = ld.textlength(text, font=f)
        x = (W - bw) / 2
        yy = y + y_shift
        ld.text((x + 6, yy + 8), text, font=f, fill=(0, 0, 0, 150))
        ld.text((x, yy), text, font=f, fill=color + (255,))
        if has_glow:
            gd.text((x, yy), text, font=f, fill=color + (255,))
    glow = glow.filter(ImageFilter.GaussianBlur(28))
    out = Image.alpha_composite(glow, layer)
    if alpha < 1:
        a = out.split()[3].point(lambda p: int(p * alpha))
        out.putalpha(a)
    return out

PINK, CYAN, WHITE, GOLD = (255, 60, 170), (60, 240, 255), (255, 255, 255), (255, 214, 90)

def frame(i):
    t = i / FPS
    img = BG.copy().convert("RGBA")
    # slow push-in on background
    z = 1 + 0.06 * (t / DUR)
    bw, bh = int(W * z), int(H * z)
    img = img.resize((bw, bh), Image.BICUBIC).crop(((bw - W) // 2, (bh - H) // 2, (bw - W) // 2 + W, (bh - H) // 2 + H))
    S1, S2, S3 = SCENES
    if t < 3.4:
        k = ease(t / 0.5); out = 1 - ease((t - 3.0) / 0.4)
        pulse = 1 + 0.04 * math.sin(t * 6)
        img = Image.alpha_composite(img, text_layer(S1, min(k, out), scale=lerp(1.25, 1, k) * pulse))
    elif t < 6.8:
        lt = t - 3.4; k = ease(lt / 0.5); out = 1 - ease((lt - 3.0) / 0.4)
        img = Image.alpha_composite(img, text_layer(S2, min(k, out), y_shift=int(lerp(80, 0, k))))
    else:
        lt = t - 6.8; k = ease(lt / 0.5)
        img = Image.alpha_composite(img, text_layer(S3, k, y_shift=int(lerp(80, 0, k))))
        k2 = ease((lt - 1.2) / 0.5)
        if k2 > 0:
            img = Image.alpha_composite(img, text_layer([("FOLLOW FOR LAUNCH-WEEK DROPS", INTER, 50, GOLD, 1680, True)], k2))
    # fade from/to black
    fade = min(ease(t / 0.3), 1 - ease((t - (DUR - 0.4)) / 0.4)) if t > DUR - 0.4 else ease(t / 0.3)
    if fade < 1:
        img = Image.blend(Image.new("RGBA", (W, H), (0, 0, 0, 255)), img, fade)
    return img.convert("RGB")

import json
if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1]))
    G = {"BOLD": BOLD, "INTER": INTER, "PINK": PINK, "CYAN": CYAN, "WHITE": WHITE, "GOLD": GOLD, "GREEN": (120,255,150), "RED": (255,90,110)}
    SCENES = [[(t, G[f], sz, G[c], y, gl) for t, f, sz, c, y, gl in sc] for sc in cfg["scenes"]]
    name = cfg["name"]
    if len(sys.argv) > 2:
        for s_ in [1.5, 5.0, 9.0]:
            frame(int(s_ * FPS)).save(f"/home/claude/reel/prev_{name}_{s_}.jpg", quality=85)
        sys.exit()
    out = f"/home/claude/reel/{name}.silent.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", "-pix_fmt", "yuv420p", out],
                         stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    for i in range(N):
        p.stdin.write(frame(i).tobytes())
    p.stdin.close(); sys.exit(p.wait())
