# persona · 人物素材

`ProjectAssets` 里的人物素材。一个人一个目录，目录内部自洽：原片、站点交付、切格和索引各占一层。

```
persona/
  README.md            这份索引
  nianzhen/            念真
    README.md          素材包说明：用哪张、怎么复现、sha256
    prompt-v4.md       2026-11-16 版出图 prompt
    manifest.json      35 张的索引与哈希
    source/            选中原片（PNG）
    site/              站点交付（WebP）
    crops/             表情与细节切格
```

## 约定

- **目录名用角色 id**，与站点 `_tabs/persona.md` 的 `permalink` / 角色 id 对应，不用中文名当目录。
- **文件名写内容，不写版本号**：`nz-<slug>.webp`，slug 与 `manifest.json` 一致。换图时同名覆盖，旧文件直接删，不留 `-v2`、`-final`。
- **原片只留选中的**：同场景多版只收最终采用的那张；被替换的旧版本不进入 `source/`。
- **`site/` 是站点发布目录的母本**：与 `yen-chiu.github.io/assets/img/persona/` 同名同步，改完两边一起换。
- **每个包的 README 必须写三件事**：用哪张、怎么复现、sha256 前 8 位。

## 现有

| 目录 | 角色 | 内容 |
| --- | --- | --- |
| `nianzhen/` | 念真 | 2026-11 重画版：35 张原片、52 张站点 WebP、17 张切格、prompt v4 |
