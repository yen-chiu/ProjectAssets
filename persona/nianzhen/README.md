# 念真 · 定妆照素材

> 三格定妆照（全身正面 / 全身 3/4 / 头部特写），后续所有图的角色锚点。
> 原包在 `~/Desktop/nianzhen-pack`，2026-11-09 归档到这里，文件名按本库约定整理过（见 `../README.md`）。

---

## 一、目录

```
prompt-v3.md    出图提示词 + 人设速查（当前版：3:2 三格）
source/         两次生成的整张原片（系统压缩副本，不是生成时的原图）
  sheet_prev_1312x1199.png   上一版整张，左右两格出自这里
  sheet_this_1536x1024.png   这一版整张，中间格出自这里
panels/         切好的三格
  01_front.png          全身正面   387×1199
  02_threequarter.png   全身 3/4   422×1024
  03_closeup.png        头部特写   546×1199
final/
  nianzhen_sheet_1920_master.png                    1920×1280  母版，任何重拼都从它出发
  nianzhen_sheet_3840_realcugan_up2x-nodenoise.png  3840×2560  ★ 锚点就是这张
  nianzhen_sheet_3840_esrgan.png                    3840×2560  极限锐度备选
  nianzhen_sheet_3840_waifu2x.png                   3840×2560  反偏色对照
  nianzhen_sheet_3840_lanczos.png                   3840×2560  纯插值对照，可删
compare/        超分对比：整图并排、1:1 三处裁切、2× 放大条
scripts/        拼版（compose / rebuild_from_source）与量测（analyze_upscale / zoom_check）
site/           站点正在用的那一组：nz-anchor-sheet.webp + 三张 nz-upscale-0*.png
scenes/         场景图（按 art-prompts 第 2 节出的单张成品，未超分）
  nianzhen_nightread_lookup_1012x1348.png   夜读·台灯下抬头 3:4  → 聊天页欢迎屏 900×1200
  nianzhen_nightread_lookup_1254x1254.png   夜读·台灯下抬头 1:1  → 聊天页书桌位 1000×1000
  nianzhen_nightread_lookup_1448x1086.png   夜读·台灯下抬头 4:3  → 聊天页欢迎屏（2026-11-10 起换成它）
sheets/         设定稿与表情表原图（站点 02/03/04 图位都从这两张裁）
  nianzhen_character_sheet_1312x1199.png    一页设定稿：正/三分之四全身、面部、四处细节、配色
  nianzhen_expressions_9up_1254x1254.png    九宫格表情第一版，3×3 每格 418×418
  nianzhen_expressions_9up_notes.txt        出这张表时的备注（第五格外转不够、第七格像不悦）
```

---

## 二、用哪张

- **喂模型当参考图 → `final/nianzhen_sheet_3840_realcugan_up2x-nodenoise.png`。** 四版里色偏最小（背景 ΔE 0.65，ESRGAN 是 1.56），而缩到模型实际吃的 1K 时锐度反超 ESRGAN（1.12× vs 1.08×）——参考图最终就是这个尺寸，所以选它。
- **要极限锐度 / 印刷 → `..._esrgan.png`。** 发丝、睫毛、针织织纹补得最狠，代价是睫毛外沿和发丝带暖红描边，背心的冷灰蓝针脚被推成暖铜色。
- **把偏色降到最低的对照 → `..._waifu2x.png`。** 几乎不偏色，但锐度只比插值高一档（1.19×），细节增长有限。
- **`1920_master` 是母版。** 重新拼版、重新超分都从它出发，别拿 3840 再放一次。
- `..._lanczos.png` 只是对照物，可以不留。

---

## 三、三格是怎么来的

三格不是一次生成的，是两次生成里各取一格拼的：

| 格 | 来源 | 为什么选它 |
|---|---|---|
| 左·全身正面 | 上一版 | 表情松弛，脸圆，肩线自然 |
| 中·全身 3/4 | 这一版 | 真正的 45° 转身：左肩朝镜头、只露左耳、右耳被头挡住 |
| 右·头部特写 | 上一版 | 和左格同一张画，脸完全一致；酒窝、金耳圈、发夹都在 |

拼接时做了四件事，接缝才看不出来：

1. 三格背景灰统一到同一色（204, 203, 208）
2. 全身格人物按身高对齐（1129 px）
3. 脚底压到同一条基线（y=1240，1920 版坐标）
4. 分隔线两侧各内收 3 px —— 原图格线边缘有半透明白，不裁掉拼出来就是一条白缝

几何参数：单格 632×1280，格间距 12 px，整图 3:2。

---

## 四、已知问题

- **三格全在笑，没有中性脸。** 上一版左格本身就是微笑的，拼过来之后中性那张就没了。
- **中间格裤型比两侧蓬**，腰也高一截。两批画的，衣服松紧对不上。
- **中间格和特写不是同一张脸**：特写来自上一版，中间来自这一版，脸型略有出入。
- source 里这两张是**系统压缩过的副本**（1312×1199、1536×1024），不是生成时的原图。原图换进来，脚本不用改。
- 上面几条都是素材本身的差异，拼图解决不了；要彻底一致只能整张重画。

