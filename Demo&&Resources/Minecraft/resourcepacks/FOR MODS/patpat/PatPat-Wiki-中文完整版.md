# PatPat 官方 Wiki — 中文完整翻译

> 来源：https://github.com/LopyMine/PatPat/wiki
> 
> 翻译整理时间：2026-05-10 | 对应 Wiki 版本：2024-2025

---

## 目录

1. [入门：关于自定义动画](#1-入门关于自定义动画)
2. [创建动画纹理](#2-创建动画纹理)
3. [创建动画配置](#3-创建动画配置)
   - [3.1 主选项](#31-主选项)
   - [3.2 "animation" 对象](#32-animation-对象)
   - [3.3 "frame" 对象](#33-frame-对象)
   - [3.4 "sound" 对象](#34-sound-对象)
   - [3.5 "entity" 对象](#35-entity-对象)
   - [3.6 "from" 对象](#36-from-对象)
   - [3.7 创建你自己的动画配置](#37-创建你自己的动画配置)
4. [添加动画音效](#4-添加动画音效)
   - [4.1 从 MP3 转换为 OGG](#41-从-mp3-转换为-ogg)
   - [4.2 注册音效](#42-注册音效)
5. [模板资源包](#5-模板资源包)
6. [成品资源包](#6-成品资源包)
7. [附录：完整示例配置文件](#7-附录完整示例配置文件)

---

## 1. 入门：关于自定义动画

> 原文：[Getting Started • About Custom Animations](https://github.com/LopyMine/PatPat/wiki/Getting-Started-%E2%80%A2-About-Custom-Animations)

PatPat 模组的自定义动画可以通过原版资源包机制创建。你的资源包包含三个主要文件：

| 文件                                                                                         | 是否必需     | 说明                    |
| ------------------------------------------------------------------------------------------ | -------- | --------------------- |
| 动画纹理 ![必需](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/required.png) | **✅ 必需** | 包含所有动画帧的精灵图           |
| 动画配置 ![必需](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/required.png) | **✅ 必需** | JSON/JSON5 文件，定义动画参数  |
| 动画音效 ![可选](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/optional.png) | ❌ 可选     | 自定义音效及 sounds.json 注册 |

我们试试为 PatPat 模组创建一个自定义动画资源包。

> 建议先下载[模板资源包](#5-模板资源包)开始，但这并非必需。

---

## 2. 创建动画纹理

> 原文：[Creating Animation Texture](https://github.com/LopyMine/PatPat/wiki/Creating-Animation-Texture)

自定义动画的核心要素之一是**动画纹理**。简言之，纹理就是把所有动画帧存放在一张 `.png` 文件中。

让我们创建一个包含 2D 活塞动画的纹理。

**第 1 步**：首先获取活塞侧面纹理（我从 Minecraft 资产中获得的）：

![获取活塞纹理](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/creating_animation_texture/creating_animation_texture_0.png)

**第 2 步**：打开它，旋转并添加一些帧：

> *我会使用 Aseprite 来操作，你可以用任何其他图像编辑软件*

![编辑纹理](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/creating_animation_texture/creating_animation_texture_1.png)

**第 3 步**：逐帧制作动画：

![逐帧动画 1](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/creating_animation_texture/creating_animation_texture_2.png)
![逐帧动画 2](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/creating_animation_texture/creating_animation_texture_3.png)

**第 4 步**：保存纹理，完成！

![保存结果](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/creating_animation_texture/creating_animation_texture_4.png)

> 确认你的最终纹理文件是一个精灵图（spritesheet），所有帧水平排列在一张 PNG 中。

---

## 3. 创建动画配置

> 原文：[Creating Animation Config](https://github.com/LopyMine/PatPat/wiki/Creating-Animation-Config)

现在需要为动画创建**配置文件**。配置只能是 `.json` 或 `.json5` 格式。你可以将此文件放在 `assets/patpat/` 下的**任何子文件夹**中。

PatPat 模组提供了一个[示例配置](https://github.com/LopyMine/PatPat/blob/master/src/main/resources/example/example_custom_animation_config.json5)，含有所有选项。

下面详细介绍每个选项的用途：

---

### 3.1 主选项

#### `version` ![必需](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/required.png)

> 始于：`1.0.0` | 类型：`String` | 示例：`1.5.2`

表示配置文件的版本。这很有必要，以便将来模组能处理旧的配置选项。填写一个不带空格、以点号分隔的三个数字组成的字符串。

---

#### `priority` ![可选](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/optional.png)

> 始于：`1.0.0` | 类型：`Integer` | 示例：`10` | 默认值：`0`

表示自定义动画的优先级。填写 `-2147483648` 到 `2147483647` 之间的整数。

> 尽量避免使用最小值和最大值，范围 [-10000, 10000] 完全够用！

<details>
<summary><b>优先级如何工作？</b>（点击展开）</summary>

每个自定义动画都有自己的优先级。当玩家与一个实体交互时，第一个满足以下三个条件的自定义动画将被使用：

- 实体类型
- 实体名称
- 实体 UUID

如果有多个自定义动画满足这些条件，则按以下规则排序：

1. 如果自定义动画来自**不同**的资源包，则使用资源包列表中**位置更靠上**的那个。
2. 如果自定义动画来自**同一**资源包，则使用 `priority` 值**更高**的那个。
3. 如果 `priority` 相同，则按文件路径字母序排序。

</details>

---

#### `animation` ![必需](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/required.png)

> 始于：`1.0.0` | 详见 [3.2 "animation" 对象](#32-animation-对象)

包含动画设置，如持续时间、音效等。

---

#### `blacklist` ![可选](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/optional.png)

> 始于：`1.0.0` | 类型：`Boolean` | 示例：`false` 或 `true` | 默认值：`false`

将 `entities` 列表切换为白名单模式（`false`）或黑名单模式（`true`）。

- 如果为 `true`，则列表作为**黑名单**——接受所有实体，除了 `entities` 列表中列出的。
- 如果为 `false`，则列表作为**白名单**——只接受 `entities` 列表中列出的实体。

---

#### `entities` ![必需](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/required.png)

> 始于：`1.0.0` | 详见 [3.5 "entity" 对象](#35-entity-对象)

包含此动画将生效的实体列表。可以设置为 `"all"` 来选择所有实体。

---

### 3.2 "animation" 对象

#### `texture` ![必需](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/required.png)

> 始于：`1.0.0` | 类型：`String` | 示例：`patpat:textures/path/to/texture.png`

包含动画播放时将使用的纹理路径。

> **注意**：所有动画纹理必须放在 `textures/` 文件夹内，因为模组只在此文件夹中查找纹理！

---

#### `duration` ![必需](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/required.png)

> 始于：`1.0.0` | 类型：`Integer` | 示例：`300`

表示动画持续时间，单位为毫秒（ms）。不能为负数。

---

#### `frame` ![必需](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/required.png)

> 始于：`1.0.0` | 详见 [3.3 "frame" 对象](#33-frame-对象)

包含帧设置，如总帧数、偏移量、缩放等。

---

#### `sound` ![可选](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/optional.png)

> 始于：`1.0.0` | 详见 [3.4 "sound" 对象](#34-sound-对象)

指定动画播放时伴随的音效，以及可选的音高和音量范围。

---

### 3.3 "frame" 对象

#### `totalFrames` ![必需](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/required.png)

> 始于：`1.0.0` | 类型：`Integer` | 示例：`5`

表示纹理中的总帧数。

---

#### `scaleX` ![可选](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/optional.png)

> 始于：`1.0.0` | 类型：`Double` | 示例：`1.5` | 默认值：`0.9`

表示纹理在 X 轴上的缩放。例如，如果值为 `2.0`，则纹理将放大两倍。

---

#### `scaleY` ![可选](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/optional.png)

> 始于：`1.0.0` | 类型：`Double` | 示例：`1.5` | 默认值：`0.9`

表示纹理在 Y 轴上的缩放。例如，如果值为 `2.0`，则纹理将放大两倍。

---

#### `offsetX` ![可选](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/optional.png)

> 始于：`1.0.0` | 类型：`Double` | 示例：`-1.5` | 默认值：`0.0`

表示纹理在 X 轴上的偏移量。

---

#### `offsetY` ![可选](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/optional.png)

> 始于：`1.0.0` | 类型：`Double` | 示例：`1.5` | 默认值：`0.0`

表示纹理在 Y 轴上的偏移量。

---

#### `offsetZ` ![可选](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/optional.png)

> 始于：`1.0.0` | 类型：`Double` | 示例：`-1.5` | 默认值：`0.0`

表示纹理在 Z 轴上的偏移量。

---

### 3.4 "sound" 对象

#### `id` ![必需](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/required.png)

> 始于：`1.0.0` | 类型：`String` | 示例：`patpat:pat_sound`

表示音效 ID。

---

#### `minPitch` ![可选](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/optional.png)

> 始于：`1.0.0` | 类型：`Double` | 示例：`1.5` | 默认值：`1.0`

表示音效的最小音高值。

> **注意**：在示例配置中也写作 `min_pitch`（下划线格式），两者均可。

---

#### `maxPitch` ![可选](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/optional.png)

> 始于：`1.0.0` | 类型：`Double` | 示例：`1.5` | 默认值：`1.0`

表示音效的最大音高值。

> **注意**：在示例配置中也写作 `max_pitch`（下划线格式），两者均可。

---

#### `volume` ![可选](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/optional.png)

> 始于：`1.0.0` | 类型：`Double` | 示例：`1.5` | 默认值：`1.0`

表示音效的音量。

---

### 3.5 "entity" 对象

> `entities` 数组中的每个元素可以是字符串（仅 `id`）或带有更多筛选条件的对象。

#### `id` ![可选](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/optional.png)

> 始于：`1.0.0` | 类型：`String` | 示例：`minecraft:pig`

表示实体类型。如果此字段不存在，PatPat 模组会跳过此项比较。

---

#### `name` ![可选](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/optional.png)

> 始于：`1.0.0` | 类型：`String` | 示例：`My Cute Dog`

表示**实体名称**。实体名称指的是实体被命名的名字，而非实体类型名。例如，我把我的狗命名为 `My Cute Dog`，我只想对这个名字的实体使用动画，那就把 `My Cute Dog` 写在这里。

---

#### `uuid` ![可选](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/optional.png)

> 始于：`1.0.0` | 类型：`String` | 示例：`192e3748-12d5-4573-a8a5-479cd394a1dc`

表示实体 UUID。通常你会用它来为某个特定的玩家指定动画，因为每个玩家有唯一的 UUID。例如，只想对玩家 `LopyMine` 使用动画，把他的 UUID 写在这里。

---

#### `from` ![可选](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/optional.png)

> 始于：`1.0.0` | 详见 [3.6 "from" 对象](#36-from-对象)

指定谁可以触发此动画。例如，有两个玩家，但动画只应在其中一人抚摸狗时触发，就可以在此配置。

---

### 3.6 "from" 对象

#### `name` ![可选](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/optional.png)

> 始于：`1.0.0` | 类型：`String` | 示例：`nikita51`

表示可以使用此动画的玩家名。例如，你想要一个动画**只有你**抚摸别人时才生效，那就把你的昵称写在这里。

---

#### `uuid` ![可选](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/optional.png)

> 始于：`1.0.0` | 类型：`String` | 示例：`192e3748-12d5-4573-a8a5-479cd394a1dc`

表示玩家 UUID。和 `name` 功能相同，但使用 UUID。

---

### 3.7 创建你自己的动画配置

**第 1 步**：基于[这个示例配置](https://github.com/LopyMine/PatPat/blob/master/src/main/resources/example/example_custom_animation_config.json5)，创建我们自己的简单配置文件：

`animated_piston.json5`

```json5
{
    "version": "1.0.0",
    "animation": {
        "texture": "patpat:textures/animated_piston_texture.png",
        "duration": 300,
        "frame": {
            "totalFrames": 5,
            "scaleX": 1,
            "scaleY": 1,
            "offsetX": 0,
            "offsetY": 0,
            "offsetZ": 0
        }
    },
    "entities": [
        "minecraft:zombie"
    ]
}
```

**第 2 步**：将它保存在与纹理相同的目录中：

![保存配置](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/creating_animation_config/creating_animation_config.png)

**第 3 步**：加载资源包进游戏，然后抚摸僵尸看看效果：

[![演示视频](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/video_preview_1.png)](https://youtu.be/sst0NKRAGnQ)

**第 4 步**：可以看到动画生效了，但我们没听到任何声音——因为我们忘了为动画添加自定义音效。下面我们就来做这件事：

---

## 4. 添加动画音效

> 原文：[Adding Animation Sound(s)](https://github.com/LopyMine/PatPat/wiki/Adding-Animation-Sound\(s\))

最后，让我们为自定义动画添加音效。其实，如果你曾经通过资源包给 Minecraft 添加过自定义音效，这里并没有什么新东西。

---

### 4.1 从 MP3 转换为 OGG

**第 1 步**：先获取所需的声音文件。例如，我从互联网下载了一个活塞激活音效，但它是 `.mp3` 格式——这个格式行不通。

![MP3 文件](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/adding_animation_sound/adding_sound_2.png)

**第 2 步**：我们需要把声音从 `.mp3` 转换为 **`.ogg`**。可以使用任意在线转换工具来完成。

> ⚠️ **不能直接重命名文件！** 仅改变扩展名不会改变音频格式。

![转换格式](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/adding_animation_sound/adding_sound_1.png)

**第 3 步**：好的，现在有了正确的音频格式。剩下的就是注册这个音效了。

---

### 4.2 注册音效

**第 1 步**：首先，将音效文件放入 `assets/patpat/sounds/` 文件夹（对我们来说 `namespace` 就是 `patpat`）。然后，在 `assets/patpat/sounds.json` 中注册该音效。

![目录结构](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/adding_animation_sound/adding_sound_0.png)

这是一个简单的 `sounds.json` 内容示例：

`sounds.json`

```json
{
    "这里填写唯一的音效ID": {
        "sounds": [
            "命名空间:这里填写sounds文件夹里的音效文件名（不含.ogg）"
        ]
    }
}
```

**第 2 步**：修改成我们的内容：

`sounds.json`

```json
{
    "patpat_piston_sound_id": {
        "sounds": [
            "patpat:piston_sound"
        ]
    }
}
```

**第 3 步**：最后，告诉 PatPat 模组动画要播放哪个音效。需要编辑 `animated_piston.json5`，同时指定最小/最大音高和音量。

以下是我们要添加的内容：

`animated_piston.json5`

```json5
{
    // ...
    "animation": {
        // ...
        "sound": {
            "id": "patpat:patpat_piston_sound_id",
            "minPitch": 0.5,
            "maxPitch": 1.5,
            "volume": 0.8
        }
        // ...
    }
    // ...
}
```

<details>
<summary><b>查看完整文件</b>（点击展开）</summary>

`animated_piston.json5`

```json5
{
    "version": "1.0.0",
    "animation": {
        "texture": "patpat:textures/animated_piston.png",
        "duration": 300,

        "sound": {
            "id": "patpat:patpat_piston_sound_id",
            "minPitch": 0.5,
            "maxPitch": 1.5,
            "volume": 0.8
        },

        "frame": {
            "totalFrames": 5,

            "scaleX": 1,
            "scaleY": 1,

            "offsetX": 0,
            "offsetY": 0,
            "offsetZ": 0
        }
    },
    "entities": [
        "minecraft:zombie"
    ]
}
```

</details>

**第 4 步**：现在测试我们的成品资源包！

[![YouTube 视频](https://raw.githubusercontent.com/LopyMine/PatPat/master/img/wiki/video_preview_2.png)](https://youtu.be/rNBidvtxwKg)

---

## 5. 模板资源包

> 原文：[Template Resource Pack](https://github.com/LopyMine/PatPat/wiki/Template-Resource-Pack)

你可以从[**这里**](https://github.com/LopyMine/PatPat/blob/master/img/wiki/custom_animations/Template%20Custom%20Animation.zip)下载自定义动画的模板资源包。此资源包包含你需要编辑的文件夹和文件，您可以免费随意使用/修改。

### 资源包结构

```
.
└── Template Custom Animation/
    ├── assets/
    │   └── patpat/
    │       ├── sounds.json
    │       ├── sounds/
    │       └── texture/
    └── pack.mcmeta
```

---

## 6. 成品资源包

> 原文：[Ready‑To‑Use Resource Pack](https://github.com/LopyMine/PatPat/wiki/Ready%E2%80%90To%E2%80%90Use-Resource-Pack)

你可以从[**这里**](https://github.com/LopyMine/PatPat/blob/master/img/wiki/custom_animations/Piston%20Custom%20Animation.zip)下载本 Wiki 制作的成品资源包——即活塞自定义动画。你可以免费随意使用/修改。

### 资源包结构

```
.
└── Piston Custom Animation/
    ├── assets/
    │   └── patpat/
    │       ├── sounds.json
    │       ├── sounds/
    │       │   └── piston_sound.ogg
    │       └── texture/
    │           ├── animated_piston_config.json5
    │           ├── animated_piston_texture.png
    │           └── piston_side.png
    ├── pack.png
    └── pack.mcmeta
```

---

## 7. 附录：完整示例配置文件

> 来源：PatPat 源码中的[示例配置](https://github.com/LopyMine/PatPat/blob/master/src/main/resources/example/example_custom_animation_config.json5)

以下是从 PatPat 模组源码中提取的**官方完整示例配置文件**（使用 JSON5 格式，支持注释）：

```json5
// no j52j
// 上面这行注释对模组开发者很重要！
// 参见 https://github.com/LopyMine/Mossy?tab=readme-ov-file#about-json5-files
{
    "version": "1.0.1",
    "priority": 1,
    // 可选，默认 0

    "animation": {
        "texture": "patpat:textures/test1/custom_hand.png",
        "duration": 230,
        "frame": {
            "totalFrames": 3,
            // 纹理中的总帧数
            "scaleX": 1,
            // 帧宽缩放，支持浮点数，可选，默认 1
            "scaleY": 1,
            // 帧高缩放，支持浮点数，可选，默认 1
            "offsetX": 0,
            // 可选，默认 0，支持浮点数，如 0.543, 0.2, 0.00002
            "offsetY": 0,
            // 可选，默认 0，支持浮点数，如 0.543, 0.2, 0.00002
            "offsetZ": 0
            // 可选，默认 0，支持浮点数，如 0.543, 0.2, 0.00002
        },
        "sound": {
            "id": "patpat:bonk",
            "min_pitch": 0.9,
            // 可选，默认 1
            "max_pitch": 1.2,
            // 可选，默认 1
            "volume": 2.5
            // 可选，默认 1
        }
        // 也可以简写为： "sound": "patpat:bonk"
    },
    "blacklist": false,
    // 可选，默认为 false
    // 如果为 true，则该配置对除了 "entities" 以外的所有生物生效

    "entities": [
        "minecraft:goat",
        "minecraft:cat",
        {
            "id": "minecraft:player",
            "name": "LopyMine",
            // 可选
            "uuid": "192e3748-12d5-4573-a8a5-479cd394a1dc"
            // 可选
        },
        // 详细的实体信息
        {
            "id": "minecraft:goat",
            "name": "Funny Goat",
            // 可选
            "from": [
                // 可选
                {
                    "name": "nikita51",
                    // 可选
                    "uuid": "7b829ed59b74428f9b4dede06975fbc1"
                    // 可选
                }
                // 如果两个字段都缺失，将抛出错误
            ]
        }
    ]
    // 或者可以用 "entities": "minecraft:goat" 来指定单一实体
}
```

---

> **本文档功能等同 [PatPat 官方 Wiki](https://github.com/LopyMine/PatPat/wiki) 全部页面内容的中文翻译整合**，包括：
> 
> - [Getting Started • About Custom Animations](https://github.com/LopyMine/PatPat/wiki/Getting-Started-%E2%80%A2-About-Custom-Animations)
> - [Creating Animation Texture](https://github.com/LopyMine/PatPat/wiki/Creating-Animation-Texture)
> - [Creating Animation Config](https://github.com/LopyMine/PatPat/wiki/Creating-Animation-Config)
> - [Adding Animation Sound(s)](https://github.com/LopyMine/PatPat/wiki/Adding-Animation-Sound\(s\))
> - [Template Resource Pack](https://github.com/LopyMine/PatPat/wiki/Template-Resource-Pack)
> - [Ready‑To‑Use Resource Pack](https://github.com/LopyMine/PatPat/wiki/Ready%E2%80%90To%E2%80%90Use-Resource-Pack)
> 
> 所有图片均从原 Wiki 引用（raw.githubusercontent.com CDN）。
