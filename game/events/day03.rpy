# ============================================================
# day03.rpy —— 第 3 天剧情：边境的烽火 / 深夜的密报
# 事件 id: d3_border_fire、d3_night_report（后者需莉莉丝信任 ≥ 20）
# ============================================================

label event_day03:

    scene bg border
    with dissolve

    "第 3 天 · 午后　边境"

    chancellor "边境传来烽火。邻国的巡逻队越过了界碑。"

    $ change_kingdom_value("stability", -5)

    if kingdom["stability"] < 40:

        "防线本就空虚，士兵们在寒风里缩着肩膀。"

        $ change_kingdom_value("stability", -5)
        $ change_character_values("irene", {"trust": -3})

        irene "……如果军费再不到位，我无法保证下一次还能守住这里。"

    else:

        irene "交给我。只要士气还在，界碑就还在我们这边。"

        $ change_character_values("irene", {"affection": 4, "trust": 4})

    menu:
        "增派兵力":

            $ change_kingdom_value("gold", -150)
            $ change_kingdom_value("stability", 6)

            irene "陛下信任我，我不会让您失望。"

        "派密使外交交涉":

            $ change_kingdom_value("diplomacy", 8)
            $ change_character_values("lilith", {"trust": 4})

            lilith "密使今晚就会出发。……不过，回来的未必只有和平。"

    return


label event_day03_secret:

    scene bg night
    with dissolve

    "第 3 天 · 深夜　书房"

    shadow "陛下，还没有休息？"

    lilith "关于邻国的调动，我有一条不能写进公文的消息。"

    if has_flag("secret_serena"):

        lilith "……和您那本旧账簿，其实是同一笔钱。"

        $ set_flag("secret_lilith")
        $ change_character_values("lilith", {"affection": 5, "trust": 5})

    else:

        lilith "邻国的密使，三天前见过我们宫里的人。"

        $ change_character_values("lilith", {"trust": 4})

    "你看着她递来的纸条，纸角还带着夜里的湿气。"

    return
