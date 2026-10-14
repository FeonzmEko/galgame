# ============================================================
# script.rpy —— 主流程编排
# ------------------------------------------------------------
# 本文件只负责"什么时候做什么"：
#   · 规则实现放在 systems/
#   · 剧情内容放在 events/
#   · 界面展示放在 screens/
#
# 每日循环：
#   晨间报告 → 早朝议事（选政务）→ 剧情事件 → 当日结算 → 结局判定 → 下一天
#
# 重要约定：经营面板里的按钮只提交选择，日期推进与结算全部由这里调用
# systems/ 层完成，避免重复结算或跳过剧情。
# ============================================================

label start:

    call prologue

    jump main_loop


label prologue:

    scene bg throne
    with fade

    "你在一片低声的议论中睁开眼睛。"

    queen "从今天起，这个国家的每一笔账、每一场战事、每一次结盟，都要由我来决定。"

    chancellor "陛下，朝会已经开始了。"

    return


label main_loop:

    $ set_phase("morning")

    # 1. 晨间报告：展示当前状态与今日日程
    scene bg hall
    with dissolve
    call screen daily_report_panel

    # 2. 早朝议事：界面只提交选择，由 daily_manager 记录
    call screen kingdom_panel
    $ select_policy(_return)

    # 3. 剧情事件：事件注册在 event_manager，内容在 events/
    $ set_phase("event")
    show screen kingdom_hud
    call play_daily_event
    hide screen kingdom_hud

    # 4. 当日结算：所有数值变化统一在这里发生
    $ set_phase("settle")
    $ day_report = settle_day()
    call screen settlement_panel(day_report)

    # 5. 结局判定
    $ next_ending = check_ending()
    if next_ending is not None:
        $ set_ending(next_ending)
        jump ending_flow

    # 6. 进入下一天
    $ advance_day()
    jump main_loop


# 播放当天所有未执行且条件满足的事件（每个事件有唯一 id，只执行一次）
label play_daily_event:

    $ daily_events = get_available_events(current_day)

    if not daily_events:
        call event_quiet_day
        return

    while daily_events:
        $ daily_event = daily_events.pop(0)
        $ mark_event_completed(daily_event["id"])
        call expression daily_event["label"]

    return


label ending_flow:

    $ ending_data = get_ending(ending_id)
    call screen ending_panel(ending_data)

    return
