#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compare the 4 upscale candidates of nianzhen_sheet_1920_master + build 1:1 crops."""
import os
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FINAL = r"C:\Users\YanQiu\Desktop\nianzhen-pack\final"
OUT = r"C:\03_Github\.work\upscale\rc-check"
os.makedirs(OUT, exist_ok=True)

P = {
    "master":    os.path.join(FINAL, "nianzhen_sheet_1920_master.png"),
    "lanczos":   os.path.join(FINAL, "nianzhen_sheet_3840_lanczos.png"),
    "esrgan":    os.path.join(FINAL, "nianzhen_sheet_3840_esrgan.png"),
    "waifu2x":   os.path.join(FINAL, "nianzhen_sheet_3840_waifu2x.png"),
    "realcugan": os.path.join(FINAL, "nianzhen_sheet_1920_master-up2x-no-denoise.png"),
}
ORDER = ["lanczos", "esrgan", "waifu2x", "realcugan"]
LABEL = {"lanczos": "Lanczos (interp)", "esrgan": "Real-ESRGAN x4p-anime",
         "waifu2x": "waifu2x cunet n2", "realcugan": "Real-CUGAN up2x-no-denoise",
         "master": "Master (nearest x2)"}


def lap_energy(gray):
    a = gray.astype(np.float32)
    L = np.abs(-4 * a[1:-1, 1:-1] + a[:-2, 1:-1] + a[2:, 1:-1] + a[1:-1, :-2] + a[1:-1, 2:])
    return float(L.mean()), float(L.std())


def srgb2lab(rgb):
    c = np.asarray(rgb, dtype=np.float64) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = M @ c
    white = np.array([0.95047, 1.0, 1.08883])
    t = xyz / white
    f = np.where(t > 216 / 24389, np.cbrt(t), (24389 / 27 * t + 16) / 116)
    return np.array([116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2])])


def dE76(a, b):
    return float(np.linalg.norm(srgb2lab(a) - srgb2lab(b)))


def bg_patch(im, size=200):
    a = np.asarray(im.convert("RGB")).astype(np.float64)
    h, w = a.shape[:2]
    s = max(8, size * h // 2560)
    return a[10:10 + s, 10:10 + s].reshape(-1, 3).mean(0)


stats = {}
imgs = {}
for name, path in P.items():
    im = Image.open(path).convert("RGB")
    imgs[name] = im
    stats[name] = {"size": list(im.size)}

master = imgs["master"]
mw, mh = master.size
mm = np.asarray(master).astype(np.float64)

for name in ORDER:
    im = imgs[name]
    w, h = im.size
    st = stats[name]
    g = np.asarray(im.convert("L"))
    st["edge_native"] = lap_energy(g)
    # 折回 1920 再算，跟母版同尺度比较
    g1 = np.asarray(im.resize((mw, mh), Image.LANCZOS).convert("L"))
    st["edge_at1920"] = lap_energy(g1)
    # 背景色偏
    bg = bg_patch(im)
    bgm = bg_patch(master)
    st["bg_rgb"] = [round(float(x), 2) for x in bg]
    st["bg_dE_vs_master"] = round(dE76(bg, bgm), 2)
    st["bg_drgb"] = [round(float(x), 2) for x in (bg - bgm)]
    # 整图低频色偏（480x320 下采样后比）
    a = np.asarray(im.resize((480, 320), Image.LANCZOS)).astype(np.float64)
    b = np.asarray(master.resize((480, 320), Image.LANCZOS)).astype(np.float64)
    d = np.abs(a - b)
    st["lowfreq_mad"] = round(float(d.mean()), 3)
    st["lowfreq_p99"] = round(float(np.percentile(d, 99)), 2)
    st["mean_rgb"] = [round(float(x), 2) for x in a.reshape(-1, 3).mean(0)]
    st["mean_dE_vs_master"] = round(dE76(a.reshape(-1, 3).mean(0), b.reshape(-1, 3).mean(0)), 2)

# ---- 1:1 crops -------------------------------------------------------------
SCALE = 2  # upscalers are 2x of the master


def crop_sheet(crops, outfile, cols, pad=6, head=46):
    """crops: list of (name, (x0,y0,x1,y1)) at 3840 coords; master uses /2 + nearest x2"""
    # build per column: col 0 = master nearest x2, then ORDER
    items = []
    for cname, (x0, y0, x1, y1) in crops:
        items.append((cname, x0, y0, x1, y1))
    tw = items[0][3] - items[0][1]
    th = items[0][4] - items[0][2]
    ncol = len(items)
    W = ncol * tw + (ncol - 1) * pad
    H = head + th
    canvas = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.load_default(size=26)
    except TypeError:
        font = ImageFont.load_default()
    for i, (cname, x0, y0, x1, y1) in enumerate(items):
        if cname == "master":
            t = master.crop((x0 // SCALE, y0 // SCALE, x1 // SCALE, y1 // SCALE))
            t = t.resize((tw, th), Image.NEAREST)
        else:
            t = imgs[cname].crop((x0, y0, x1, y1))
        canvas.paste(t, (i * (tw + pad), head))
        label = LABEL[cname]
        bx0 = i * (tw + pad)
        draw.rectangle([bx0, 0, bx0 + tw - 1, head - 8], fill=(32, 32, 32))
        draw.text((bx0 + 10, 8), label, fill=(255, 255, 255), font=font)
    canvas.save(outfile)
    return outfile, canvas.size


CROP_EYES = (2900, 700, 3500, 1100)   # closeup panel, eye band
CROP_KNIT = (2760, 1230, 3360, 1630)  # closeup panel, sweater knit
CROP_HAIR = (3050, 380, 3650, 780)    # closeup panel, hair top / hairpin

crops = [("master", CROP_EYES)] + [(n, CROP_EYES) for n in ORDER]
f1, s1 = crop_sheet(crops, os.path.join(OUT, "cmp_eyes_1to1.png"), None)
crops = [("master", CROP_KNIT)] + [(n, CROP_KNIT) for n in ORDER]
f2, s2 = crop_sheet(crops, os.path.join(OUT, "cmp_knit_1to1.png"), None)
crops = [("master", CROP_HAIR)] + [(n, CROP_HAIR) for n in ORDER]
f3, s3 = crop_sheet(crops, os.path.join(OUT, "cmp_hair_1to1.png"), None)

# full-view strip, downscaled
thumbs = []
for n in ["master"] + ORDER:
    im = imgs[n]
    r = 900 / im.size[1]
    thumbs.append((n, im.resize((round(im.size[0] * r), 900), Image.LANCZOS)))
W = sum(t.size[0] for _, t in thumbs) + 6 * (len(thumbs) - 1)
H = 900 + 46
cv = Image.new("RGB", (W, H), (255, 255, 255))
d = ImageDraw.Draw(cv)
try:
    font = ImageFont.load_default(size=26)
except TypeError:
    font = ImageFont.load_default()
x = 0
for n, t in thumbs:
    cv.paste(t, (x, 46))
    d.rectangle([x, 0, x + t.size[0] - 1, 38], fill=(32, 32, 32))
    d.text((x + 10, 8), LABEL[n], fill=(255, 255, 255), font=font)
    x += t.size[0] + 6
cv.save(os.path.join(OUT, "cmp_overview.png"))

print(json.dumps(stats, ensure_ascii=False, indent=1))
print("eyes  ->", f1, s1)
print("knit  ->", f2, s2)
print("hair  ->", f3, s3)
print("overview ->", os.path.join(OUT, "cmp_overview.png"))
