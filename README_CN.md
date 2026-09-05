# 🧩 DesktopWidget-Plugins

[![License](https://img.shields.io/badge/License-MIT-orange)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-blue)](https://github.com/Cherish95279/DesktopWidget)

DesktopWidget 官方**内容池插件**共享仓库。这里收录经过审核的社区插件，用户可以下载 ZIP 包导入到 [DesktopWidget](https://github.com/Cherish95279/DesktopWidget) 桌面小组件中，在表盘 8 个槽位上显示自定义信息。

> **适用版本**：DesktopWidget v1.6.0 及以上

<p align="center">
  <a href="README.md"><strong>🇺🇸 English</strong></a> |
  <a href="README_CN.md"><strong>🇨🇳 简体中文</strong></a>
</p>

---

## 📦 插件列表

| 插件 | 版本 | 作者 | 说明 | 任务栏 | 下载 |
|------|:----:|------|------|:------:|------|
| 🌅 日出日落 | 1.0.0 | DesktopWidget Test | 显示今日日出日落时间 | ✅ | [ZIP](https://github.com/Cherish95279/DesktopWidget-Plugins/releases/download/sunrise_sunset_v1.0.0/sunrise_sunset_v1.0.0.zip) |
| 🔋 电池增强 | 1.1.0 | DesktopWidget | 显示电池电量、充电状态与续航时间 | ✅ | [ZIP](https://github.com/Cherish95279/DesktopWidget-Plugins/releases/download/battery_plus_v1.1.0/battery_plus_v1.1.0.zip) |

> 标记 ✅ 的插件已通过人工审核与静态安全扫描。

---

## 📥 如何安装插件

1. 在上方表格中点击 **ZIP** 链接，下载插件压缩包
2. 启动 DesktopWidget，打开 **设置 → 显示项目**
3. 点击 **管理插件** 按钮
4. 在对话框上半部分点击 **浏览...**，选择下载的 ZIP 文件
5. 查看校验结果与安全扫描信息，确认无误后点击 **导入**
6. 导入成功后，关闭对话框，在 8 个槽位下拉框中选择该插件
7. 表盘即可显示插件内容 ✅

> 也可以从 [Releases 页面](https://github.com/Cherish95279/DesktopWidget-Plugins/releases) 下载所有历史版本的插件包。

---

## 🛠️ 开发自己的插件

想为 DesktopWidget 开发插件？请先阅读插件开发指南：

- **中文指南**：[PLUGIN_DEV_GUIDE_CN.md](https://github.com/Cherish95279/DesktopWidget/blob/main/docs/PLUGIN_DEV_GUIDE_CN.md)
- **English Guide**：[PLUGIN_DEV_GUIDE_EN.md](https://github.com/Cherish95279/DesktopWidget/blob/main/docs/PLUGIN_DEV_GUIDE_EN.md)

开发完成后，按照 [CONTRIBUTING.md](CONTRIBUTING_CN.md) 的规范提交 Pull Request，通过审核后即可发布到本仓库。

### 快速开始

每个插件是一个包含 `plugin.json` 和主模块 `.py` 的目录：

```
my_plugin/
├── plugin.json          # 元数据
└── my_plugin.py         # 插件主模块（继承 ContentPlugin）
```

```python
from plugin_manager import ContentPlugin

class MyPlugin(ContentPlugin):
    def collect(self, context):
        return {"value": 42}

    def render_short(self, data, i18n):
        return "答案：" + str(data["value"])

    def render_detail(self, data, is_pro, i18n):
        return ["答案：" + str(data["value"])]

    def render_taskbar(self, data, i18n):
        return "42"
```

---

## 🔒 安全说明

- 本仓库所有插件均经过**人工审核**与**静态安全扫描**
- 导入时 DesktopWidget 会扫描危险代码模式（命令执行、动态导入、文件删除等）并显示警告
- 插件运行在错误隔离环境中，崩溃不会影响主程序
- 连续采集失败 5 次的插件会被自动禁用
- 详细的提交安全要求见 [CONTRIBUTING.md](CONTRIBUTING_CN.md#6-安全要求)

> ⚠️ 请勿从非官方渠道下载插件。仅从本仓库或 DesktopWidget 官方渠道获取插件包。

---

## 📁 仓库结构

```
DesktopWidget-Plugins/
├── README.md                       # 仓库说明
├── CONTRIBUTING.md                 # 提交规范（开发者必读）
├── LICENSE
├── plugins/                        # 插件源码
│   ├── index.json                  # 插件索引（供 App 端浏览）
│   ├── sunrise_sunset/
│   │   ├── plugin.json
│   │   └── sunrise_sunset.py
│   └── battery_plus/
│       ├── plugin.json
│       └── battery_plus.py
└── releases/                       # 预打包 ZIP
    ├── sunrise_sunset_v1.0.0.zip
    └── battery_plus_v1.1.0.zip
```

---

## 🌐 相关链接

- **主项目**：[DesktopWidget](https://github.com/Cherish95279/DesktopWidget)
- **Microsoft Store**：[下载 DesktopWidget](https://apps.microsoft.com/detail/9P6GSZ8NNW52)
- **插件开发指南**：[中文](https://github.com/Cherish95279/DesktopWidget/blob/main/docs/PLUGIN_DEV_GUIDE_CN.md) / [English](https://github.com/Cherish95279/DesktopWidget/blob/main/docs/PLUGIN_DEV_GUIDE_EN.md)
- **提交规范**：[CONTRIBUTING.md](CONTRIBUTING_CN.md)
