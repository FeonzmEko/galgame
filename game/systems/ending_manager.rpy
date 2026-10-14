# ============================================================
# ending_manager.rpy —— 结局判定（游戏逻辑层）
# ------------------------------------------------------------
# 每天结算后调用 check_ending()：
#   返回 None        继续下一天
#   返回结局 id      script.rpy 跳转到对应结局 label
# ============================================================

init -1 python:

    # 结局注册表：id -> 展示信息
    ENDINGS = {
        "collapse": {
            "title": "王座倾覆",
            "desc": "稳定度归零，王国在动荡中崩塌。",
        },
        "neutral": {
            "title": "平静的日常",
            "desc": "王国安然度过这段时光，但没有人真正走进你心里。",
        },
        "route_irene": {
            "title": "剑与誓言",
            "desc": "骑士团长艾琳将剑交付于你，誓言共守这片疆土。",
        },
        "route_serena": {
            "title": "账簿之后",
            "desc": "财政顾问瑟琳娜放下账簿，第一次直视你的眼睛。",
        },
        "route_lilith": {
            "title": "暗影同盟",
            "desc": "情报官莉莉丝将最深的秘密交给你保管。",
        },
    }

    # 进入角色路线所需的好感度门槛
    ROUTE_AFFECTION_THRESHOLD = 30

    def get_ending(ending_id):
        """按 id 取结局信息。"""
        return ENDINGS.get(ending_id)

    def _route_ending():
        """按好感度决定角色路线结局，未达标则为平淡结局。"""
        best_id = top_character()
        if best_id is None:
            return "neutral"

        if characters[best_id].get("affection", 0) >= ROUTE_AFFECTION_THRESHOLD:
            if characters[best_id].get("route_unlocked", False):
                return "route_" + best_id

        return "neutral"

    def check_ending():
        """判定是否应当结束游戏，返回结局 id 或 None。"""
        if kingdom["stability"] <= 0:
            return "collapse"

        # Demo 在第 DEMO_MAX_DAY 天结算后结束
        if current_day >= DEMO_MAX_DAY:
            return _route_ending()

        return None

    def set_ending(new_ending_id):
        """记录最终结局。"""
        global ending_id
        if new_ending_id not in ENDINGS:
            raise Exception("Unknown ending: " + str(new_ending_id))
        ending_id = new_ending_id
        return ending_id
