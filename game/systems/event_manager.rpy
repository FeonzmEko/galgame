# ============================================================
# event_manager.rpy —— 事件注册与调度（游戏逻辑层）
# ------------------------------------------------------------
# 所有剧情事件在此登记：唯一 id、触发天数、条件、对应 label。
# 事件是否已执行由 completed_events 记录，防止重复触发。
# 剧情内容本身写在 events/*.rpy 的 label 中，不写在这里。
# ============================================================

init -1 python:

    # ---------- 事件触发条件 ----------
    # 条件是无参函数，返回 True 表示允许触发。
    def _cond_lilith_trust():
        return characters["lilith"]["trust"] >= 15

    def _cond_serena_trust():
        return characters["serena"]["trust"] >= 20

    EVENT_CONDITIONS = {
        "lilith_trust": _cond_lilith_trust,
        "serena_trust": _cond_serena_trust,
    }

    # ---------- 事件注册表（常量，不随存档变化） ----------
    # id      唯一标识，用于 completed_events 去重
    # day     触发天数
    # title   事件标题（界面展示）
    # label   剧情 label 名
    # require 触发条件名（EVENT_CONDITIONS 的键），None 表示无条件
    EVENT_REGISTRY = [
        {
            "id": "d1_knight_petition",
            "day": 1,
            "title": "骑士团的请愿",
            "label": "event_day01",
            "require": None,
        },
        {
            "id": "d2_suspect_ledger",
            "day": 2,
            "title": "可疑的账本",
            "label": "event_day02",
            "require": None,
        },
        {
            "id": "d3_border_fire",
            "day": 3,
            "title": "边境的烽火",
            "label": "event_day03",
            "require": None,
        },
        {
            "id": "d3_night_report",
            "day": 3,
            "title": "深夜的密报",
            "label": "event_day03_secret",
            "require": "lilith_trust",
        },
    ]

    def get_event(event_id):
        """按 id 取事件定义，不存在返回 None。"""
        for event in EVENT_REGISTRY:
            if event["id"] == event_id:
                return event
        return None

    def is_event_completed(event_id):
        """事件是否已执行过。"""
        return event_id in completed_events

    def _event_condition_ok(event):
        """判断事件的触发条件是否满足。"""
        require = event.get("require")
        if require is None:
            return True

        condition = EVENT_CONDITIONS.get(require)
        if condition is None:
            raise Exception("Unknown event condition: " + str(require))

        return bool(condition())

    def get_events_for_day(day):
        """返回某天注册的全部事件定义。"""
        return [e for e in EVENT_REGISTRY if e["day"] == day]

    def get_available_events(day):
        """返回某天尚未执行且条件满足的事件列表。"""
        result = []
        for event in EVENT_REGISTRY:
            if event["day"] != day:
                continue
            if is_event_completed(event["id"]):
                continue
            if not _event_condition_ok(event):
                continue
            result.append(event)
        return result

    def mark_event_completed(event_id):
        """标记事件已执行，重复标记会抛异常，便于尽早发现重复触发 bug。"""
        if get_event(event_id) is None:
            raise Exception("Unknown event: " + str(event_id))

        if is_event_completed(event_id):
            raise Exception("Event already completed: " + str(event_id))

        completed_events.append(event_id)

    def pick_daily_event(day):
        """挑选当天要播放的事件（取第一个可用的），没有则返回 None。"""
        available = get_available_events(day)
        if not available:
            return None
        return available[0]
