# 念真 · 人物素材包（2026-11 版）

这是 2026 年 11 月 16 日重画的一套念真。交付 41 张，保留 35 张；被替换的旧版本（170 cm 档案照、旧九宫格、旧书店蹲姿、11 月 4–9 日的夜读图）没有进入这个包。

站点页面：`yen-chiu.github.io/_tabs/persona.md`（`/persona/`）。本目录是母本，`site/` 与站点 `assets/img/persona/` 同名同步。

## 用哪张

| 用途 | 文件 |
| --- | --- |
| 首屏肖像 | `nz-portrait.webp`（原图 08） |
| 一页设定稿 | `nz-sheet.webp`（原图 25） |
| 九宫格表情 | `nz-expressions.webp` + `nz-expr-1..9-*.webp`（原图 23） |
| 160 cm 档案照 | `nz-archive-160.webp`（原图 12） |
| 细节 / 材质 | `nz-detail-*.webp`、`nz-material-*.webp`（从设定稿切） |
| 场景与日常 | 其余 `nz-*.webp` |

`nz-expressions.webp` 是整张九宫格，页面实际用切开的九张；保留整张便于以后换版式。

## 目录

```
nianzhen/
  README.md          本文件
  prompt-v4.md       2026-11-16 版 prompt 库（0–15 节）
  manifest.json      35 张的索引、原文件名、字节数、sha256 前 8 位
  source/            35 张选中原片，PNG，nz-<slug>.png
  site/              52 张站点交付，WebP
  crops/             17 张切格：9 张表情 + 8 张细节/材质
```

## 怎么复现

1. **出图**：按 `prompt-v4.md` 的 0、12、15 节先定脸、三视图和一页设定稿，再用第 2–8 节补场景。不要先出场景再回头改脸，脸会飘。
2. **选片**：按 `manifest.json` 的 `index` 对应原片；同一场景有多版时，取时间更晚、脸更一致的那张（06 取 20:51，不取 30 的 17:04；23 取 11/16，不取 22 的 11/10）。
3. **压缩**：设定稿最长边 1600 / q92；肖像 1000 / q88；场景 760 / q84；九宫格 1200 / q90；切格 q90–92。全部 WebP，`method=6`。
4. **切格**：设定稿源图 1536×1024。表情按 3×3 等分；细节四格约 `(788,292)-(1526,452)`，材质四格 `(788,458)-(1526,572)`，横向四等分。精确框见 `C:/03_Github/.work/build_persona_assets.py`。
5. **同步站点**：`site/*.webp` 复制到 `yen-chiu.github.io/assets/img/persona/`，同名覆盖；页面引用以 `nz-` 开头。

## 35 张索引

