"""
Build #001's preview image (the link card on Substack, Bluesky, X and LinkedIn), 1200 x 630.

Format §9.8 as revised on 2026-10-05 (decisions 31-32): background #FBF2EC full bleed, all content in
the central safe zone x 310-890, y 125-455. Two white rounded panels with a thin grey border, in the
top of the zone (y 125-395), which must survive every crop: left, the Mediterranean in the 1980s above
the 2020s, without colour bar (make_preview_map.py; Riccardo's choice of 2026-10-04, restored 2026-10-05); right, "BIT VERDICT", the Reality's hero number and a gloss
of at most 8 words. The bottom band (y 395-455) holds only what may be lost: the range line.
The number is read from KEY_NUMBERS.md ("Verdict, Reality line"), exactly as the Verdict states it.
Fails if it is missing, if the hero would be under 60 px, or if the gloss needs a third line. After
saving, the PNG is read back and its content box checked inside the safe zone; 160 px and centred
square crops are saved for the checks. Run make_preview_map.py en|it first.

    python make_preview.py en|it        -> figures/fig-001-preview[-it].png

BIG IF TRUE · tropical-nights · https://github.com/bigiftruebits/bit-001-tropical-nights
Author: Riccardo Gallotti (FBK). Code by Claude Opus 5.5 under his direction.
Licence: MIT (code); data licences in DATA_MANIFEST.md.
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import ROOT, FIGURES
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib

LANG = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ("en", "it") else "en"
TXT = {"en": dict(kicker="BIT VERDICT", gloss="fewer cool hours a night, per person", rng={"half an hour": "± half an hour"},
                  fig="fig-001-preview-map.png", out="fig-001-preview.png"),
       "it": dict(kicker="BIT VERDETTO", gloss="ore fresche in meno a notte, a persona", rng={"half an hour": "± mezz’ora"},
                  fig="fig-001-preview-map-it.png", out="fig-001-preview-it.png")}[LANG]
W, H = 1200, 630
SAFE = (305, 80, 895, 480)     # mobile first (decision 33): everything that matters inside x 305-895, y 80-480
SQUARE = (285, 0, 915, 630)
BG, PANEL, BORDER, ACCENT, INK = (251, 242, 236), "white", (201, 206, 214), "#C1440E", "#26323F"
fdir = os.path.join(matplotlib.get_data_path(), "fonts", "ttf")
font = lambda px, bold=False: ImageFont.truetype(os.path.join(fdir, "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), px)
x0, y0, x1, y1 = SAFE
img = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(img)

# the Verdict's number, exactly as printed, with its range
k = open(ROOT / "KEY_NUMBERS.md", encoding="utf8").read()
m = re.search(r"Verdict, Reality line: \*\*(\d+(?:\.\d+)?) hours a night(?:, give or take ([^*]+))?\*\*", k)
if not m:
    sys.exit("FAIL: the Verdict's number is not in KEY_NUMBERS.md (line 'Verdict, Reality line')")
hero = (m.group(1).replace(".", ",") if LANG == "it" else m.group(1)) + " h"
rng = TXT["rng"].get(m.group(2), "") if m.group(2) else ""

# left panel: the two maps, uncropped; the panel takes the maps' own shape (no empty band), and
# both panels are centred vertically in the zone. The range sits inside the Verdict panel (5 Oct).
LW, PAD, GAP = 372, 8, 12
f = Image.open(FIGURES / TXT["fig"]).convert("RGB")
fw = LW - 2 * PAD; fh = round(f.height * fw / f.width)
PH = fh + 2 * PAD
py0 = y0 + ((y1 - y0) - PH) // 2; py1 = py0 + PH
d.rounded_rectangle([x0 + 1, py0, x0 + LW, py1], radius=14, fill=PANEL, outline=BORDER, width=2)
img.paste(f.resize((fw, fh), Image.LANCZOS), (x0 + PAD + 1, py0 + PAD))
# right panel: kicker, hero number, gloss, range
rx0 = x0 + LW + GAP; rw = x1 - 2 - rx0; ip = 14; cw = rw - 2 * ip     # 2 px in: the outline stays inside
d.rounded_rectangle([rx0, py0, x1 - 2, py1], radius=14, fill=PANEL, outline=BORDER, width=2)
size = 120
while size > 1 and d.textlength(hero, font=font(size, True)) > cw: size -= 1
if size < 60:
    sys.exit(f"FAIL: the hero number would be {size} px, below 60")
gs, lines = 28, None
while gs >= 20:
    ls = [""]
    for w_ in TXT["gloss"].split():
        t = (ls[-1] + " " + w_).strip()
        if d.textlength(t, font=font(gs)) <= cw: ls[-1] = t
        else: ls.append(w_)
    if len(ls) <= 3: lines = ls; break
    gs -= 1
if lines is None:
    sys.exit("FAIL: the gloss needs more than 3 lines")
ks = 24
while ks > 16 and d.textlength(TXT['kicker'], font=font(ks, True)) > cw: ks -= 1
rs = 26
while rng and rs > 16 and d.textlength(rng, font=font(rs, True)) > cw: rs -= 1
rf = font(rs, True)
hb = d.textbbox((0, 0), hero, font=font(size, True))
block = ks + 14 + (hb[3] - hb[1]) + 16 + round(gs * 1.25) * len(lines) + (14 + rs if rng else 0)
y = py0 + (PH - block) // 2
d.text((rx0 + ip, y), TXT["kicker"], font=font(ks, True), fill=ACCENT); y += ks + 14
d.text((rx0 + ip, y - hb[1]), hero, font=font(size, True), fill=ACCENT); y += hb[3] - hb[1] + 16
for ln in lines:
    d.text((rx0 + ip, y), ln, font=font(gs), fill=INK); y += round(gs * 1.25)
if rng:
    y += 14; d.text((rx0 + ip, y), rng, font=rf, fill=ACCENT); y += rs
if y > py1 - 10:
    sys.exit("FAIL: the verdict panel overflows")
FIGURES.mkdir(exist_ok=True); img.save(FIGURES / TXT["out"])

# ---- read the PNG back, and save the 160 px and square-crop checks ----------------------------
a = np.asarray(Image.open(FIGURES / TXT["out"]).convert("RGB")).astype(int)
ys, xs = np.where(np.abs(a - np.array(BG)).sum(axis=2) > 0)
box = (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)
inside = box[0] >= x0 and box[1] >= y0 and box[2] <= x1 and box[3] <= y1
print(f"{TXT['out']}: hero '{hero}' {size} px ({size * 520 / W:.0f} at 520, {size * 160 / W:.0f} at 160); gloss {len(lines)} lines at {gs} px;"
      f" box x {box[0]}-{box[2]}, y {box[1]}-{box[3]}; inside the safe zone: {inside}")
if not inside:
    sys.exit("FAIL: content outside the safe zone")
im = Image.open(FIGURES / TXT["out"])
im.resize((160, 84), Image.LANCZOS).save(FIGURES / TXT["out"].replace(".png", "-160.png"))
im.crop(SQUARE).resize((170, 170), Image.LANCZOS).save(FIGURES / TXT["out"].replace(".png", "-square-170.png"))
