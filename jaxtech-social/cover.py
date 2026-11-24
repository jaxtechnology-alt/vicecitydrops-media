"""Render Facebook cover options (1640x624). Key content kept inside the
mobile-safe centre (x 270-1370) and clear of the profile photo (bottom-left)."""
import base64, pathlib, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
A = HERE / "assets"
def d(p): return "data:image/jpeg;base64," + base64.b64encode((A / p).read_bytes()).decode()
NAVY, BLUE, INK = "#0F1E3A", "#8FB3F0", "#0A1630"
LOGO = d("logo.jpg")
BASE = f"""<style>*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1640px;height:624px;overflow:hidden;font-family:Inter,Arial,sans-serif;color:#fff;background:{NAVY}}}
h1{{font-family:'Inter Display',Inter;font-weight:800;letter-spacing:-.025em;line-height:1.02}}
em{{font-style:normal;color:{BLUE}}}
.brand{{display:flex;align-items:center;gap:14px;font-weight:800;font-size:26px;letter-spacing:.12em}}
.brand img{{width:54px;height:54px;border-radius:12px}}
.chip{{display:inline-flex;align-items:baseline;gap:8px;padding:12px 20px;border-radius:14px;background:rgba(143,179,240,.12);border:1px solid rgba(143,179,240,.35);font-size:21px;color:#D6E2F7}}
.chip b{{font-family:'Inter Display';font-size:30px;color:#fff}}
.cta{{font-weight:700;font-size:24px;color:{NAVY};background:{BLUE};padding:14px 26px;border-radius:40px;display:inline-block}}
</style>"""

def phone():
    # CSS phone showing an incoming business call
    return f"""<div style="width:250px;height:500px;border-radius:40px;background:#05080f;padding:12px;box-shadow:0 30px 80px rgba(0,0,0,.55),0 0 0 2px #2a3550">
 <div style="height:100%;border-radius:30px;background:linear-gradient(170deg,#1d3a73,#0b1428 70%);display:flex;flex-direction:column;align-items:center;padding-top:58px">
  <div style="font-size:15px;color:#9fb6de;letter-spacing:.08em">INCOMING · OFFICE LINE</div>
  <div style="font-family:'Inter Display';font-weight:800;font-size:30px;margin-top:14px">021 002 5637</div>
  <div style="font-size:16px;color:#c3d1ea;margin-top:6px">Reception → your cellphone</div>
  <img src="{LOGO}" style="width:86px;height:86px;border-radius:50%;margin-top:40px;border:3px solid {BLUE}">
  <div style="display:flex;gap:70px;margin-top:auto;margin-bottom:56px">
   <div style="width:62px;height:62px;border-radius:50%;background:#e5484d;display:grid;place-items:center;font-size:28px">✕</div>
   <div style="width:62px;height:62px;border-radius:50%;background:#30a46c;display:grid;place-items:center;font-size:28px">✆</div>
  </div></div></div>"""

OPTIONS = {
"A-phone": f"""<body style="background:radial-gradient(900px 520px at 78% 40%,#1E3D7A 0%,{NAVY} 60%,{INK} 100%)">
<div style="position:absolute;left:300px;top:52px;width:720px">
 <div class="brand"><img src="{LOGO}">JAX TECH</div>
 <h1 style="font-size:76px;margin-top:28px">Never miss a<br><em>business call</em> again.</h1>
 <div style="font-size:25px;line-height:1.45;color:#C9D4E8;margin-top:22px;width:640px">Your office number rings on any cellphone, laptop or desk phone, wherever your team is.</div>
 <div style="display:flex;gap:12px;margin-top:28px">
  <div class="chip"><b>R59</b>/extension</div><div class="chip"><b>33c</b>/min, per second</div><div class="chip"><b>0</b> contracts</div></div>
 <div style="font-size:23px;color:#AFC3E6;font-weight:700;margin-top:24px;letter-spacing:.03em">jaxtech.co.za · 021 002 5637</div>
</div>
<div style="position:absolute;left:1080px;top:62px;transform:rotate(-6deg)">{phone()}</div>

</body>""",

"B-photo": f"""<body>
<img src="{d('woman-call-desk.jpg')}" style="position:absolute;left:560px;top:0;width:1080px;height:624px;object-fit:cover;object-position:center 30%">
<div style="position:absolute;inset:0;background:linear-gradient(90deg,{NAVY} 0%,{NAVY} 38%,rgba(15,30,58,.88) 52%,rgba(15,30,58,.15) 70%,rgba(15,30,58,0) 100%)"></div>
<div style="position:absolute;left:300px;top:80px;width:720px">
 <div class="brand"><img src="{LOGO}">JAX TECH</div>
 <h1 style="font-size:74px;margin-top:30px">Business phones,<br><em>no contract.</em></h1>
 <div style="font-size:26px;line-height:1.45;color:#C9D4E8;margin-top:22px">Keep your number. Answer on your cellphone.<br>R59 an extension · 33c a minute, billed per second.</div>
 <div style="margin-top:30px"><span class="cta">Free bill check · 021 002 5637</span></div>
</div></body>""",

"C-bold": f"""<body style="background:{INK}">
<div style="position:absolute;inset:0;background:repeating-linear-gradient(115deg,rgba(143,179,240,.05) 0 2px,transparent 2px 46px)"></div>
<div style="position:absolute;left:0;right:0;top:48px;text-align:center">
 <div class="brand" style="justify-content:center"><img src="{LOGO}">JAX TECH</div>
 <h1 style="font-size:82px;margin-top:28px">One number. <em>Every phone.</em><br>No contract.</h1>
 <div style="font-size:26px;color:#C9D4E8;margin-top:16px">Cloud business phones for South African offices</div>
 <div style="display:flex;gap:22px;justify-content:center;margin-top:38px">
  <div class="chip" style="padding:18px 30px"><b>R59</b>per extension</div>
  <div class="chip" style="padding:18px 30px"><b>R27</b>per app user</div>
  <div class="chip" style="padding:18px 30px"><b>33c</b>a minute, per second</div></div>
 <div style="font-size:23px;font-weight:700;color:{BLUE};margin-top:34px;letter-spacing:.04em">jaxtech.co.za · 021 002 5637</div>
</div></body>""",
}

def main():
    out = HERE / "out"; out.mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width":1640,"height":624})
        for k, body in OPTIONS.items():
            pg.set_content("<html><head>"+BASE+"</head>"+body+"</html>"); pg.wait_for_timeout(300)
            f = out / f"fb-cover-{k}.jpg"; pg.screenshot(path=str(f), type="jpeg", quality=95); print(f)
        b.close()
main()