| # | slug | 内容 | 原文件 | sha256 |
| --- | --- | --- | --- | --- |
| 0 | `hallway` | 走廊 · 放学后 | `IMG_20261116_194512.png` | `5f71c2cf` |
| 1 | `desk-nap` | 凌晨三点 · 趴在桌上睡着 | `IMG_20261116_205615.png` | `5c923833` |
| 2 | `convenience-store` | 便利店 · 挑饮料 | `IMG_20261116_210704.png` | `928f30d4` |
| 3 | `desk-top` | 书桌俯拍 · 写到手酸 | `IMG_20261116_210714.png` | `1dabd002` |
| 4 | `intp-split` | 现实与内心的分屏 | `INTP：现实与内心的分屏.png` | `0511d068` |
| 5 | `camera-leaves` | 秋天 · 举着相机 | `file_00000000050c81fd8f74546b3c55d7bd.png` | `c43f7be0` |
| 6 | `bookstore-crouch` | 旧书店 · 蹲在书架前 | `file_0000000029cc81fdba952a0a1b038779.png` | `c70be65c` |
| 7 | `night-bus` | 夜班车 · 窗前 | `file_00000000388881fda13e6e12ddbe28bd.png` | `1f84060e` |
| 8 | `portrait` | 正面肖像 · 基准脸 | `file_0000000069a081fda0ffafa3471bd422.png` | `94e1f02f` |
| 10 | `kalimba-window` | 窗边 · 弹卡林巴 | `file_00000000a54881fda4e23ed64d86c4d9.png` | `e4f52b03` |
| 11 | `subway-platform` | 末班地铁 · 站台 | `file_00000000b6e081fd8d1aeb3fa691e62b.png` | `cadaba75` |
| 12 | `archive-160` | 虚构档案照 · 160 cm | `file_00000000e02881fd95b16573664b7dbb.png` | `cda6bedb` |
| 13 | `stairwell-light` | 楼梯间的光 | `file_00000000e9e081fd9a45c7a1798e1592.png` | `c44c8dba` |
| 14 | `bookstore-hand` | 「你拍我干嘛」 | `「你拍我干嘛」.png` | `ee655557` |
| 15 | `state-code` | 夜里写代码 | `凑过来看屏幕.png` | `a5341228` |
| 16 | `typhoon-window` | 台风天 · 窗户在响 | `台风天 · 窗户在响.png` | `f5286785` |
| 17 | `summer-sparkler` | 夏 · 仙女棒 | `夏.png` | `33d01725` |
| 18 | `rooftop-night` | 夏夜天台 · 汽水 | `夏夜天台 · 汽水2.png` | `5a9657eb` |
| 23 | `expressions-9up` | 九宫格表情 · 开怀大笑…委屈 | `开怀大笑、浅笑、平静、困倦、嘴硬、惊讶、专注、得意、委屈。.png` | `8c5b0d25` |
| 24 | `unhappy` | 念真 · 不高兴 | `念真 · 不高兴.png` | `154230e7` |
| 25 | `character-sheet` | 一页角色设定稿 | `念真的动漫角色设定集.png` | `306ecfe1` |
| 26 | `clay-cat` | 手工 · 黏土猫 | `手工 · 黏土小东西.png` | `9ada57a9` |
| 27 | `quote-flowers` | 抄句子 · 本子与干花 | `抄句子 · 本子与干花.png` | `cb4c5f9b` |
| 28 | `shadow-hand` | 拍影子 · 手 | `拍影子2.png` | `7f3109e1` |
| 29 | `shadow-camera` | 拍影子 · 楼梯间 | `拍影子3.png` | `42c662cf` |
| 31 | `seasons` | 春夏秋冬 · 四格 | `春夏秋冬.png` | `5b9d49c7` |
| 32 | `store-night` | 深夜便利店 · 关东煮 | `深夜便利店 · 关东煮.png` | `fbce17d2` |
| 33 | `cat-camera` | 猫：相册里永远拍不全 | `猫：相册里永远拍不全.png` | `669374c0` |
| 34 | `laugh` | 真正笑出声 | `真正笑出声.png` | `ac15118e` |
| 35 | `autumn-ginkgo` | 秋天 · 银杏和干花 | `秋天 · 银杏和干花.png` | `502562ca` |
| 36 | `rain-shelter` | 突然下雨 · 躲进屋檐 | `突然下雨 · 躲进屋檐.png` | `0e75b841` |
| 37 | `shelf-build` | 装书架 · 少了一颗螺丝 | `装书架 · 少了一颗螺丝.png` | `8e867f9d` |
| 38 | `walk-candy` | 走路 · 口袋里的糖 | `走路 · 口袋里的糖.png` | `ffbc0774` |
| 39 | `offer-candy` | 递糖果 | `递糖果.png` | `266f2c11` |
| 40 | `laundry-balcony` | 阳台晒被子 | `阳台晒被子.png` | `a6c22bea` |

sha256 取前 8 位，对应 `source/nz-<slug>.png` 的完整文件；全量哈希可用 `Get-FileHash` 复核。

## 取舍记录

- **09 / 12**：09 是 170 cm 的旧档案照，身高写错；12 是 160 cm 的正确版。只留 12。
- **22 / 23**：22 是 11 月 10 日的旧九宫格；23 是 11 月 16 日重画的表情表，眼神和脸型与 08 一致。只留 23。
- **30 / 06**：30 是 17:04 的旧书店蹲姿，06 是 20:51 的更新版；同一构图只留 06。
- **19–21**：11 月 4–9 日的夜读三版，属于上一轮；博客封面另存于文章目录，不进入人物页素材包。
- 旧 v3 的 `compare/`、`final/`、`panels/`、`scenes/`、`scripts/`、`sheets/` 和 `prompt-v3.md` 已删除；站点旧 27 张 `nz-*` 已由新 52 张替换。
