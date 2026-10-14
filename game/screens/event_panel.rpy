# ============================================================
# event_panel.rpy —— 每日报告 / 当日结算 / 结局展示
# ------------------------------------------------------------
# 这三个界面都是"只读展示 + 一个确认按钮"，
# 真正的状态变化由 systems/ 层的函数完成。
# ============================================================

# ---------------- 晨间报告 ----------------
screen daily_report_panel():
    tag daily_report
    modal True
    zorder 55

    $ subtitle = "第 {} 天".format(current_day)

    add Solid(KUI_BG)

    vbox:
        xalign 0.5
        yalign 0.5
        xsize 1400
        spacing 26

        use kui_title_bar("晨间报告", subtitle)

        hbox:
            spacing 30

            frame:
                background Solid(KUI_PANEL)
                padding (36, 32)
                xsize 660
                vbox:
                    spacing 22
                    text "王国概况" size 34 color KUI_ACCENT
                    use kui_kingdom_summary()

            frame:
                background Solid(KUI_PANEL)
                padding (36, 32)
                xsize 700
                vbox:
                    spacing 16
                    text "今日日程" size 34 color KUI_ACCENT
                    text "早朝议事 → 剧情事件 → 当日结算" size 24 color KUI_MUTED

                    $ today_events = get_events_for_day(current_day)
                    if not today_events:
                        text "今日没有特殊事件。" size 26 color KUI_MUTED
                    else:
                        for event in today_events:
                            $ done_mark = "（已发生）" if is_event_completed(event["id"]) else ""
                            $ event_line = "· " + event["title"] + done_mark
                            text event_line size 26 color KUI_TEXT

        textbutton "开始早朝" action Return(True) xalign 1.0


# ---------------- 当日结算 ----------------
screen settlement_panel(report):
    tag settlement
    modal True
    zorder 80

    $ day_no = report["day"]
    $ subtitle = "第 {} 天".format(day_no)
    # 最后一天结算后直接进入结局判定，按钮文案相应改变
    $ next_label = "查看结局" if is_final_day(day_no) else "进入第 {} 天".format(day_no + 1)

    add Solid(KUI_BG)

    vbox:
        xalign 0.5
        yalign 0.5
        xsize 1400
        spacing 24

        use kui_title_bar("当日结算", subtitle)

        frame:
            background Solid(KUI_PANEL)
            padding (36, 30)
            xsize 1400
            vbox:
                spacing 18

                if report["policy"]:
                    $ policy_line = "今日政务：" + report["policy"]
                    text policy_line size 28 color KUI_ACCENT
                else:
                    text "今日政务：无" size 28 color KUI_BAD

                text "王国数值变化" size 30 color KUI_TEXT
                if not report["kingdom_changes"]:
                    text "无变化" size 24 color KUI_MUTED
                else:
                    for change in report["kingdom_changes"]:
                        $ kingdom_line = "{}　{}　→ {}".format(change["label"], kui_delta_text(change["delta"]), change["value"])
                        text kingdom_line size 26 color kui_delta_color(change["delta"])

                text "角色关系变化" size 30 color KUI_TEXT
                if not report["character_changes"]:
                    text "无变化" size 24 color KUI_MUTED
                else:
                    for change in report["character_changes"]:
                        $ field_label = "好感度" if change["field"] == "affection" else "信任度"
                        $ char_line = "{}　{}　{}　→ {}".format(change["name"], field_label, kui_delta_text(change["delta"]), change["value"])
                        text char_line size 26 color kui_delta_color(change["delta"])

        frame:
            background Solid(KUI_PANEL_LIGHT)
            padding (36, 24)
            xsize 1400
            vbox:
                spacing 10
                text "备注" size 30 color KUI_ACCENT
                for note in report["notes"]:
                    $ note_line = "· " + note
                    text note_line size 24 color KUI_MUTED

        textbutton next_label action Return(True) xalign 1.0


# ---------------- 结局展示 ----------------
screen ending_panel(ending):
    modal True
    zorder 90

    add Solid("#0e1116")

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 28
        xsize 1200

        text ending["title"] size 64 color KUI_ACCENT xalign 0.5
        text ending["desc"] size 32 color KUI_TEXT xalign 0.5

        frame:
            background Solid(KUI_PANEL)
            padding (36, 30)
            xfill True
            vbox:
                spacing 18
                text "最终王国概况" size 30 color KUI_ACCENT
                use kui_kingdom_summary()

        textbutton "结束本局" action Return(True) xalign 0.5
