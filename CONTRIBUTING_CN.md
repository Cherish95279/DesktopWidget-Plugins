# 🤝 贡献指南

感谢你有兴趣为 DesktopWidget 贡献插件！本文件说明了提交插件到本仓库的**目录结构**、**命名规范**、**安全要求**和**审核流程**。

> 提交前请务必先阅读[插件开发指南](https://github.com/Cherish95279/DesktopWidget/blob/main/docs/PLUGIN_DEV_GUIDE_CN.md)，了解 `ContentPlugin` 接口和 `plugin.json` 字段定义。

---

## 目录

- [1. 前置要求](#1-前置要求)
- [2. 目录结构](#2-目录结构)
- [3. plugin.json 规范](#3-pluginjson-规范)
- [4. 命名规范](#4-命名规范)
- [5. 代码要求](#5-代码要求)
- [6. 安全要求](#6-安全要求)
- [7. 版本号规范](#7-版本号规范)
- [8. 提交流程](#8-提交流程)
- [9. 审核流程](#9-审核流程)
- [10. 更新插件索引](#10-更新插件索引)
- [11. 测试清单](#11-测试清单)

---

## 1. 前置要求

- DesktopWidget v1.5.5 或更高版本（用于本地测试导入）
- Python 3.12 + PyQt6 环境
- 已阅读[插件开发指南](https://github.com/Cherish95279/DesktopWidget/blob/main/docs/PLUGIN_DEV_GUIDE_CN.md)
- 了解 `ContentPlugin` 接口的四个方法：`collect` / `render_short` / `render_detail` / `render_taskbar`

---

## 2. 目录结构

每个插件是 `plugins/` 下的一个独立子目录，包含 `plugin.json` 和主模块 `.py`：

```
plugins/
└── your_plugin_key/
    ├── plugin.json              ← 元数据（必须）
    ├── your_plugin_key.py       ← 主模块（必须，文件名 = 目录名 = key）
    └── translations/            ← 翻译文件（可选）
        ├── translations_en.ts
        └── translations_ja.ts
```

### 规则

- **目录名**必须与 `plugin.json` 中的 `key` 字段**完全一致**
- **主模块文件名**必须为 `<key>.py`（即与目录名一致）
- 一个目录**只能包含一个插件**
- 不要提交 `__pycache__`、`.pyc`、临时文件等（已在 `.gitignore` 中忽略）

---

## 3. plugin.json 规范

```json
{
    "key": "your_plugin_key",
    "name": "插件显示名称",
    "description": "一句话描述插件功能",
    "version": "1.0.0",
    "author": "你的名字或 GitHub 用户名",
    "min_app_version": "1.5.5",
    "collect_interval": 300,
    "supports_taskbar": true
}
```

| 字段 | 类型 | 必须 | 说明 |
|------|------|:----:|------|
| `key` | str | ✅ | 唯一标识，只允许字母、数字、下划线，**发布后不可更改** |
| `name` | str | ✅ | 显示名称，出现在下拉框和插件管理列表 |
| `description` | str | ✅ | 简短描述（建议不超过 30 字） |
| `version` | str | ✅ | 语义化版本号，如 `1.0.0` |
| `author` | str | ✅ | 作者名 |
| `min_app_version` | str | ❌ | 最低支持的 App 版本，建议填 `1.5.5` |
| `collect_interval` | int | ❌ | 采集间隔（秒），最小 5，默认 300 |
| `supports_taskbar` | bool | ❌ | 是否支持任务栏显示，默认 `false` |

> ⚠️ `key` 一旦发布就**不可更改**，它是用户保存槽位配置的依据。改 key 会导致用户已保存的配置失效。

---

## 4. 命名规范

| 项目 | 规则 | 示例 |
|------|------|------|
| `key` / 目录名 | 全小写 + 下划线，只允许字母数字下划线 | `sunrise_sunset`、`battery_plus` |
| 主类名 | 大驼峰 | `SunriseSunsetPlugin`、`BatteryPlusPlugin` |
| 文件编码 | UTF-8（无 BOM） | 文件头 `# -*- coding: utf-8 -*-` |

---

## 5. 代码要求

### 5.1 必须继承 ContentPlugin

主模块中必须定义**一个**继承 `ContentPlugin` 的类：

```python
from plugin_manager import ContentPlugin

class MyPlugin(ContentPlugin):
    def collect(self, context):
        ...
    def render_short(self, data, i18n):
        ...
    def render_detail(self, data, is_pro, i18n):
        ...
    def render_taskbar(self, data, i18n):   # supports_taskbar=True 时必须实现
        ...
```

### 5.2 方法返回值约定

| 方法 | 返回类型 | 说明 |
|------|----------|------|
| `collect` | `dict` | 采集的数据，会传给 render 方法 |
| `render_short` | `str` 或 `list[str]` | str 为单行，list 为多行（建议不超过 2 行） |
| `render_detail` | `list[str]` | 每个元素一行 |
| `render_taskbar` | `str` | 单行紧凑文本 |

### 5.3 其他要求

- **禁止模块顶层副作用**：不要在模块顶层执行网络请求、文件写入、弹窗等操作。所有逻辑放在 `collect()` 或类方法内
- **异常自处理**：方法内抛出的异常虽会被 PluginManager 捕获，但请在 `collect()` 中自行 try/except，返回合理的降级数据
- **网络请求放 collect**：`render_*` 会被频繁调用，不要在其中发起网络请求或耗时操作
- **不依赖主程序内部对象**：通过 `PluginContext`（`context.settings`、`context.now`、`context.get_setting()`）获取数据，不要 import 或访问 MainWindow

---

## 6. 安全要求

### 6.1 静态扫描检测项

导入时 DesktopWidget 会扫描以下危险代码模式。**上架本仓库的插件应尽量避免使用这些模式**；如确有必要，必须在 PR 描述中说明用途：

| 检测项 | 说明 | 上架要求 |
|--------|------|----------|
| `os.system` / `os.popen` | 系统命令执行 | ❌ 禁止 |
| `subprocess.Popen` / `run` / `call` | 子进程执行 | ❌ 禁止 |
| `eval(` / `exec(` | 动态代码执行 | ❌ 禁止 |
| `__import__` | 动态导入 | ❌ 禁止 |
| `ctypes.CDLL` / `WinDLL` / `windll` | DLL 加载 | ❌ 禁止 |
| `os.remove` / `shutil.rmtree` | 文件/目录删除 | ❌ 禁止 |
| `open(` | 文件读写 | ⚠️ 需说明用途（如读取本地配置） |
| `socket.socket` | 原始网络通信 | ⚠️ 需说明用途，建议改用 `requests` |

### 6.2 网络行为

- 允许使用 `requests` 等库访问网络 API 获取数据（如天气、汇率）
- **网络请求必须放在 `collect()` 中**，不得放在 `render_*()`
- 必须设置合理的超时（建议 ≤ 10 秒）和异常处理
- **禁止**上传用户隐私数据到外部服务器
- **禁止**访问非插件功能所需的本地文件

### 6.3 禁止行为

以下行为将直接拒绝审核：

- ❌ 执行任意系统命令或启动外部进程
- ❌ 动态加载/执行代码（eval、exec、__import__、ctypes）
- ❌ 删除、修改用户文件或系统文件
- ❌ 收集并外传用户隐私信息
- ❌ 植入后门、恶意代码或未经声明的网络通信
- ❌ 干扰主程序或其他插件的正常运行

---

## 7. 版本号规范

采用[语义化版本](https://semver.org/lang/zh-CN/) `MAJOR.MINOR.PATCH`：

- **PATCH**（`1.0.0` → `1.0.1`）：Bug 修复，行为不变
- **MINOR**（`1.0.0` → `1.1.0`）：新增功能，向后兼容
- **MAJOR**（`1.0.0` → `2.0.0`）：不兼容的改动（如 `collect()` 返回结构变化）

> `key` 永远不变，只有 `version` 随更新递增。

---

## 8. 提交流程

### 8.1 Fork & Clone

```bash
git clone https://github.com/<你的用户名>/DesktopWidget-Plugins.git
cd DesktopWidget-Plugins
```

### 8.2 添加插件

1. 在 `plugins/` 下创建以你的 `key` 命名的目录
2. 添加 `plugin.json` 和主模块 `.py`
3. 本地打包测试：`zip -r <key>_v<version>.zip <key>/`
4. 在 DesktopWidget 中导入 ZIP 测试通过

### 8.3 提交 PR

```bash
git checkout -b add-<your_plugin_key>
git add plugins/<your_plugin_key>/
git commit -m "Add plugin: <插件名称> v<version>"
git push origin add-<your_plugin_key>
```

然后在本仓库发起 Pull Request。

### 8.4 PR 描述模板

```markdown
## 插件信息
- **名称**：xxx
- **key**：xxx
- **版本**：1.0.0
- **作者**：xxx

## 功能描述
简要说明插件提供什么信息、数据来源。

## 安全说明
- [ ] 不包含命令执行 / 动态代码执行 / 文件删除
- [ ] 网络请求（如有）放在 collect() 中，已设超时
- [ ] 不收集或上传用户隐私数据
- [ ] 不访问插件功能无关的本地文件

## 测试结果
- [ ] 已在 DesktopWidget v1.5.5 中导入测试通过
- [ ] 表盘槽位显示正常
- [ ] 悬停详情显示正常
- [ ] 任务栏显示正常（如 supports_taskbar=true）
```

---

## 9. 审核流程

```
PR 提交
  │
  ▼
① 自动检查：目录结构 / plugin.json 格式 / key 合法性 / 语法检查
  │
  ▼
② 静态安全扫描：检查危险代码模式
  │
  ▼
③ 人工代码审查：逻辑 / 性能 / 安全 / 代码风格
  │
  ▼
④ 测试导入：在 DesktopWidget 中导入并验证三个场景显示
  │
  ▼
✅ 审核通过 → 合并 PR
  │
  ▼
⑤ 打包 ZIP，发布到 GitHub Release
  │
  ▼
⑥ 更新 plugins/index.json 和 README 插件列表
  │
  ▼
⑦ 标记 ✅ 已验证
```

### 审核周期

- 一般在 **3 个工作日内**完成初审
- 如需修改，请在 PR 中根据 review 意见更新后重新提交
- 审核通过后由维护者负责打包发布

---

## 10. 更新插件索引

新增或更新插件后，请同步更新 `plugins/index.json`：

```json
{
  "key": "your_plugin_key",
  "name": "插件名称",
  "description": "描述",
  "version": "1.0.0",
  "author": "作者",
  "min_app_version": "1.5.5",
  "collect_interval": 300,
  "supports_taskbar": true,
  "verified": true,
  "download_url": "https://github.com/Cherish95279/DesktopWidget-Plugins/releases/download/<key>_v<version>/<key>_v<version>.zip",
  "source_path": "plugins/your_plugin_key"
}
```

> `download_url` 指向 GitHub Release 资产地址，发布 Release 后由维护者填写。

---

## 11. 测试清单

提交前请逐项确认：

- [ ] `plugin.json` 的 `key` 与目录名、主模块文件名一致
- [ ] `key` 只包含字母、数字、下划线
- [ ] 主模块定义了继承 `ContentPlugin` 的类
- [ ] `collect()` 返回 `dict`，异常已自行处理
- [ ] `render_short()` 返回 `str` 或 `list`，不超过 2 行
- [ ] `render_detail()` 返回 `list[str]`
- [ ] `supports_taskbar=true` 时 `render_taskbar()` 返回 `str`
- [ ] 无模块顶层副作用
- [ ] 无禁止的危险代码（见[第 6 节](#6-安全要求)）
- [ ] 网络请求（如有）放在 `collect()` 中并设超时
- [ ] 已打包 ZIP 并在 DesktopWidget 中导入测试通过
- [ ] 已更新 `plugins/index.json`

---

> 如有疑问，请在 PR 中留言或参考[插件开发指南](https://github.com/Cherish95279/DesktopWidget/blob/main/docs/PLUGIN_DEV_GUIDE_CN.md)。
