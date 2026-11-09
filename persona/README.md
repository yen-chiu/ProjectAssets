# persona · 人物素材

`ProjectAssets` 里的人物素材。一个人一个目录，目录内部自洽——原图、切格、成品、对比、脚本、站点交付各占一层，加人不用动已有的。

```
persona/
  README.md            这份索引
  nianzhen/            念真
    README.md          素材包说明：三格怎么来的、超分选型、溯源
    prompt-v3.md       出图提示词 + 人设速查
    source/            两次生成的整张原片
    panels/            切好的三格
    final/             母版 1920 与四个 3840 版本
    compare/           超分对比条与整图并排
    scripts/           拼版、切格、量测脚本
    site/              站点正在用的那一组（webp / png）
```

## 约定

- **目录名用角色 id**，与站点 `chat/assets/persona/nianzhen.json` 的 `id` 一致，别用中文名当目录。
- **文件名写清版本与参数**：`<角色>_<内容>_<尺寸>_<模型>_<参数>.<ext>`，例如 `nianzhen_sheet_3840_realcugan_up2x-nodenoise.png`。看文件名就知道哪一版、用什么放大的，不用翻 README。
- **只收成品与原片**，中间临时文件（`__pycache__`、跑废的试出图）不入库。
- **站点用的那份再留一份在 `site/`**：`yen-chiu.github.io/assets/img/persona/` 是发布用的，这里是母本备份；两处同名，同步时直接覆盖。
- 每个包的 README 必须写三件事：**用哪张、怎么复现、sha256 前 8 位**。

## 现有

| 目录 | 角色 | 内容 |
| --- | --- | --- |
| `nianzhen/` | 念真 | 三格定妆照锚点（3840×2560）+ 四版超分对比 + 出图 prompt v3 |
