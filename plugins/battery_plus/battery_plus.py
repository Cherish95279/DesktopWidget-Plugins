# -*- coding: utf-8 -*-
"""电池增强插件 - 显示电池电量、充电状态与续航时间"""

import psutil
from plugin_manager import ContentPlugin


class BatteryPlusPlugin(ContentPlugin):
    """电池增强插件

    基于 psutil 读取电池信息，在表盘、详情面板和任务栏三个场景展示。
    桌式机无电池时显示「无电池」提示。
    """

    def collect(self, context):
        """采集电池数据"""
        battery = psutil.sensors_battery()

        if battery is None:
            return {
                "has_battery": False,
                "percent": 0,
                "plugged": False,
                "secs_left": None,
            }

        return {
            "has_battery": True,
            "percent": int(battery.percent),
            "plugged": bool(battery.power_plugged),
            "secs_left": battery.secs_left,
        }

    def render_short(self, data, i18n):
        """表盘显示：两行"""
        if not data.get("has_battery"):
            return ["🔋 无电池"]

        icon = "🔌" if data["plugged"] else self._level_icon(data["percent"])
        line1 = icon + " " + str(data["percent"]) + "%"
        line2 = "充电中" if data["plugged"] else "使用中"
        return [line1, line2]

    def render_detail(self, data, is_pro, i18n):
        """悬停详情"""
        if not data.get("has_battery"):
            return ["🔋 当前设备未检测到电池"]

        lines = [
            "电量：" + str(data["percent"]) + "%",
            "状态：" + ("充电中 ⚡" if data["plugged"] else "使用中"),
        ]

        secs = data.get("secs_left")
        if secs is not None and secs != psutil.POWER_TIME_UNLIMITED and secs > 0:
            hours = int(secs // 3600)
            minutes = int((secs % 3600) // 60)
            lines.append("剩余：" + str(hours) + "小时" + str(minutes) + "分")
        elif data["plugged"]:
            lines.append("剩余：已接通电源")
        else:
            lines.append("剩余：计算中…")

        if is_pro:
            bar = self._battery_bar(data["percent"], data["plugged"])
            lines.append("")
            lines.append(bar)

        return lines

    def render_taskbar(self, data, i18n):
        """任务栏：单行"""
        if not data.get("has_battery"):
            return "🔋-"
        icon = "🔌" if data["plugged"] else self._level_icon(data["percent"])
        return icon + str(data["percent"]) + "%"

    # ---------- 内部方法 ----------

    def _level_icon(self, percent):
        """根据电量返回对应图标"""
        if percent >= 80:
            return "🔋"
        if percent >= 50:
            return "🔋"
        if percent >= 20:
            return "🪫"
        return "🪫"

    def _battery_bar(self, percent, plugged):
        """生成纯文本电量条（Pro 专属）"""
        total = 10
        filled = max(0, min(total, round(percent / 100 * total)))
        empty = total - filled
        bar = "█" * filled + "░" * empty
        color = "⚡" if plugged else ("🟢" if percent >= 50 else "🟡" if percent >= 20 else "🔴")
        return color + " [" + bar + "] " + str(percent) + "%"
