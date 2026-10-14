# ============================================================
# character_panel.rpy —— 女主档案
# ------------------------------------------------------------
# 只读界面：展示好感、信任、剧情进度与已解锁路线。
# 未发现（剧情标记为假）的秘密不显示。
# ============================================================

screen character_panel():
    tag character_panel
    modal True
    zorder 70

    $ subtitle = "第 {} 天".format(current_day)

    add Solid("#0e1116f2")

    vbox:
        xalign 0.5
        yalign 0.5
        xsize 1360
        spacing 24

        use kui_title_bar("女主档案", subtitle)

        for char_id in ("irene", "serena", "lilith"):
            $ char = characters[char_id]
            $ route_text = "已解锁" if char["route_unlocked"] else "未解锁"
            $ secret_known = has_flag("secret_" + char_id)
            $ progress_text = "个人剧情进度：{} · 个人路线：{}".format(char["story_stage"], route_text)

            frame:
                background Solid(KUI_PANEL)
                padding (30, 24)
                xfill True
                vbox:
                    spacing 12

                    hbox:
                        spacing 16
                        text char["name"] size 34 color KUI_ACCENT
                        text char["title"] size 24 color KUI_MUTED yalign 0.5

                    use kui_stat_bar("好感度", char["affection"], 100, KUI_GOOD, 420)
                    use kui_stat_bar("信任度", char["trust"], 100, KUI_ACCENT, 420)

                    text progress_text size 24 color KUI_MUTED

                    if secret_known:
                        $ secret_text = "已知秘密：" + KUI_CHARACTER_SECRETS[char_id]
                        text secret_text size 24 color KUI_BAD
                    else:
                        text "已知秘密：尚未发现" size 24 color KUI_MUTED

        textbutton "关闭" action Hide("character_panel") xalign 1.0
