# AstrBot Minecraft Server Query Plugin

一个为 [AstrBot](https://github.com/AstrBotDevs/AstrBot) 设计的轻量级 Minecraft 服务器查询插件。支持通过自然语言对话查询服务器状态，并由大模型组织语言回复。

## 功能特性 / Features
- 支持通过自然语言对话直接查询 Java 版 Minecraft 服务器的状态。
- 可查询信息包括：在线人数、最大人数、服务器版本、延迟 (Ping) 以及 MOTD 描述。
- 纯文本输出：将数据交给大模型，由大模型根据语境自动组织语言回复，不固定输出格式。
- 支持在 WebUI 插件设置中配置默认绑定的服务器 IP。

## 依赖安装 / Dependency installation
本插件依赖 `mcstatus` 库，请在你的 AstrBot 环境中安装：
```bash
pip install mcstatus
```
