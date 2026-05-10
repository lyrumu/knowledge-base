# PatPat 模组 — 资源包制作指南

> 结合 [PatPat 官方 Wiki](https://github.com/LopyMine/PatPat/wiki/Getting-Started-%E2%80%A2-About-Custom-Animations) 与实际操作，涵盖两种修改方式。

---

## 目录

1. [两种修改方式](#两种修改方式)
2. [PatPat 模组资产结构](#patpat-模组资产结构)
3. [前置条件](#前置条件)
4. [方式 A：替换默认动画（简单）](#方式-a替换默认动画)
   - [A1. 确定 pack_format](#a1-确定-pack_format)
   - [A2. 处理纹理](#a2-处理纹理)
   - [A3. 处理音效](#a3-处理音效)
   - [A4. 编写 pack.mcmeta](#a4-编写-packmcmeta)
   - [A5. 打包 ZIP](#a5-打包-zip)
5. [方式 B：自定义动画配置（高级）](#方式-b自定义动画配置)
   - [B1. 动画配置文件格式](#b1-动画配置文件格式)
   - [B2. 配置字段详解](#b2-配置字段详解)
   - [B3. 优先级系统](#b3-优先级系统)
   - [B4. 自定义音效注册](#b4-自定义音效注册)
   - [B5. 完整示例](#b5-完整示例)
6. [获取原版 Minecraft 素材](#获取原版-minecraft-素材)
7. [官方模板资源包](#官方模板资源包)
8. [常见踩坑](#常见踩坑)
9. [参考链接](#参考链接)

---

## 两种修改方式

|           | 方式 A：替换默认资产            | 方式 B：自定义动画配置                    |
| --------- | ---------------------- | ------------------------------- |
| **原理**    | 直接覆盖 PatPat 默认的纹理和音效文件 | 通过 JSON 配置文件添加新动画，可指定实体、触发者、优先级 |
| **适用场景**  | 修改所有生物的抚摸效果            | 为特定实体/玩家制作专属动画                  |
| **配置复杂度** | 低（只改文件不改配置）            | 中（需要编写 `.json` / `.json5` 配置）   |
| **灵活性**   | 一种动画通用于所有生物            | 可同时存在多个动画，按实体类型/名称/UUID 匹配      |

> 两种方式可以**共存** —— 方式 B 的动画会在匹配到特定实体时覆盖方式 A 的默认效果。

---

## PatPat 模组资产结构

从 `PatPat-1.2.6+26.1+fabric.jar` 解压得到：

```
assets/patpat/
├── sounds.json                     # 默认音效注册表
├── sounds/
│   ├── pat.ogg     (9KB)           # 抚摸音效变体 1
│   ├── pat1.ogg    (9KB)           # 抚摸音效变体 2
│   ├── pat2.ogg    (9KB)           # 抚摸音效变体 3
│   ├── lopi.ogg    (16KB)          # 彩蛋音效变体 1
│   ├── lopi1.ogg   (15KB)          # 彩蛋音效变体 2
│   ├── lopi2.ogg   (17KB)          # 彩蛋音效变体 3
│   └── lopi3.ogg   (17KB)          # 彩蛋音效变体 4
├── textures/
│   ├── default/patpat.png          # 默认动画纹理（560×112，5帧）
│   ├── cape/patpat_cape_hand.png   # 披风纹理（64×32）
│   ├── config/                     # 配置界面图标
│   └── easter/egg.json             # 内置彩蛋配置（山羊 "Снежа"）
└── lang/                           # 140+ 语言文件
```

**默认纹理规格**：

| 属性  | 值                             |
| --- | ----------------------------- |
| 文件  | `textures/default/patpat.png` |
| 尺寸  | 560 × 112（5 帧精灵图）             |
| 每帧  | 112 × 112                     |
| 格式  | PNG, RGBA                     |

**默认音效规格**：

| 属性  | 值                                          |
| --- | ------------------------------------------ |
| 文件  | `sounds/pat.ogg` / `pat1.ogg` / `pat2.ogg` |
| 格式  | OGG Vorbis, **单声道**                        |
| 采样率 | 44100 Hz                                   |

`sounds.json` 内容：

```json
{
    "patpat": { "sounds": ["patpat:pat", "patpat:pat1", "patpat:pat2"] },
    "lopi":   { "sounds": ["patpat:lopi", "patpat:lopi1", "patpat:lopi2", "patpat:lopi3"] }
}
```

---

## 前置条件

| 工具                                          | 用途                               |
| ------------------------------------------- | -------------------------------- |
| 图像编辑器（GIMP / Aseprite / Photoshop / Pillow） | 制作/编辑 PNG 纹理                     |
| Audacity 或在线转换器                             | 导出 OGG Vorbis 单声道音效（**不能只改后缀名**） |
| 7-Zip / Python zipfile                      | 打包 ZIP                           |
| 浏览器                                         | 访问 Mojang API 获取原版素材             |

---

## 方式 A：替换默认动画

> 直接覆盖 `patpat.png` 和 `pat*.ogg`，改变**所有生物**的抚摸效果。这是我们实际操作中采用的方式。

### A1. 确定 pack_format

`pack_format` 是 Minecraft 判断资源包兼容性的版本号。**错误的值会导致资源包不显示或不兼容。**

| Minecraft 版本 | pack_format |
| ------------ | ----------- |
| 1.21.1       | 34          |
| 1.21.4       | 46          |
| 1.21.5       | 55          |
| **26.1**     | **84**      |

**自查方法**：

- 游戏内 `F3 + V`：右侧显示当前支持的 pack format
- [Minecraft Wiki 完整对照表](https://minecraft.wiki/w/Template:Resource_pack_format)

```bash
# API 查询（以 26.1 为例）
curl -s "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json" \
  | jq -r '.versions[] | select(.id=="26.1") | .url' \
  | xargs curl -s | jq '.pack_version.resource'
# 输出: {"resource": 84, "data": 103}
```

### A2. 处理纹理

目标路径：`assets/patpat/textures/default/patpat.png`

必须为 **560 × 112** 的精灵图（5 帧 × 112×112）。

**示例：倒置末地烛**（Python / Pillow）：

```python
from PIL import Image, ImageOps

# 加载原版末地烛纹理（16×16）
src = Image.open("end_rod.png")

# 垂直翻转 → 倒置
flipped = ImageOps.flip(src)

# 缩放到 112×112（NEAREST 保留像素风格）
frame = flipped.resize((112, 112), Image.NEAREST)

# 平铺 5 帧 → 560×112
spritesheet = Image.new("RGBA", (560, 112))
for i in range(5):
    spritesheet.paste(frame, (i * 112, 0))

spritesheet.save("patpat.png")
```

> 也可以用 Aseprite 逐帧绘制真正的动画（而非 5 帧相同），参考 [官方 Wiki：Creating Animation Texture](https://github.com/LopyMine/PatPat/wiki/Creating-Animation-Texture)。

### A3. 处理音效

目标路径：`assets/patpat/sounds/pat.ogg` / `pat1.ogg` / `pat2.ogg`

```bash
# 从原版素材复制（以史莱姆音效为例）
cp slime_big1.ogg   pat.ogg
cp slime_big2.ogg   pat1.ogg
cp slime_small1.ogg pat2.ogg
```

**格式验证**：

```bash
file pat.ogg
# 期望: Ogg data, Vorbis audio, mono, 44100 Hz
# ❌ 如果是 stereo → 用 Audacity 重新导出为 Mono
```

### A4. 编写 pack.mcmeta

```json
{
  "pack": {
    "description": "PatPat × 倒置末地烛 + 史莱姆音效",
    "pack_format": 84,
    "supported_formats": 84
  }
}
```

### A5. 打包 ZIP

#### ⚠️ 最常见的错误：ZIP 多了一层文件夹

```
❌ 错误：
my_pack.zip
└── MyPack/                  ← 多余！
    ├── pack.mcmeta
    └── assets/...

✅ 正确：
my_pack.zip
├── pack.mcmeta              ← 必须在 ZIP 根层级
└── assets/
    └── patpat/
        ├── textures/default/patpat.png
        └── sounds/...
```

#### 验证 ZIP 结构

```bash
python3 -c "
import zipfile
with zipfile.ZipFile('my_pack.zip', 'r') as zf:
    for name in zf.namelist():
        print(name)
"
# 第一行必须是 pack.mcmeta
```

#### Python 打包脚本

```python
import zipfile, os

src_dir = "my_pack_folder"  # 源文件夹
with zipfile.ZipFile("my_pack.zip", "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            fp = os.path.join(root, f)
            arcname = os.path.relpath(fp, src_dir)
            zf.write(fp, arcname)
```

---

## 方式 B：自定义动画配置

> PatPat 支持通过 JSON 配置文件创建**专属动画**，可精确控制哪些实体触发、谁可以触发、动画参数等。这是官方 Wiki 的核心内容。

根据 [PatPat Wiki — Creating Animation Config](https://github.com/LopyMine/PatPat/wiki/Creating-Animation-Config)，你需要三个文件：

| 文件                           | 必需    | 说明                     |
| ---------------------------- | ----- | ---------------------- |
| 动画纹理 `.png`                  | ✅     | 精灵图（所有帧放一张图）           |
| 动画配置 `.json` / `.json5`      | ✅     | 定义纹理路径、帧数、持续时间、实体匹配规则等 |
| 自定义音效 `.ogg` + `sounds.json` | ❌（可选） | 注册新音效事件                |

配置文件的存放位置：`assets/patpat/` 下的**任意子目录**。

### B1. 动画配置文件格式

参考 [官方示例配置](https://github.com/LopyMine/PatPat/blob/master/src/main/resources/example/example_custom_animation_config.json5)：

```json5
// animated_piston.json5（文件名随意，后缀 .json 或 .json5）
{
    "version": "1.0.0",           // 配置版本（必需）
    "priority": 10,               // 优先级（可选，默认 0）
    "blacklist": false,           // true=黑名单 / false=白名单（可选，默认 false）
    "animation": {
        "texture": "patpat:textures/animated_piston.png",
        "duration": 300,          // 动画时长（ms）
        "frame": {
            "totalFrames": 5,     // 总帧数
            "scaleX": 1.0,        // X 轴缩放（默认 0.9）
            "scaleY": 1.0,        // Y 轴缩放（默认 0.9）
            "offsetX": 0.0,       // X 轴偏移（默认 0）
            "offsetY": 0.0,       // Y 轴偏移（默认 0）
            "offsetZ": 0.0        // Z 轴偏移（默认 0）
        },
        "sound": {
            "id": "patpat:my_custom_sound_id",
            "minPitch": 0.5,
            "maxPitch": 1.5,
            "volume": 0.8
        }
    },
    "entities": [
        // 指定实体（可以是类型字符串或 entity 对象）
        "minecraft:zombie",
        {
            "id": "minecraft:sheep",
            "name": "Jeb_",                       // 仅匹配名为 "Jeb_" 的羊
            "from": {
                "name": "LopyMine"                // 仅 LopyMine 抚摸时触发
            }
        }
    ]
}
```

### B2. 配置字段详解

以下内容来自 [PatPat Wiki: Creating Animation Config](https://github.com/LopyMine/PatPat/wiki/Creating-Animation-Config)，标注 ✅ 为必需项。

#### 主选项

| 字段           | 类型      | 默认值     | 说明                           |
| ------------ | ------- | ------- | ---------------------------- |
| `version` ✅  | String  | —       | 配置版本号（如 `"1.0.0"`），用于未来兼容处理  |
| `priority`   | Integer | `0`     | 优先级，范围建议 [-10000, 10000]     |
| `blacklist`  | Boolean | `false` | `true`=黑名单模式 / `false`=白名单模式 |
| `entities` ✅ | Array   | —       | 实体匹配列表，设为 `"all"` 匹配所有实体     |

#### `animation` 对象

| 字段           | 类型      | 默认值 | 说明                                                       |
| ------------ | ------- | --- | -------------------------------------------------------- |
| `texture` ✅  | String  | —   | 纹理路径，如 `"patpat:textures/xxx.png"`。纹理必须在 `textures/` 目录下 |
| `duration` ✅ | Integer | —   | 动画持续时间（毫秒），不可为负                                          |
| `frame` ✅    | Object  | —   | 帧设置                                                      |
| `sound` ✅    | Object  | 无   | 音效设置                                                     |

#### `frame` 对象

| 字段              | 类型      | 默认值 | 说明      |
| --------------- | ------- | --- | ------- |
| `totalFrames` ✅ | Integer | —   | 纹理中的总帧数 |
| `scaleX`        | Double  | 0.9 | X 轴缩放比例 |
| `scaleY`        | Double  | 0.9 | Y 轴缩放比例 |
| `offsetX`       | Double  | 0.0 | X 轴偏移   |
| `offsetY`       | Double  | 0.0 | Y 轴偏移   |
| `offsetZ`       | Double  | 0.0 | Z 轴偏移   |

#### `sound` 对象

| 字段         | 类型     | 默认值 | 说明                          |
| ---------- | ------ | --- | --------------------------- |
| `id` ✅     | String | —   | 音效 ID，如 `"patpat:my_sound"` |
| `minPitch` | Double | 1.0 | 最小音高                        |
| `maxPitch` | Double | 1.0 | 最大音高                        |
| `volume`   | Double | 1.0 | 音量                          |

#### `entity` 对象（`entities` 数组中每个元素可以是字符串或对象）

| 字段          | 类型     | 说明                                |
| ----------- | ------ | --------------------------------- |
| `id`        | String | 实体类型，如 `"minecraft:pig"`          |
| `name`      | String | 实体**名称**（不是类型名），如 `"My Cute Dog"` |
| `uuid`      | String | 实体 UUID                           |
| `from.name` | String | 触发者玩家名                            |
| `from.uuid` | String | 触发者玩家 UUID                        |

### B3. 优先级系统

> 来源：[PatPat Wiki — priority](https://github.com/LopyMine/PatPat/wiki/Creating-Animation-Config#priority-)

当玩家抚摸实体时，PatPat 按以下顺序选择动画：

1. 筛选匹配当前**实体类型** / **实体名称** / **实体 UUID** 的动画
2. 如果多个动画匹配同一实体：
   - 不同资源包中 → 使用**资源包列表靠上**的
   - 同一资源包中 → 使用 `priority` 值**更高**的
   - `priority` 相同时 → 按**文件路径**字母序排列

### B4. 自定义音效注册

> 来源：[PatPat Wiki — Adding Animation Sound(s)](https://github.com/LopyMine/PatPat/wiki/Adding-Animation-Sound\(s\))

如果要使用**新音效**（而非 PatPat 内置的 `patpat:patpat` 音效事件），需要注册：

1. 将 `.ogg` 文件放入 `assets/patpat/sounds/`
2. 创建/编辑 `assets/patpat/sounds.json`：

```json
{
    "my_custom_sound_id": {
        "sounds": ["patpat:my_sound_file_name"]
    }
}
```

3. 在动画配置中引用：

```json
"sound": {
    "id": "patpat:my_custom_sound_id",
    "minPitch": 0.8,
    "maxPitch": 1.2,
    "volume": 1.0
}
```

> ⚠️ 如果 `sounds.json` 格式有误，**整个文件会被忽略**。使用 JSON 校验器检查。

### B5. 完整示例

以下是一个为僵尸定制活塞动画的资源包结构：

```
MyPatPatAnimation/
├── pack.mcmeta
└── assets/
    └── patpat/
        ├── textures/
        │   └── animated_piston.png         # 活塞精灵图
        ├── sounds/
        │   └── piston_sound.ogg             # 自定义音效
        ├── sounds.json                       # 音效注册
        └── my_animations/
            └── animated_piston.json5         # 动画配置
```

对应的 `pack.mcmeta`：

```json
{
  "pack": {
    "description": "PatPat × 自定义活塞动画",
    "pack_format": 84,
    "supported_formats": 84
  }
}
```

---

## 获取原版 Minecraft 素材

如果希望借用原版 Minecraft 纹理或音效（如末地烛、史莱姆声音），可从 Mojang 官方服务器下载。

### 从 Asset Index 获取

```bash
# 1. 获取版本元数据
VER="26.1"
VER_URL=$(curl -s "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); \
    [print(v['url']) for v in d['versions'] if v['id']=='$VER']")

# 2. 获取 asset index URL
ASSET_IDX=$(curl -s "$VER_URL" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['assetIndex']['url'])")

# 3. 搜索目标文件
curl -s "$ASSET_IDX" | python3 -c "
import sys,json
d=json.load(sys.stdin)
for path, info in d['objects'].items():
    if 'end_rod' in path or 'slime' in path:
        print(f'{path} -> {info[\"hash\"]}')
"
```

输出示例：

```
minecraft/textures/block/end_rod.png -> <sha1_hash>
minecraft/sounds/mob/slime/big1.ogg -> b5eca1979e69271b2065ac67ba2c37b5afac0f98
```

### 下载文件

```
https://resources.download.minecraft.net/{hash前2位}/{完整hash}
```

```bash
# 例
curl -o big1.ogg \
  "https://resources.download.minecraft.net/b5/b5eca1979e69271b2065ac67ba2c37b5afac0f98"
```

### 从客户端 JAR 提取（纹理）

部分纹理也可直接从客户端 JAR 解压：

```bash
curl -o client.jar "<version.json 中 downloads.client.url>"
unzip client.jar "assets/minecraft/textures/block/end_rod.png"
```

---

## 官方模板资源包

PatPat 官方提供了[模板资源包](https://github.com/LopyMine/PatPat/blob/master/img/wiki/custom_animations/Template%20Custom%20Animation.zip)，结构如下：

```
Template Custom Animation/
├── pack.mcmeta
└── assets/
    └── patpat/
        ├── sounds.json
        ├── sounds/
        └── texture/
```

可以直接下载后修改。官方 Wiki 也有一个[成品示例](https://github.com/LopyMine/PatPat/wiki/Ready%E2%80%90To%E2%80%90Use-Resource-Pack)（活塞动画资源包）。

---

## 常见踩坑

| 症状                          | 原因                             | 解决                             |
| --------------------------- | ------------------------------ | ------------------------------ |
| 资源包**不显示**在列表中              | `pack_format` 版本号不对            | 用 `F3+V` 确认当前版本值               |
| 显示但标记**"不兼容"**              | `pack_format` 太低（如 34 用于 26.1） | 更新为正确值（26.1 = 84）              |
| 显示**"已损坏"**                 | ZIP 根结构错误 / JSON 语法错误          | `pack.mcmeta` 必须在 ZIP 根层级      |
| 纹理显示异常                      | 尺寸不匹配                          | 默认纹理必须 560×112；自定义动画纹理可任意尺寸    |
| 音效**无声**                    | OGG 是立体声而非单声道                  | Audacity → 导出 Mono             |
| `sounds.json` 内所有音效**全部失效** | JSON 格式错误（缺少逗号/引号）             | 用 JSON 校验器检查语法                 |
| 自定义动画**不生效**                | 实体匹配规则不满足 / `version` 字段缺失     | 检查 `entities` 配置和 `version` 字段 |
| `F3+T` 重载后不变                | 未启用资源包或优先级太低                   | 选项→资源包 → 移到列表顶部                |

### 调试快捷键

| 快捷键      | 作用                                      |
| -------- | --------------------------------------- |
| `F3 + V` | 显示当前支持的 pack_format / data pack version |
| `F3 + T` | 重新加载所有资源包（无需重启游戏）                       |

---

## 参考链接

| 资源                             | 链接                                                                                                              |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| PatPat 官方 Wiki — 入门            | https://github.com/LopyMine/PatPat/wiki/Getting-Started-%E2%80%A2-About-Custom-Animations                       |
| PatPat Wiki — 创建动画纹理           | https://github.com/LopyMine/PatPat/wiki/Creating-Animation-Texture                                              |
| PatPat Wiki — 创建动画配置           | https://github.com/LopyMine/PatPat/wiki/Creating-Animation-Config                                               |
| PatPat Wiki — 添加音效             | https://github.com/LopyMine/PatPat/wiki/Adding-Animation-Sound(s)                                               |
| PatPat Wiki — 模板资源包            | https://github.com/LopyMine/PatPat/wiki/Template-Resource-Pack                                                  |
| PatPat 官方配置示例                  | https://github.com/LopyMine/PatPat/blob/master/src/main/resources/example/example_custom_animation_config.json5 |
| PatPat 模组源码                    | https://github.com/LopyMine/PatPat                                                                              |
| Minecraft Wiki — Pack format   | https://minecraft.wiki/w/Pack_format                                                |
| Minecraft Wiki — pack.mcmeta   | https://minecraft.wiki/w/Pack.mcmeta                                                                            |
| Minecraft Wiki — Resource Pack | https://minecraft.wiki/w/Resource_Pack                                                                          |
| Minecraft Wiki — sounds.json   | https://minecraft.wiki/w/Sounds.json                                                                            |
| Mojang 版本清单 API                | https://piston-meta.mojang.com/mc/game/version_manifest_v2.json                                                 |
| Mojang 资源 CDN                  | https://resources.download.minecraft.net/                                                                       |
| Fabric 官方文档                    | https://docs.fabricmc.net/                                                                                      |

---

> **本文档结合 [PatPat 官方 Wiki](https://github.com/LopyMine/PatPat/wiki)（2024-2025）与实际操作验证**，在 Minecraft 26.1（Fabric）上测试通过。


