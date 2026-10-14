# ============================================================
# kingdom_panel.rpy —— 王国议事厅（政务面板）
# ------------------------------------------------------------
# 交互约定：面板只负责"展示 + 提交选择"。
# 点击政务按钮返回策略 id，由 script.rpy 交给 daily_manager 处理，
# 面板本身不修改任何游戏状态、也不推进日期。
# ============================================================

screen kingdom_panel():
    tag kingdom_panel
    modal True
    zorder 60

    $ subtitle = "第 {} 天 · {}".format(current_day, kui_phase_label())

    add Solid(KUI_BG)

    vbox:
        xalign 0.5
        yalign 0.5
        xsize 1600
        spacing 26

        use kui_title_bar("王国议事厅", subtitle)

        hbox:
            spacing 30

            # ---------- 左：王国概况 ----------
            frame:
                background Solid(KUI_PANEL)
                padding (36, 32)
                xsize 660
                vbox:
                    spacing 22
                    text "王国概况" size 34 color KUI_ACCENT
                    use kui_kingdom_summary()
                    null height 8
                    text kui_selected_policy_text() size 26 color KUI_MUTED

            # ---------- 右：政务选项 ----------
            frame:
                background Solid(KUI_PANEL)
                padding (36, 32)
                xsize 880
                vbox:
                    spacing 16
                    text "今日政务（选择一项）" size 34 color KUI_ACCENT

                    for choice in get_policy_choices():
                        button:
                            xfill True
                            sensitive choice["available"]
                            action Return(choice["id"])
                            background Solid(KUI_PANEL_LIGHT)
                            hover_background Solid("#313d4d")
                            insensitive_background Solid("#141920")
                            padding (26, 18)
                            vbox:
                                spacing 6
                                text choice["title"] size 30 color KUI_TEXT
                                text choice["desc"] size 23 color KUI_MUTED
                                text choice["effect"] size 23 color KUI_ACCENT
                                if not choice["available"]:
                                    text choice["reason"] size 22 color KUI_BAD

        # ---------- 底部：附加入口 ----------
        hbox:
            spacing 20
            xalign 1.0
            textbutton "查看女主档案" action Show("character_panel")
            textbutton "查看过往决策" action Show("policy_history_panel")


# 历史政务记录
screen policy_history_panel():
    tag policy_history_panel
    modal True
    zorder 75

    add Solid("#0e1116ee")

    frame:
        background Solid(KUI_PANEL)
        padding (40, 32)
        xalign 0.5
        yalign 0.5
        xsize 900
        vbox:
            spacing 18
            text "过往决策" size 36 color KUI_ACCENT

            if not policy_history:
                text "尚未做出任何决策。" size 26 color KUI_MUTED
            else:
                for record in policy_history:
                    $ record_policy = get_policy(record["policy"])
                    $ record_title = record_policy["title"] if record_policy else record["policy"]
                    hbox:
                        spacing 20
                        text "第 " + str(record["day"]) + " 天" size 26 color KUI_MUTED xsize 160
                        text record_title size 26 color KUI_TEXT

            null height 10
            textbutton "关闭" action Hide("policy_history_panel") xalign 1.0
