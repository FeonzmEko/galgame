# ============================================================
# daily_manager.rpy —— 政务决策与每日结算（游戏逻辑层）
# ------------------------------------------------------------
# 关键约定：
#   经营面板按钮只调用 select_policy() 提交选择，不推进日期。
#   由本文件的 settle_day() 统一执行事件效果、财政结算，
#   advance_day() 负责进入第二天，避免重复结算 / 跳过剧情。
# ============================================================

init -1 python:

    # ---------- 数值参数 ----------
    DAILY_BASE_INCOME = 60      # 每日基础收入
    DAILY_UPKEEP = 40           # 每日固定支出
    LOW_GOLD_THRESHOLD = 200    # 低于此值触发"国库空虚"
    LOW_GOLD_STABILITY_PENALTY = -3

    DEMO_MAX_DAY = 3            # 第一阶段 Demo 的天数上限

    # ---------- 政务选项注册表（常量） ----------
    # kingdom     政务执行时的王国数值变化
    # characters  政务执行时的角色数值变化
    # min_kingdom 解锁所需最低数值（用于按钮置灰）
    POLICIES = [
        {
            "id": "fund_knights",
            "title": "拨款骑士团",
            "desc": "拨出 200 金币充实军备，稳定度上升，艾琳好感提升。",
            "kingdom": {"gold": -200, "stability": 8},
            "characters": {"irene": {"affection": 5, "trust": 5}},
            "min_kingdom": {"gold": 200},
        },
        {
            "id": "audit_finance",
            "title": "调查财政",
            "desc": "暂缓军费、彻查账目。国库增收，但贵族不满。",
            "kingdom": {"gold": 150, "stability": -4},
            "characters": {"serena": {"trust": 6}},
            "min_kingdom": {},
        },
        {
            "id": "expand_intel",
            "title": "整顿密探",
            "desc": "拨款扩建情报网，情报值上升，莉莉丝好感提升。",
            "kingdom": {"gold": -100, "intel": 8},
            "characters": {"lilith": {"affection": 3, "trust": 5}},
            "min_kingdom": {"gold": 100},
        },
    ]

    def get_policy(policy_id):
        """按 id 取政务定义，不存在返回 None。"""
        if policy_id is None:
            return None
        for policy in POLICIES:
            if policy["id"] == policy_id:
                return policy
        return None

    def is_policy_available(policy):
        """判断政务是否可执行，返回 (是否可用, 原因)。"""
        for key, minimum in policy.get("min_kingdom", {}).items():
            if kingdom[key] < minimum:
                return False, "%s不足（需要 %d）" % (KINGDOM_LABELS[key], minimum)
        return True, ""

    def _format_policy_effect(policy):
        """把政务的王国数值变化格式化为 '国库 -200 · 稳定度 +8'。"""
        parts = []
        for key, amount in policy.get("kingdom", {}).items():
            parts.append("%s %+d" % (KINGDOM_LABELS[key], amount))
        return " · ".join(parts)

    def get_policy_choices():
        """返回供界面展示的政务列表，含可用状态。"""
        choices = []
        for policy in POLICIES:
            available, reason = is_policy_available(policy)
            choices.append({
                "id": policy["id"],
                "title": policy["title"],
                "desc": policy["desc"],
                "effect": _format_policy_effect(policy),
                "available": available,
                "reason": reason,
            })
        return choices

    def select_policy(policy_id):
        """提交当天的政务选择（不产生任何数值变化）。"""
        global selected_policy

        if day_settled:
            raise Exception("Cannot select policy after the day is settled.")

        if selected_policy is not None:
            raise Exception("Policy already selected today: " + str(selected_policy))

        policy = get_policy(policy_id)
        if policy is None:
            raise Exception("Unknown policy: " + str(policy_id))

        available, reason = is_policy_available(policy)
        if not available:
            raise Exception("Policy unavailable: " + reason)

        selected_policy = policy_id
        policy_history.append({"day": current_day, "policy": policy_id})
        return selected_policy

    # ---------- 结算 ----------

    def _snapshot_kingdom():
        return dict(kingdom)

    def _snapshot_characters():
        return {
            char_id: {"affection": data.get("affection", 0), "trust": data.get("trust", 0)}
            for char_id, data in characters.items()
        }

    def _diff_kingdom(before, after):
        """对比王国数值前后快照，返回变化列表。"""
        changes = []
        for key in ("gold", "stability", "diplomacy", "intel"):
            delta = after[key] - before[key]
            if delta != 0:
                changes.append({
                    "key": key,
                    "label": KINGDOM_LABELS[key],
                    "delta": delta,
                    "value": after[key],
                })
        return changes

    def _diff_characters(before, after):
        """对比角色数值前后快照，返回变化列表。"""
        changes = []
        for char_id, data in characters.items():
            for field in CHARACTER_VALUE_FIELDS:
                delta = after[char_id][field] - before[char_id][field]
                if delta != 0:
                    changes.append({
                        "char_id": char_id,
                        "name": data["name"],
                        "field": field,
                        "delta": delta,
                        "value": after[char_id][field],
                    })
        return changes

    def settle_day():
        """执行当天结算：应用政务效果、财政收支、随机/规则事件，返回结算报告。"""
        global day_settled

        if day_settled:
            raise Exception("Day already settled: " + str(current_day))

        before_kingdom = _snapshot_kingdom()
        before_characters = _snapshot_characters()
        notes = []

        policy = get_policy(selected_policy)
        if policy is not None:
            for key, amount in policy.get("kingdom", {}).items():
                change_kingdom_value(key, amount)
            for char_id, changes in policy.get("characters", {}).items():
                change_character_values(char_id, changes)
            notes.append("已执行政务：%s" % policy["title"])
        else:
            notes.append("今日未做任何政务决策，朝野议论纷纷。")
            change_kingdom_value("stability", -2)

        # 每日财政：收入随稳定度浮动
        income = DAILY_BASE_INCOME + kingdom["stability"] // 2
        change_kingdom_value("gold", income - DAILY_UPKEEP)
        notes.append("财政结算：收入 %d，支出 %d" % (income, DAILY_UPKEEP))

        # 国库空虚惩罚
        if kingdom["gold"] < LOW_GOLD_THRESHOLD:
            change_kingdom_value("stability", LOW_GOLD_STABILITY_PENALTY)
            notes.append("国库空虚（低于 %d），稳定度下降。" % LOW_GOLD_THRESHOLD)

        # 好感达标自动解锁个人路线
        for char_id, data in characters.items():
            if data.get("affection", 0) >= ROUTE_AFFECTION_THRESHOLD and not data.get("route_unlocked", False):
                unlock_character_route(char_id)
                notes.append("%s 的个人路线已解锁。" % data["name"])

        day_settled = True

        return {
            "day": current_day,
            "policy": policy["title"] if policy else None,
            "kingdom_changes": _diff_kingdom(before_kingdom, _snapshot_kingdom()),
            "character_changes": _diff_characters(before_characters, _snapshot_characters()),
            "notes": notes,
        }

    # ---------- 日期推进 ----------

    def set_phase(phase):
        """切换当前阶段（morning / event / settle）。"""
        global current_phase
        current_phase = phase

    def advance_day():
        """进入下一天，重置当天状态。必须在结算之后调用。"""
        global current_day, current_phase, day_settled, selected_policy

        if not day_settled:
            raise Exception("Cannot advance day before settlement.")

        current_day += 1
        current_phase = "morning"
        day_settled = False
        selected_policy = None
        return current_day

    def is_final_day(day=None):
        """判断某天是否为本 Demo 的最后一天（供界面显示不同按钮文案）。"""
        if day is None:
            day = current_day
        return day >= DEMO_MAX_DAY