---

## 五、重新拼

```bash
python scripts/rebuild_from_source.py --height 1280 --out final/nianzhen_sheet_1920_master.png
python scripts/rebuild_from_source.py --height 2560 --out final/nianzhen_sheet_3840_lanczos.png
```

- 脚本自己找两条白色分隔线切三格（prev: 393 / 757；this: 468 / 900），两侧内收 3 px
- 背景色取四角小块的中位值（取上下边缘会把鞋和影子算进去，拼出来边上留浅印）
- 三格人物统一 1129 px 高、脚底压 y=1240，实测三格 bbox 完全一致
- 换更高清的 source 进来，脚本自动按人物高度重新对，不用改参数

---

## 六、超分实录（2026-11-09 实跑，Intel UHD 620）

输入一律 `final/nianzhen_sheet_1920_master.png`。

### Real-CUGAN 2× · 无降噪（当前锚点）

浏览器里跑（CPU，图片不出本机）：倍率 2X、降噪「无降噪」、预览「左右并排」。12 MB 引擎 + 约 1.6 GB 内存，1920×1280 跑了约 150 秒，下载回来是**原生 3840×2560 PNG**，工具没有再降采样——这点已经逐像素核过（与母版对齐偏移为 0,0）。

这张是平灰底、干净的渲染图，没有噪点，所以「无降噪」档最合适；降噪档会把发丝一起抹平。

可用镜像：`https://binglengdexiwang.top/static/web/image-upscale.html`（原项目 demo 站已失效；镜像不支持 iOS）。

### Real-ESRGAN（ncnn-vulkan）

```
realesrgan-ncnn-vulkan.exe -i nianzhen_sheet_1920_master.png -o master_esrgan4x.png -n realesrgan-x4plus-anime -s 4 -t 128
```

**坑：这台机器上 `-s 2` 输出是坏的。** 出来是一堆错位的小方块拼贴，每个 tile 内容都偏了一截，整张跑和单块跑都这样，调 `-t` 也没用；同样参数换 `-s 4` 就正常。所以流程是**先 4 倍到 7680×5120，再用 Pillow LANCZOS 降回 3840×2560**。耗时约 4 分钟。

### waifu2x（ncnn-vulkan）

```
waifu2x-ncnn-vulkan.exe -i nianzhen_sheet_1920_master.png -o master_waifu2x.png -n 2 -s 2 -m models-cunet
```

`-s 2` 没问题，直接出 3840，约 30 秒。`-n 2` 是降噪档，这张背景平灰没噪点，`-n 1` 也够。

### 四版数据（3840 下）

| 版本 | 锐度（Laplacian 均值） | 相对插值 | 缩到 2048 | 缩到 1024 | 背景 ΔE | 低频偏离 MAD |
|---|---|---|---|---|---|---|
| Lanczos 插值 | 2.27 | 1.00× | 1.00× | 1.00× | 0.00 | 0.54 |
| Real-ESRGAN | 5.52 | 2.44× | 1.52× | 1.08× | 1.56 | 1.55 |
| waifu2x cunet n2 | 2.71 | 1.19× | 1.04× | 0.99× | 0.46 | 0.51 |
| **Real-CUGAN up2x-no-denoise** | **5.04** | **2.22×** | **1.49×** | **1.12×** | **0.65** | **1.01** |

- 「缩到 2048 / 1024」是同一张图缩到该宽度后、相对插值的锐度倍数，模拟参考图被生成模型降采样。**锐度差在这一步基本消失，色偏却全额保留**，这就是选 Real-CUGAN 的理由。
- 早期这页记的「边缘能量 1.41 / 2.09 / 1.41」是另一套归一化，倍数一致，别拿来跟这张表混着比。
- 低频偏离是缩到 480×320 后与母版的 MAD，越小越贴着母版结构。
- 观感：ESRGAN 睫毛/发丝外沿有暖红描边，针织暗部把冷灰蓝针脚高光（母版 R−B = −14.2）推到局部 R−B = +69；Real-CUGAN 同处 −11.7，边缘干净。

---

## 七、拿去用

1. **特写格是脸部锚点**，后面每张图优先喂它，比喂全身稳。
2. 全身两格管服装、比例、站姿。
3. 场景图只喂锚点图，**别把「浅灰底平光」写进新提示词**，否则每张都被定妆光带偏。
4. 模型支持参考图就优先图生图；纯文字重画，脸一定会跑。
5. 出图 prompt 用 `prompt-v3.md`；站点上同一份在 `yen-chiu.github.io/chat/assets/persona/art-prompts.md` 第 0 节。
6. 站点页面：`yen-chiu.github.io/_tabs/persona.md` 第 10 节「定妆照 · 锚点图」，含三组 1:1 对比与这张表。

