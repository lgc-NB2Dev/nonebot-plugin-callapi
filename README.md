<!-- markdownlint-disable MD031 MD033 MD036 MD041 -->

<div align="center">

<a href="https://v2.nonebot.dev/store">
  <img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo">
</a>

<p>
  <img src="https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/template/plugin.svg" alt="NoneBotPluginText">
</p>

# NoneBot-Plugin-CallAPI

_✨ 使用指令来调用 Bot 的 API ✨_

<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">
<a href="https://pdm.fming.dev">
  <img src="https://img.shields.io/badge/pdm-managed-blueviolet" alt="pdm-managed">
</a>
<a href="https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/f4cf118f-464e-4dfc-bf93-dd2cb970b034">
  <img src="https://wakatime.com/badge/user/b61b0f9a-f40b-4c82-bc51-0a75c67bfccf/project/f4cf118f-464e-4dfc-bf93-dd2cb970b034.svg" alt="wakatime">
</a>

<br />

<a href="https://pydantic.dev">
  <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/template/pyd-v1-or-v2.json" alt="Pydantic Version 1 Or 2" >
</a>
<a href="./LICENSE">
  <img src="https://img.shields.io/github/license/lgc-NB2Dev/nonebot-plugin-callapi.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-callapi">
  <img src="https://img.shields.io/pypi/v/nonebot-plugin-callapi.svg" alt="pypi">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-callapi">
  <img src="https://img.shields.io/pypi/dm/nonebot-plugin-callapi" alt="pypi download">
</a>

<br />

<a href="https://registry.nonebot.dev/plugin/nonebot-plugin-callapi:nonebot_plugin_callapi">
  <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fnbbdg.lgc2333.top%2Fplugin%2Fnonebot-plugin-callapi" alt="NoneBot Registry">
</a>
<a href="https://registry.nonebot.dev/plugin/nonebot-plugin-callapi:nonebot_plugin_callapi">
  <img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fnbbdg.lgc2333.top%2Fplugin-adapters%2Fnonebot-plugin-callapi" alt="Supported Adapters">
</a>

</div>

## 📖 介绍

使用 Bot 指令来直接调用 Bot 的 API 吧！

## 💿 安装

以下提到的方法 任选**其一** 即可

<details open>
<summary>[推荐] 使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

```bash
nb plugin install nonebot-plugin-callapi
```

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

```bash
pip install nonebot-plugin-callapi
```

</details>
<details>
<summary>pdm</summary>

```bash
pdm add nonebot-plugin-callapi
```

</details>
<details>
<summary>poetry</summary>

```bash
poetry add nonebot-plugin-callapi
```

</details>
<details>
<summary>conda</summary>

```bash
conda install nonebot-plugin-callapi
```

</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分的 `plugins` 项里追加写入

```toml
[tool.nonebot]
plugins = [
    # ...
    "nonebot_plugin_callapi"
]
```

</details>

## ⚙️ 配置

在 nonebot2 项目的 `.env` 文件中添加下表中的必填配置

|    配置项     | 必填 | 默认值 | 说明                                                               |
| :-----------: | :--: | :----: | :----------------------------------------------------------------- |
| `CALLAPI_PIC` |  否  | `True` | API 调用结果是否生成为图片（如所在平台不支持图片，将会回退到文本） |

## 🎉 使用

### 指令

插件指令仅限 `SUPERUSER` 调用

![intro](https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/callapi/intro.png)

### 效果图

![preview](https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/callapi/preview.png)

## 📞 联系

QQ：3076823485  
Telegram：[@lgc2333](https://t.me/lgc2333)  
吹水群：[168603371](https://qm.qq.com/q/EikuZ5sP4G)  
邮箱：<lgc2333@126.com>

## 💡 鸣谢

### [ITCraftDevelopmentTeam/XDbot2](https://github.com/ITCraftDevelopmentTeam/XDbot2)

功能启发

### [MeetWq/pil-utils](https://github.com/MeetWq/pil-utils)

超好用的 Pillow 辅助库

### [felinae98/nonebot-plugin-send-anything-anywhere](https://github.com/felinae98/nonebot-plugin-send-anything-anywhere)

多适配器消息发送支持（本插件用来发送图片）

## 💰 赞助

**[赞助我](https://blog.lgc2333.top/donate)**

感谢大家的赞助！你们的赞助将是我继续创作的动力！

## 📝 更新日志

### 0.3.0

- 适配 pil-utils 0.2

### 0.2.0

- 适配 Pydantic V1 & V2
- 换用 alconna

### 0.1.3

- 删除插件自身对 Telegram 消息发送的兼容，现在发送 Telegram 消息使用 SAA 接管

### 0.1.2

- 🎉 NoneBot 2.0 🚀

### 0.1.1

- 修复文本类 Segment 未做转义处理的问题
