# 🧩 DesktopWidget-Plugins

[![License](https://img.shields.io/badge/License-MIT-orange)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-blue)](https://github.com/Cherish95279/DesktopWidget)

The official **content-pool plugin** repository for DesktopWidget. This repo hosts reviewed community plugins that users can download as ZIP packages and import into the [DesktopWidget](https://github.com/Cherish95279/DesktopWidget) desktop widget to display custom information on the dial's 8 slots.

> **Requires**: DesktopWidget v1.6.0 or later

<p align="center">
  <a href="README.md"><strong>🇺🇸 English</strong></a> |
  <a href="README_CN.md"><strong>🇨🇳 简体中文</strong></a>
</p>

---

## 📦 Plugin Catalog

| Plugin | Version | Author | Description | Taskbar | Download |
|--------|:-------:|--------|-------------|:-------:|----------|
| 🌅 Sunrise & Sunset | 1.0.0 | DesktopWidget Test | Shows today's sunrise and sunset times | ✅ | [ZIP](https://github.com/Cherish95279/DesktopWidget-Plugins/releases/download/sunrise_sunset_v1.0.0/sunrise_sunset_v1.0.0.zip) |
| 🔋 Battery Plus | 1.1.0 | DesktopWidget | Shows battery level, charging status and time remaining | ✅ | [ZIP](https://github.com/Cherish95279/DesktopWidget-Plugins/releases/download/battery_plus_v1.1.0/battery_plus_v1.1.0.zip) |

> Plugins marked ✅ have passed manual review and static security scanning.

---

## 📥 How to Install a Plugin

1. Click the **ZIP** link in the table above to download the plugin package
2. Launch DesktopWidget and open **Settings → Display Items**
3. Click the **Manage Plugins** button
4. In the upper half of the dialog, click **Browse...** and select the downloaded ZIP file
5. Review the validation result and security scan info, then click **Import**
6. After a successful import, close the dialog and select the plugin from any of the 8 slot dropdowns
7. The dial now displays the plugin content ✅

> You can also download all plugin versions from the [Releases page](https://github.com/Cherish95279/DesktopWidget-Plugins/releases).

---

## 🛠️ Develop Your Own Plugin

Want to build a plugin for DesktopWidget? Start with the plugin development guide:

- **English Guide**: [PLUGIN_DEV_GUIDE_EN.md](https://github.com/Cherish95279/DesktopWidget/blob/main/docs/PLUGIN_DEV_GUIDE_EN.md)
- **中文指南**: [PLUGIN_DEV_GUIDE_CN.md](https://github.com/Cherish95279/DesktopWidget/blob/main/docs/PLUGIN_DEV_GUIDE_CN.md)

Once your plugin is ready, follow [CONTRIBUTING.md](CONTRIBUTING.md) to submit a Pull Request. After review, it will be published to this repository.

### Quick Start

Each plugin is a directory containing a `plugin.json` and a main `.py` module:

```
my_plugin/
├── plugin.json          # metadata
└── my_plugin.py         # main module (subclasses ContentPlugin)
```

```python
from plugin_manager import ContentPlugin

class MyPlugin(ContentPlugin):
    def collect(self, context):
        return {"value": 42}

    def render_short(self, data, i18n):
        return "Answer: " + str(data["value"])

    def render_detail(self, data, is_pro, i18n):
        return ["Answer: " + str(data["value"])]

    def render_taskbar(self, data, i18n):
        return "42"
```

---

## 🔒 Security

- All plugins in this repository undergo **manual review** and **static security scanning**
- On import, DesktopWidget scans for dangerous code patterns (command execution, dynamic imports, file deletion, etc.) and shows warnings
- Plugins run in an error-isolated environment; a crash does not affect the main program
- A plugin that fails to collect data 5 times in a row is automatically disabled
- See [CONTRIBUTING.md](CONTRIBUTING.md) for full submission security requirements

> ⚠️ Do not download plugins from unofficial sources. Only use this repository or official DesktopWidget channels.

---

## 📁 Repository Structure

```
DesktopWidget-Plugins/
├── README.md                       # this file
├── CONTRIBUTING.md                 # submission guidelines (devs must read)
├── LICENSE
├── plugins/                        # plugin source code
│   ├── index.json                  # plugin index (for in-app browsing)
│   ├── sunrise_sunset/
│   │   ├── plugin.json
│   │   └── sunrise_sunset.py
│   └── battery_plus/
│       ├── plugin.json
│       └── battery_plus.py
└── releases/                       # pre-packaged ZIPs
    ├── sunrise_sunset_v1.0.0.zip
    └── battery_plus_v1.1.0.zip
```

---

## 🌐 Related Links

- **Main project**: [DesktopWidget](https://github.com/Cherish95279/DesktopWidget)
- **Microsoft Store**: [Get DesktopWidget](https://apps.microsoft.com/detail/9P6GSZ8NNW52)
- **Plugin dev guide**: [English](https://github.com/Cherish95279/DesktopWidget/blob/main/docs/PLUGIN_DEV_GUIDE_EN.md) / [中文](https://github.com/Cherish95279/DesktopWidget/blob/main/docs/PLUGIN_DEV_GUIDE_CN.md)
- **Submission guidelines**: [CONTRIBUTING.md](CONTRIBUTING.md)
