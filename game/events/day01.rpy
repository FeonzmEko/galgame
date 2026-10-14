# ============================================================
# day01.rpy —— 第 1 天剧情：骑士团的请愿
# ------------------------------------------------------------
# 事件 id 在 systems/event_manager.rpy 注册为 d1_knight_petition。
# 剧情只通过 state_manager 的统一入口修改数值。
# ============================================================

label event_day01:

    scene bg throne
    with dissolve

    "第 1 天 · 午后　王座厅"

    chancellor "陛下，骑士团长求见。她说，是为了军费的事。"

    menu:
        "亲自接见她":

            $ change_character_values("irene", {"affection": 5, "trust": 3})
            $ set_flag("met_irene")

            irene "陛下愿意亲自听我说完，这比金币更让我感激。"

            queen "说说你的骑士团，还缺什么。"

            irene "缺的不是剑，是能让士兵相信明天还会发饷的底气。"

        "让她在殿外等候":

            $ change_character_values("irene", {"affection": -3})
            $ change_kingdom_value("stability", 2)

            chancellor "是。朝会议程照旧，稳定度略有回升。"

            "艾琳沉默着退了出去。铠甲的声音在大厅里响了很久。"

        "召见财政顾问来商议":

            $ change_character_values("serena", {"trust": 4})

            serena "……我的意见是，先查账，再谈钱。"

            serena "账目对不上的时候，任何拨款都只是在往无底洞里倒金子。"

    return
