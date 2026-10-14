# ============================================================
# day02.rpy —— 第 2 天剧情：可疑的账本
# 事件 id: d2_suspect_ledger
# ============================================================

label event_day02:

    scene bg study
    with dissolve

    "第 2 天 · 午后　书库"

    chancellor "陛下，瑟琳娜在决算里发现了一笔对不上的支出。"

    if selected_policy == "audit_finance":

        serena "既然陛下已经下令查账，我就能名正言顺地翻开那本旧簿子。"

        $ set_flag("secret_serena")
        $ change_character_values("serena", {"trust": 6, "affection": 4})

        "她从账簿的夹层里，抽出一张没有署名的收据。"

    else:

        serena "……现在动它，会惊动不该惊动的人。"

        $ change_character_values("serena", {"trust": 2})

        "她把账簿合上，没有再多说一个字。"

    menu:
        "追问下去":

            $ change_character_values("serena", {"trust": 3})
            $ change_kingdom_value("intel", 3)

            queen "我不怕惊动人。我只怕有人替我做决定。"

            serena "……陛下想知道真相的话，请给我一点时间。"

        "暂且作罢":

            $ change_character_values("serena", {"affection": 3})
            $ change_kingdom_value("stability", 2)

            "你选择相信她会在合适的时候开口。"

            serena "谢谢。……我会记住的。"

    return
