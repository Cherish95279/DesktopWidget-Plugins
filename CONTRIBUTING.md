# 🤝 Contributing Guidelines

Thanks for your interest in contributing a plugin to DesktopWidget! This file explains the **directory structure**, **naming conventions**, **security requirements**, and **review process** for submitting plugins to this repository.

> Before submitting, please read the [Plugin Development Guide](https://github.com/Cherish95279/DesktopWidget/blob/main/docs/PLUGIN_DEV_GUIDE_EN.md) to understand the `ContentPlugin` interface and `plugin.json` fields.

---

## Table of Contents

- [1. Prerequisites](#1-prerequisites)
- [2. Directory Structure](#2-directory-structure)
- [3. plugin.json Specification](#3-pluginjson-specification)
- [4. Naming Conventions](#4-naming-conventions)
- [5. Code Requirements](#5-code-requirements)
- [6. Security Requirements](#6-security-requirements)
- [7. Versioning](#7-versioning)
- [8. Submission Process](#8-submission-process)
- [9. Review Process](#9-review-process)
- [10. Updating the Plugin Index](#10-updating-the-plugin-index)
- [11. Testing Checklist](#11-testing-checklist)

---

## 1. Prerequisites

- DesktopWidget v1.5.5 or later (for local import testing)
- Python 3.12 + PyQt6 environment
- Read the [Plugin Development Guide](https://github.com/Cherish95279/DesktopWidget/blob/main/docs/PLUGIN_DEV_GUIDE_EN.md)
- Understand the four `ContentPlugin` methods: `collect` / `render_short` / `render_detail` / `render_taskbar`

---

## 2. Directory Structure

Each plugin is a standalone subdirectory under `plugins/`, containing a `plugin.json` and a main `.py` module:

```
plugins/
└── your_plugin_key/
    ├── plugin.json              ← metadata (required)
    ├── your_plugin_key.py       ← main module (required, filename = dir name = key)
    └── translations/            ← translation files (optional)
        ├── translations_en.ts
        └── translations_ja.ts
```

### Rules

- The **directory name** must exactly match the `key` field in `plugin.json`
- The **main module filename** must be `<key>.py` (same as the directory name)
- One directory holds **exactly one plugin**
- Do not commit `__pycache__`, `.pyc`, or temp files (already covered by `.gitignore`)

---

## 3. plugin.json Specification

```json
{
    "key": "your_plugin_key",
    "name": "Plugin Display Name",
    "description": "A one-line description of what the plugin does",
    "version": "1.0.0",
    "author": "Your name or GitHub username",
    "min_app_version": "1.5.5",
    "collect_interval": 300,
    "supports_taskbar": true
}
```

| Field | Type | Required | Description |
|-------|------|:--------:|-------------|
| `key` | str | ✅ | Unique identifier; letters, digits, underscores only. **Immutable after release** |
| `name` | str | ✅ | Display name shown in dropdowns and the plugin manager |
| `description` | str | ✅ | Short description (≤ 30 words recommended) |
| `version` | str | ✅ | Semantic version, e.g. `1.0.0` |
| `author` | str | ✅ | Author name |
| `min_app_version` | str | ❌ | Minimum app version; recommended `1.5.5` |
| `collect_interval` | int | ❌ | Collection interval in seconds (min 5, default 300) |
| `supports_taskbar` | bool | ❌ | Whether taskbar display is supported (default `false`) |

> ⚠️ Once published, `key` is **immutable** — it is how users' slot configs are saved. Changing it breaks saved configurations.

---

## 4. Naming Conventions

| Item | Rule | Example |
|------|------|---------|
| `key` / dir name | lowercase + underscores; alphanumeric only | `sunrise_sunset`, `battery_plus` |
| Main class name | UpperCamelCase | `SunriseSunsetPlugin`, `BatteryPlusPlugin` |
| File encoding | UTF-8 (no BOM) | Header `# -*- coding: utf-8 -*-` |

---

## 5. Code Requirements

### 5.1 Must Subclass ContentPlugin

The main module must define **one** class that subclasses `ContentPlugin`:

```python
from plugin_manager import ContentPlugin

class MyPlugin(ContentPlugin):
    def collect(self, context):
        ...
    def render_short(self, data, i18n):
        ...
    def render_detail(self, data, is_pro, i18n):
        ...
    def render_taskbar(self, data, i18n):   # required when supports_taskbar=True
        ...
```

### 5.2 Method Return Types

| Method | Return Type | Notes |
|--------|-------------|-------|
| `collect` | `dict` | Collected data, passed to render methods |
| `render_short` | `str` or `list[str]` | str = single line; list = multi-line (max 2 recommended) |
| `render_detail` | `list[str]` | One string per line |
| `render_taskbar` | `str` | Single compact line |

### 5.3 Other Requirements

- **No top-level side effects**: do not perform network calls, file writes, or dialogs at module top level. Keep all logic inside `collect()` or class methods
- **Handle your own exceptions**: although PluginManager catches exceptions, please try/except inside `collect()` and return graceful fallback data
- **Network in collect only**: `render_*()` is called frequently — never do network or heavy work there
- **No internal object access**: use `PluginContext` (`context.settings`, `context.now`, `context.get_setting()`) for data. Do not import or access MainWindow

---

## 6. Security Requirements

### 6.1 Static Scan Patterns

DesktopWidget scans for the following dangerous code patterns on import. **Plugins published here should avoid these patterns**; if unavoidable, you must explain the usage in your PR description:

| Pattern | Description | Publishing rule |
|---------|-------------|-----------------|
| `os.system` / `os.popen` | Command execution | ❌ Forbidden |
| `subprocess.Popen` / `run` / `call` | Subprocess execution | ❌ Forbidden |
| `eval(` / `exec(` | Dynamic code execution | ❌ Forbidden |
| `__import__` | Dynamic import | ❌ Forbidden |
| `ctypes.CDLL` / `WinDLL` / `windll` | DLL loading | ❌ Forbidden |
| `os.remove` / `shutil.rmtree` | File/dir deletion | ❌ Forbidden |
| `open(` | File I/O | ⚠️ Must explain usage (e.g. reading local config) |
| `socket.socket` | Raw network | ⚠️ Must explain usage; prefer `requests` |

### 6.2 Network Behavior

- Using `requests` and similar libraries to fetch data from APIs (weather, exchange rates) is allowed
- **Network calls must be in `collect()`**, never in `render_*()`
- Set a reasonable timeout (≤ 10 seconds recommended) and handle exceptions
- **Forbidden** to upload user privacy data to external servers
- **Forbidden** to access local files unrelated to the plugin's function

### 6.3 Prohibited Behavior

The following will result in immediate rejection:

- ❌ Executing arbitrary system commands or launching external processes
- ❌ Dynamic loading/execution of code (eval, exec, __import__, ctypes)
- ❌ Deleting or modifying user/system files
- ❌ Collecting and exfiltrating user privacy information
- ❌ Backdoors, malware, or undisclosed network communication
- ❌ Interfering with the main program or other plugins

---

## 7. Versioning

Follow [Semantic Versioning](https://semver.org/) `MAJOR.MINOR.PATCH`:

- **PATCH** (`1.0.0` → `1.0.1`): bug fixes, no behavior change
- **MINOR** (`1.0.0` → `1.1.0`): new features, backward compatible
- **MAJOR** (`1.0.0` → `2.0.0`): incompatible changes (e.g. `collect()` return structure change)

> `key` never changes; only `version` increments on updates.

---

## 8. Submission Process

### 8.1 Fork & Clone

```bash
git clone https://github.com/<your-username>/DesktopWidget-Plugins.git
cd DesktopWidget-Plugins
```

### 8.2 Add Your Plugin

1. Create a directory under `plugins/` named after your `key`
2. Add `plugin.json` and the main `.py` module
3. Test locally by packaging: `zip -r <key>_v<version>.zip <key>/`
4. Import the ZIP into DesktopWidget and verify it works

### 8.3 Submit a PR

```bash
git checkout -b add-<your_plugin_key>
git add plugins/<your_plugin_key>/
git commit -m "Add plugin: <Plugin Name> v<version>"
git push origin add-<your_plugin_key>
```

Then open a Pull Request against this repository.

### 8.4 PR Description Template

```markdown
## Plugin Info
- **Name**: xxx
- **key**: xxx
- **Version**: 1.0.0
- **Author**: xxx

## Description
Briefly explain what information the plugin provides and its data source.

## Security
- [ ] No command execution / dynamic code execution / file deletion
- [ ] Network calls (if any) are in collect() with a timeout set
- [ ] No collection or upload of user privacy data
- [ ] No access to local files unrelated to plugin function

## Test Results
- [ ] Import tested successfully in DesktopWidget v1.5.5
- [ ] Dial slot displays correctly
- [ ] Hover detail displays correctly
- [ ] Taskbar displays correctly (if supports_taskbar=true)
```

---

## 9. Review Process

```
PR submitted
  │
  ▼
① Automated checks: directory structure / plugin.json format / key validity / syntax
  │
  ▼
② Static security scan: check for dangerous code patterns
  │
  ▼
③ Manual code review: logic / performance / security / style
  │
  ▼
④ Import test: import into DesktopWidget and verify all three display scenarios
  │
  ▼
✅ Approved → merge PR
  │
  ▼
⑤ Package ZIP and publish to GitHub Release
  │
  ▼
⑥ Update plugins/index.json and the README plugin catalog
  │
  ▼
⑦ Mark ✅ verified
```

### Review Timeline

- Initial review typically within **3 business days**
- If changes are needed, update the PR per review comments and resubmit
- After approval, the maintainer handles packaging and release

---

## 10. Updating the Plugin Index

When adding or updating a plugin, also update `plugins/index.json`:

```json
{
  "key": "your_plugin_key",
  "name": "Plugin Name",
  "description": "Description",
  "version": "1.0.0",
  "author": "Author",
  "min_app_version": "1.5.5",
  "collect_interval": 300,
  "supports_taskbar": true,
  "verified": true,
  "download_url": "https://github.com/Cherish95279/DesktopWidget-Plugins/releases/download/<key>_v<version>/<key>_v<version>.zip",
  "source_path": "plugins/your_plugin_key"
}
```

> The `download_url` points to a GitHub Release asset and is filled in by the maintainer after the Release is published.

---

## 11. Testing Checklist

Confirm each item before submitting:

- [ ] `plugin.json` `key` matches the directory name and main module filename
- [ ] `key` contains only letters, digits, and underscores
- [ ] Main module defines a class subclassing `ContentPlugin`
- [ ] `collect()` returns a `dict` and handles its own exceptions
- [ ] `render_short()` returns `str` or `list`, max 2 lines
- [ ] `render_detail()` returns `list[str]`
- [ ] When `supports_taskbar=true`, `render_taskbar()` returns `str`
- [ ] No module-level side effects
- [ ] No forbidden dangerous code (see [Section 6](#6-security-requirements))
- [ ] Network calls (if any) are in `collect()` with a timeout
- [ ] Packaged as ZIP and import-tested successfully in DesktopWidget
- [ ] `plugins/index.json` updated

---

> If you have questions, leave a comment on your PR or refer to the [Plugin Development Guide](https://github.com/Cherish95279/DesktopWidget/blob/main/docs/PLUGIN_DEV_GUIDE_EN.md).
