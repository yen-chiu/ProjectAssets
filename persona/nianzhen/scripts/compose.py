#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把三格拼成定妆照。

用法：
    python compose.py                 # 输出 1920x1280
    python compose.py --height 2560   # 输出 3840x2560（3:2）

依赖：Pillow, numpy
    pip install pillow numpy

几何参数在下面 CONFIG 里，改宽度/留白/人物高度都在那。
"""
import argparse
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
PANELS = [
    ("panels_v2/01_front.png", "full"),       # 全身正面
    ("panels_v2/02_threequarter.png", "full"),  # 全身 3/4
    ("panels_v2/03_closeup.png", "close"),    # 头部特写
]

CONFIG = {
    "gutter": 12,      # 格间距（白）
    "panel_h": 1280,   # 单格高度
    "fig_h": 1129,     # 全身格里人物的高度（像素）
    "baseline": 1240,  # 脚底所在 y
}


def bg_of(a):
    """取上下边缘的中位色当背景色。"""
    strips = np.concatenate([a[:25].reshape(-1, 3), a[-25:].reshape(-1, 3)], axis=0)
    mask = strips.mean(axis=1) > 150
    return np.median(strips[mask], axis=0)


def fig_bbox(a, bg):
    """人物外框：跟背景差 >30 的像素。"""
    d = np.abs(a - bg).max(axis=2)
    m = d > 30
    rows = np.where(m.sum(axis=1) > 4)[0]
    cols = np.where(m.sum(axis=0) > 4)[0]
    if len(rows) == 0 or len(cols) == 0:
        return (0, 0, a.shape[1], a.shape[0])
    return (cols[0], rows[0], cols[-1] + 1, rows[-1] + 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--height", type=int, default=1280, help="输出高度，宽度按 3:2 算")
    ap.add_argument("--out", default="composite.png")
    args = ap.parse_args()

    scale = args.height / CONFIG["panel_h"]
    ph = args.height
    pw = round(ph * 632 / 1280)
    gutter = max(2, round(CONFIG["gutter"] * scale))
    fig_h = CONFIG["fig_h"] * scale
    baseline = CONFIG["baseline"] * scale

    imgs = []
    for rel, _kind in PANELS:
        p = os.path.join(HERE, rel)
        if not os.path.exists(p):
            sys.exit("找不到 " + p)
        imgs.append(Image.open(p).convert("RGB"))

    arrs = [np.asarray(im).astype(float) for im in imgs]
    bgs = [bg_of(a) for a in arrs]
    target = np.median(np.stack(bgs), axis=0)
    bbs = [fig_bbox(a, b) for a, b in zip(arrs, bgs)]

    canvas = Image.new("RGB", (pw * 3 + gutter * 2, ph), (255, 255, 255))
    bg_tile = tuple(int(round(c)) for c in target)

    for i, ((rel, kind), a, bg, bb) in enumerate(zip(PANELS, arrs, bgs, bbs)):
        a = np.clip(a * (target / bg), 0, 255).astype(np.uint8)
        img = Image.fromarray(a)
        x0, y0, x1, y1 = bb
        tile = Image.new("RGB", (pw, ph), bg_tile)

        if kind == "close":
            # 特写：整格按高度铺满
            s = ph / img.height
            img = img.resize((round(img.width * s), ph), Image.LANCZOS)
            tile.paste(img, ((pw - img.width) // 2, 0))
        else:
            # 全身：人物高度对齐，脚底压到同一条基线
            s = fig_h / (y1 - y0)
            img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
            cx = (x0 + x1) * s / 2
            yb = y1 * s
            tile.paste(img, (round(pw / 2 - cx), round(baseline - yb)))

        canvas.paste(tile, (i * (pw + gutter), 0))

    canvas.save(os.path.join(HERE, args.out))
    print("已输出 %s  %dx%d" % (args.out, canvas.width, canvas.height))


if __name__ == "__main__":
    main()
