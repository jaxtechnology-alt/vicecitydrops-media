#!/usr/bin/env python3
"""Render a Jax Tech carousel from a JSON post spec.

Usage: python3 render.py posts/2026-11-25.json   -> out/2026-11-25-1.png ... (1080x1350)

Spec:
{
  "date": "2026-11-25",
  "slides": [
    {"type": "cover", "kicker": "BUSINESS PHONES", "title": "Your landline is <em>dying</em>.", "sub": "Here's what to do before it goes quiet.", "photo": "desk-call"},
    {"type": "point", "n": 1, "title": "Short heading", "body": "One or two short sentences."},
    {"type": "stat", "big": "67%", "title": "of callers hang up...", "body": "source line"},
    {"type": "cta", "title": "Want us to check your phone bill?", "body": "Free, no obligation."}
  ],
  "caption": "...", "hashtags": [...]
}
Photos: any file name (without .jpg) in assets/. <em>...</em> highlights words in blue.
"""
import json, sys, pathlib, html as H
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent
NAVY, BLUE, GREEN, INK, PAPER = "#0F1E3A", "#8FB3F0", "#6FCF97", "#0F1E3A", "#F3F6FB"
PHONE, SITE = "021 002 5637", "jaxtech.co.za"

CSS = f"""
*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1080px;height:1350px;font-family:Inter,'Inter Display',Arial,sans-serif;overflow:hidden}}
.s{{width:1080px;height:1350px;position:relative;display:flex;flex-direction:column;justify-content:center;padding:170px 90px 150px}}
.brand{{position:absolute;top:80px;left:90px}}
.dark{{background:{NAVY};color:#fff}} .light{{background:{PAPER};color:{INK}}}
.brand{{display:flex;align-items:center;gap:18px;font-weight:800;font-size:34px;letter-spacing:.08em}}
.brand img{{width:72px;height:72px;border-radius:16px}}
.kicker{{font-weight:700;font-size:32px;letter-spacing:.14em;color:{BLUE}}}
h1{{font-family:'Inter Display',Inter,Arial,sans-serif;font-weight:800;font-size:118px;line-height:1.02;margin-top:26px;letter-spacing:-.02em}}
h1 em,h2 em{{font-style:normal;color:{BLUE}}} .light h2 em{{color:#2F5FB8}}
.sub{{font-size:40px;line-height:1.3;margin-top:36px;color:#C9D4E8}}
.photo{{position:absolute;left:0;right:0;bottom:0;height:520px;background-size:cover;background-position:center}}
.photo:after{{content:'';position:absolute;inset:0;background:linear-gradient({NAVY} 0%,rgba(15,30,58,0) 45%)}}
.swipe{{position:absolute;right:90px;bottom:60px;z-index:2;font-weight:700;font-size:30px;background:{BLUE};color:{NAVY};padding:16px 28px;border-radius:40px}}
.n{{font-family:'Inter Display',Inter;font-weight:800;font-size:180px;line-height:1;color:{BLUE};opacity:.9;margin-top:0}}
.light .n{{color:#2F5FB8}}
h2{{font-family:'Inter Display',Inter,Arial;font-weight:800;font-size:92px;line-height:1.06;margin-top:30px;letter-spacing:-.01em}}
.body{{font-size:48px;line-height:1.4;margin-top:40px;color:inherit;opacity:.88}}
.big{{font-family:'Inter Display',Inter;font-weight:800;font-size:230px;line-height:1;color:{BLUE}}}
.foot{{position:absolute;left:90px;right:90px;bottom:64px;display:flex;justify-content:space-between;font-size:28px;opacity:.7;font-weight:600}}
.cta-box{{margin-top:70px;background:rgba(143,179,240,.12);border:2px solid {BLUE};border-radius:28px;padding:44px}}
.cta-line{{font-size:46px;font-weight:800;margin-top:10px}} .cta-line span{{color:{BLUE}}}
"""

import base64
def _data(p):
    return "data:image/jpeg;base64," + base64.b64encode(p.read_bytes()).decode()

def logo():
    return _data(ROOT / "assets" / "logo.jpg")

def photo(name):
    p = ROOT / "assets" / f"{name}.jpg"
    return _data(p) if p.exists() else None

def esc(t):  # allow <em> only
    return H.escape(t or "").replace("&lt;em&gt;", "<em>").replace("&lt;/em&gt;", "</em>")

def slide_html(s, i, total):
    t = s["type"]
    brand = f'<div class="brand"><img src="{logo()}">JAX TECH</div>'
    foot = f'<div class="foot"><span>{SITE}</span><span>{i}/{total}</span></div>'
    if t == "cover":
        ph = photo(s.get("photo", "")) if s.get("photo") else None
        phd = f'<div class="photo" style="background-image:url({ph})"></div>' if ph else ""
        return f'<div class="s dark" style="justify-content:flex-start;padding-top:230px">{brand}<div class="kicker">{esc(s.get("kicker",""))}</div><h1>{esc(s["title"])}</h1><div class="sub">{esc(s.get("sub",""))}</div>{phd}<div class="swipe">Swipe →</div></div>'
    if t == "point":
        theme = "light" if i % 2 == 0 else "dark"
        return f'<div class="s {theme}">{brand}<div class="n">{s.get("n","")}</div><h2>{esc(s["title"])}</h2><div class="body">{esc(s.get("body",""))}</div>{foot}</div>'
    if t == "stat":
        return f'<div class="s dark">{brand}<div class="big">{esc(s["big"])}</div><h2>{esc(s["title"])}</h2><div class="body">{esc(s.get("body",""))}</div>{foot}</div>'
    if t == "cta":
        return (f'<div class="s dark">{brand}<h2>{esc(s["title"])}</h2><div class="body">{esc(s.get("body",""))}</div>'
                f'<div class="cta-box"><div style="font-size:30px;letter-spacing:.12em;color:{BLUE};font-weight:700">TALK TO US</div>'
                f'<div class="cta-line">Call <span>{PHONE}</span></div><div class="cta-line">WhatsApp us or visit <span>{SITE}</span></div></div></div>')
    raise ValueError(f"unknown slide type {t}")

def render(spec_path):
    spec = json.loads(pathlib.Path(spec_path).read_text())
    slides = spec["slides"]
    out = ROOT / "out"; out.mkdir(exist_ok=True)
    files = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350})
        for i, s in enumerate(slides, 1):
            pg.set_content(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{slide_html(s, i, len(slides))}</body></html>", wait_until="load")
            pg.wait_for_timeout(200)
            f = out / f"{spec['date']}-{i}.jpg"
            pg.screenshot(path=str(f), type="jpeg", quality=92)
            files.append(str(f))
        b.close()
    print("\n".join(files))

if __name__ == "__main__":
    render(sys.argv[1])
