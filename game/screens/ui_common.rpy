# ============================================================
# ui_common.rpy —— 界面层公共配色与可复用组件
# ------------------------------------------------------------
# 只放"展示"相关的内容，不含任何游戏规则。
# ============================================================

# 配色（与 gui.accent_color 保持一致的金色主题）
define KUI_BG = "#0e1116"
define KUI_PANEL = "#1a2029"
define KUI_PANEL_LIGHT = "#242c38"
define KUI_ACCENT = "#c9a227"
define KUI_TEXT = "#e8e4d8"
define KUI_MUTED = "#8b93a1"
define KUI_GOOD = "#6fbf73"
define KUI_BAD = "#d9534f"

init python:

    def kui_delta_color(delta):
        """正数绿色、负数红色、零灰色。"""
        if delta > 0:
            return KUI_GOOD
        if delta < 0:
            return KUI_BAD
        return KUI_MUTED

    def kui_delta_text(delta):
        """把数值变化格式化为 +8 / -200 形式。"""
        return "{:+d}".format(delta)

    def kui_phase_label():
        """当前阶段的友好名称。"""
        labels = {
            "morning": "上午 · 早朝",
            "event": "午后 · 事件",
            "settle": "夜晚 · 结算",
        }
        return labels.get(current_phase, current_phase)

    def kui_selected_policy_text():
        """当天已选政务的展示文本。"""
        policy = get_policy(selected_policy)
        if policy is None:
            return "尚未决定"
        return policy["title"]


# 角色隐藏秘密：只有对应剧情标记为真时才在档案中显示
define KUI_CHARACTER_SECRETS = {
    "irene": "她右手上的旧伤，来自三年前那场没有写进战报的败仗。",
    "serena": "账簿夹层里，藏着一笔来路不明的进项。",
    "lilith": "她与邻国密使，曾有过一次深夜会面。",
}


# 数值条：标签 + 进度条 + 数值
screen kui_stat_bar(label, value, max_value=100, color=KUI_ACCENT, width=360):
    hbox:
        spacing 14
        yalign 0.5
        text label xsize 110 color KUI_TEXT size 28 yalign 0.5
        bar:
            value StaticValue(value, max_value)
            xsize width
            ysize 22
            yalign 0.5
            left_bar Solid(color)
            right_bar Solid("#333a44")
        text str(value) xsize 70 color KUI_ACCENT size 28 xalign 1.0 yalign 0.5


# 王国数值总览（供多个界面复用）
screen kui_kingdom_summary():
    vbox:
        spacing 18
        use kui_stat_bar("国库", kingdom["gold"], 10000)
        use kui_stat_bar("稳定度", kingdom["stability"], 100)
        use kui_stat_bar("外交", kingdom["diplomacy"], 100)
        use kui_stat_bar("情报", kingdom["intel"], 100)


# 顶部标题栏
screen kui_title_bar(title, subtitle=""):
    frame:
        background Solid(KUI_PANEL)
        padding (36, 22)
        xfill True
        hbox:
            spacing 24
            text title size 44 color KUI_ACCENT
            if subtitle:
                text subtitle size 28 color KUI_MUTED yalign 0.5


# 剧情进行中常驻右上角的经营数据 HUD
screen kingdom_hud():
    zorder 10

    $ day_text = "第 {} 天".format(current_day)
    $ phase_text = kui_phase_label()
    $ gold_text = "国库 " + str(kingdom["gold"])
    $ stability_text = "稳定 " + str(kingdom["stability"])
    $ diplomacy_text = "外交 " + str(kingdom["diplomacy"])
    $ intel_text = "情报 " + str(kingdom["intel"])
    $ hud_title = day_text + " · " + phase_text

    frame:
        background Solid("#0e1116cc")
        padding (26, 16)
        xalign 0.98
        yalign 0.02
        vbox:
            spacing 8
            xalign 1.0
            text hud_title size 24 color KUI_ACCENT xalign 1.0
            hbox:
                spacing 22
                text gold_text size 22 color KUI_TEXT
                text stability_text size 22 color KUI_TEXT
                text diplomacy_text size 22 color KUI_TEXT
                text intel_text size 22 color KUI_TEXT

