#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 source/ 的两张整图里重新裁格、拼成定妆照。

选格规则（用户指定）：
    第 1 格  全身正面   ← sheet_prev_1312x1199.png
    第 2 格  全身 3/4   ← sheet_this_1536x1024.png
    第 3 格  头部特写   ← sheet_prev_1312x1199.png

用法：
    python rebuild_from_source.py                 # 1920x1280
    python rebuild_from_source.py --height 2560   # 3840x2560
"""
import argparse
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")
PREV = os.path.join(SRC, "sheet_prev_1312x1199.png")
THIS = os.path.join(SRC, "sheet_this_1536x1024.png")

# (源图, 第几格从 0 开始, 类型)
PICK = [
    (PREV, 0, "full"),
    (THIS, 1, "full"),
    (PREV, 2, "close"),
]

CONFIG = {
    "gutter": 12,
    "panel_h": 1280,
    "fig_h": 1129,
    "baseline": 1240,
    "panel_w_ratio": 632 / 1280,
}


def white_columns(a):
    """整列几乎全白的列号（格间分隔线）。"""
    near_white = (a >= 246).all(axis=2)
    frac = near_white.mean(axis=0)
    cols = np.where(frac > 0.96)[0]
    runs = []
    if len(cols):
        start = prev = cols[0]
        for c in cols[1:]:
            if c - prev <= 2:
                prev = c
            else:
                runs.append((start, prev))
                start = prev = c
        runs.append((start, prev))
    # 只留中间那些两侧都有内容的（去掉贴边的）
    return [r for r in runs if r[0] > 4 and r[1] < a.shape[1] - 5]


def split_panels(path):
    img = Image.open(path).convert("RGB")
    a = np.asarray(img)
    runs = white_columns(a)
    if len(runs) < 2:
        sys.exit("没找到两条分隔线：" + path)
    x0, x1 = 0, a.shape[1]
    bounds = [x0]
    for s, e in runs:
        bounds.append(s)
        bounds.append(e + 1)
    bounds.append(x1)
    spans = [(bounds[i], bounds[i + 1]) for i in range(0, len(bounds) - 1, 2)]
    # 分隔线两侧有几像素半透明白，裁进来会在拼图上留下一条白缝，往里收 3 px
    trim = 3
    panels = []
    for s, e in spans:
        s2, e2 = min(s + trim, e - 1), max(e - trim, s + 1)
        panels.append(img.crop((s2, 0, e2, img.height)))
    return img, panels


def bg_of(a):
    """背景色：优先取四角小块的中间值（角落一定是纯背景），退化时取上下边缘。"""
    h, w = a.shape[:2]
    k = max(6, min(24, min(h, w) // 12))
    corners = np.concatenate([
        a[:k, :k].reshape(-1, 3),
        a[:k, -k:].reshape(-1, 3),
        a[-k:, :k].reshape(-1, 3),
        a[-k:, -k:].reshape(-1, 3),
    ], axis=0)
    good = corners[corners.mean(axis=1) > 150]
    if len(good) >= 8:
        return np.median(good, axis=0)
    strips = np.concatenate([a[:25].reshape(-1, 3), a[-25:].reshape(-1, 3)], axis=0)
    mask = strips.mean(axis=1) > 150
    return np.median(strips[mask], axis=0)


def fig_bbox(a, bg):
    d = np.abs(a - bg).max(axis=2)
    m = d > 30
    rows = np.where(m.sum(axis=1) > 4)[0]
    cols = np.where(m.sum(axis=0) > 4)[0]
    if len(rows) == 0 or len(cols) == 0:
        return (0, 0, a.shape[1], a.shape[0])
    return (cols[0], rows[0], cols[-1] + 1, rows[-1] + 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--height", type=int, default=1280)
    ap.add_argument("--out", default="final/nianzhen_sheet_1920_master.png")
    args = ap.parse_args()

    scale = args.height / CONFIG["panel_h"]
    ph = args.height
    pw = round(ph * CONFIG["panel_w_ratio"])
    gutter = max(2, round(CONFIG["gutter"] * scale))

    cache = {}
    picked = []
    for path, idx, kind in PICK:
        if path not in cache:
            cache[path] = split_panels(path)
        panels = cache[path][1]
        if idx >= len(panels):
            sys.exit("%s 只有 %d 格" % (path, len(panels)))
        picked.append((panels[idx], kind))

    saved_dir = os.path.join(HERE, "panels_v2")
    os.makedirs(saved_dir, exist_ok=True)
    names = ["01_front.png", "02_threequarter.png", "03_closeup.png"]
    for (panel, _kind), name in zip(picked, names):
        panel.save(os.path.join(saved_dir, name))

    arrs = [np.asarray(p).astype(float) for p, _ in picked]
    bgs = [bg_of(a) for a in arrs]
    target = np.median(np.stack(bgs), axis=0)
    bbs = [fig_bbox(a, b) for a, b in zip(arrs, bgs)]

    canvas = Image.new("RGB", (pw * 3 + gutter * 2, ph), (255, 255, 255))
    bg_tile = tuple(int(round(c)) for c in target)
    fig_h = CONFIG["fig_h"] * scale
    baseline = CONFIG["baseline"] * scale

    for i, (a, bg, bb, (_, kind)) in enumerate(zip(arrs, bgs, bbs, picked)):
        a = np.clip(a * (target / bg), 0, 255).astype(np.uint8)
        img = Image.fromarray(a)
        x0, y0, x1, y1 = bb
        tile = Image.new("RGB", (pw, ph), bg_tile)

        if kind == "close":
            s = ph / img.height
            img = img.resize((round(img.width * s), ph), Image.LANCZOS)
            tile.paste(img, ((pw - img.width) // 2, 0))
        else:
            s = fig_h / (y1 - y0)
            img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
            cx = (x0 + x1) * s / 2
            yb = y1 * s
            tile.paste(img, (round(pw / 2 - cx), round(baseline - yb)))

        canvas.paste(tile, (i * (pw + gutter), 0))

    out = os.path.join(HERE, args.out)
    os.makedirs(os.path.dirname(out) or HERE, exist_ok=True)
    canvas.save(out)
    print("已输出 %s  %dx%d" % (args.out, canvas.width, canvas.height))


if __name__ == "__main__":
    main()
