#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Alignment check (is the 2x output pixel-aligned with the master?) + zoom sheet."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FINAL = r"C:\Users\YanQiu\Desktop\nianzhen-pack\final"
OUT = r"C:\03_Github\.work\upscale\rc-check"

P = {
    "lanczos":   "nianzhen_sheet_3840_lanczos.png",
    "esrgan":    "nianzhen_sheet_3840_esrgan.png",
    "waifu2x":   "nianzhen_sheet_3840_waifu2x.png",
    "realcugan": "nianzhen_sheet_1920_master-up2x-no-denoise.png",
}
LABEL = {"lanczos": "Lanczos", "esrgan": "Real-ESRGAN",
         "waifu2x": "waifu2x", "realcugan": "Real-CUGAN", "master": "Master x2 (nearest)"}

master = Image.open(os.path.join(FINAL, "nianzhen_sheet_1920_master.png")).convert("RGB")
mw, mh = master.size
mg = np.asarray(master.convert("L")).astype(np.float64)


def best_shift(a, b, r=3):
    """a,b same size; return (dx,dy) that minimizes MAD between a and b shifted."""
    best = (0.0, 0, 0)
    h, w = a.shape
    cy, cx = h // 2, w // 2
    sl = (slice(cy - 300, cy + 300), slice(cx - 400, cx + 400))
    ref = a[sl]
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            sub = b[cy - 300 + dy: cy + 300 + dy, cx - 400 + dx: cx + 400 + dx]
            mad = float(np.abs(ref - sub).mean())
            if best == (0.0, 0, 0) or mad < best[0]:
                best = (mad, dx, dy)
    return best


print("== 对齐检查（1:1 折回 1920 后与母版相关）==")
for n, f in P.items():
    im = Image.open(os.path.join(FINAL, f)).convert("RGB")
    print(f"{n:10s} {im.size}", end="  ")
    g = np.asarray(im.resize((mw, mh), Image.LANCZOS).convert("L")).astype(np.float64)
    mad, dx, dy = best_shift(mg, g)
    print(f"best shift=({dx},{dy}) MAD={mad:.3f}   MAD@(0,0)={float(np.abs(mg-g).mean()):.3f}")

# ---- zoom sheet: tight eye crop, 2x nearest for viewing ---------------------
BOX = (3090, 840, 3290, 990)   # 200x150 at 3840
Z = 2
tw, th = (BOX[2] - BOX[0]) * Z, (BOX[3] - BOX[1]) * Z
pad, head = 6, 44
cols = ["master"] + list(P.keys())
W = len(cols) * tw + (len(cols) - 1) * pad
cv = Image.new("RGB", (W, head + th), (255, 255, 255))
d = ImageDraw.Draw(cv)
try:
    font = ImageFont.load_default(size=26)
except TypeError:
    font = ImageFont.load_default()
for i, n in enumerate(cols):
    if n == "master":
        t = master.crop((BOX[0] // 2, BOX[1] // 2, BOX[2] // 2, BOX[3] // 2))
    else:
        t = Image.open(os.path.join(FINAL, P[n])).convert("RGB").crop(BOX)
    t = t.resize((tw, th), Image.NEAREST)
    x = i * (tw + pad)
    cv.paste(t, (x, head))
    d.rectangle([x, 0, x + tw - 1, 36], fill=(32, 32, 32))
    d.text((x + 8, 6), LABEL[n], fill=(255, 255, 255), font=font)
out = os.path.join(OUT, "zoom_eye_2x.png")
cv.save(out)
print("zoom ->", out, cv.size)