---

## 八、素材溯源（sha256 前 8 位）

| 文件 | sha256 | 说明 |
|---|---|---|
| `source/sheet_prev_1312x1199.png` | `40903d38` | 上一版整张 |
| `source/sheet_this_1536x1024.png` | `4b79fde7` | 这一版整张 |
| `panels/01_front.png` | `ae406349` | 全身正面 |
| `panels/02_threequarter.png` | `af251db4` | 全身 3/4 |
| `panels/03_closeup.png` | `20968765` | 头部特写 |
| `final/nianzhen_sheet_1920_master.png` | `26555f13` | 母版 |
| `final/nianzhen_sheet_3840_realcugan_up2x-nodenoise.png` | `d6bc121f` | ★ 锚点（原文件名 `..._1920_master-up2x-no-denoise.png`） |
| `final/nianzhen_sheet_3840_esrgan.png` | `d42dde97` | ESRGAN 超分 |
| `final/nianzhen_sheet_3840_waifu2x.png` | `031498ca` | waifu2x 超分 |
| `final/nianzhen_sheet_3840_lanczos.png` | `d38d4c61` | 插值对照 |
| `compare/upscale_compare_overview.png` | `b28ea17c` | 五版整图并排 |
| `compare/upscale_compare_eyes_1to1.png` | `932994aa` | 眼部 1:1 五列 |
| `compare/upscale_compare_knit_1to1.png` | `e740cf79` | 针织 1:1 五列 |
| `compare/upscale_compare_hair_1to1.png` | `429c6010` | 发丝 1:1 五列 |
| `compare/upscale_zoom_eye_2x.png` | `fd5f4445` | 眼部 2× 放大 |
| `compare/upscale_zoom_knit_2x.png` | `c639c8a5` | 针织 2× 放大 |
| `compare/nianzhen_compare_upscale_eyes.png` | `b1f9c0eb` | 早期三联对照（插值/ESRGAN/waifu2x） |
| `site/nz-anchor-sheet.webp` | `26926edd` | 站点锚点图（1600 宽） |
| `site/nz-upscale-01-eyes.png` | `537fa9af` | 站点对比图 ① |
| `site/nz-upscale-02-knit.png` | `d4e596ee` | 站点对比图 ② |
| `site/nz-upscale-03-hair.png` | `24e7e361` | 站点对比图 ③ |
| `scenes/nianzhen_nightread_lookup_1012x1348.png` | `9f91c8ae` | 夜读·台灯下抬头 3:4（2026-11-04 生成） |
| `scenes/nianzhen_nightread_lookup_1254x1254.png` | `a9678df7` | 夜读·台灯下抬头 1:1（2026-11-04 生成） |
| `scenes/nianzhen_nightread_lookup_1448x1086.png` | `409a078a` | 夜读·台灯下抬头 4:3（2026-11-09 生成） |
| `sheets/nianzhen_character_sheet_1312x1199.png` | `0b9f4cc3` | 一页设定稿原图 |
| `sheets/nianzhen_expressions_9up_1254x1254.png` | `239ba6fe` | 九宫格表情第一版 |
| `sheets/nianzhen_expressions_9up_notes.txt` | `e28ab62b` | 九宫格备注原文 449 B |

---

## 九、设定稿与表情表（站点 02/03/04 图位的来源）

站点 `yen-chiu.github.io` 的角色设定页把这两张表裁成了单格：

| 站点图位 | 取自 | 裁切框（原图坐标） |
|---|---|---|
| 02a 正视 | 设定稿左侧全身 | `98,18 → 333,842`，补背景到 1:2，出 500×1000 |
| 02b 三分之四侧 | 设定稿第二身 | `362,18 → 554,834`，补背景到 1:2，出 500×1000 |
| 03a–03f 表情 | 九宫格第 1/3/5/6/8/9 格（平静、真笑、嘴硬、困倦、惊讶、戏谑） | 每格 418×418，出 420×420，站点排 3+3 |
| 04a 一字夹 | 设定稿右列发夹细节 | `1109,397 → 1263,543`，出 420×420 |
| 04b 酒窝 | 设定稿中央面部 | `705,305 → 945,545`，出 420×420 |
| 04e 耳圈 | 设定稿右列耳部细节 | `1109,205 → 1279,377`，出 420×420 |

补背景的做法：全身格把人裁到最紧后，用**右缘 5 列的中位色按行平铺**补到 1:2——用纯背景色平涂会在接缝处露出一条色差，用边缘复制则会把人物衣服的颜色拖成竖条。

**没上站的部分**：设定稿只有正视和三分之四侧，`02c 背视` 仍是空位；细节栏的「指节铅笔灰」「口袋里的糖」两张表里也没有，`04c/04d` 留空。

出图 prompt 里该补的负面词：`three-quarter view, back view` 之外，背视要单独写 `back view, nape of the neck`，否则模型会退回三分之四。

