# ============================================================
# state_manager.rpy —— 统一状态修改入口（游戏逻辑层）
# ------------------------------------------------------------
# 全项目唯一允许修改 kingdom / characters / story_flags 的地方。
# 剧情脚本只调用这里的函数，不直接赋值，便于统一调整数值规则。
# ============================================================

# 各王国数值的合理上下限（不同字段上限不同，避免"一刀切"）
define KINGDOM_LIMITS = {
    "gold": (0, 100000),
    "stability": (0, 100),
    "diplomacy": (0, 100),
    "intel": (0, 100),
}

# 角色数值上下限
define CHARACTER_VALUE_LIMITS = (0, 100)

# 角色可修改的数值字段白名单
define CHARACTER_VALUE_FIELDS = ("affection", "trust")

# 王国数值的中文显示名（供界面复用）
define KINGDOM_LABELS = {
    "gold": "国库",
    "stability": "稳定度",
    "diplomacy": "外交",
    "intel": "情报",
}

init -1 python:

    def _clamp(value, low, high):
        """把数值裁剪到 [low, high] 区间。"""
        return max(low, min(high, value))

    def change_kingdom_value(key, amount):
        """按字段上限修改王国数值，返回修改后的值。

        key    王国字段名（gold / stability / diplomacy / intel）
        amount 变化量，可正可负
        """
        if key not in KINGDOM_LIMITS:
            raise Exception("Unknown kingdom field: " + str(key))

        low, high = KINGDOM_LIMITS[key]
        kingdom[key] = _clamp(kingdom[key] + amount, low, high)
        return kingdom[key]

    def set_kingdom_value(key, value):
        """直接设定王国数值（同样受上下限约束），返回设定后的值。"""
        if key not in KINGDOM_LIMITS:
            raise Exception("Unknown kingdom field: " + str(key))

        low, high = KINGDOM_LIMITS[key]
        kingdom[key] = _clamp(value, low, high)
        return kingdom[key]

    def get_kingdom_value(key):
        """读取王国数值。"""
        if key not in KINGDOM_LIMITS:
            raise Exception("Unknown kingdom field: " + str(key))
        return kingdom[key]

    def change_character_value(char_id, key, amount):
        """修改角色数值，返回修改后的值。

        char_id 角色 id（characters 的键）
        key     字段名（affection / trust）
        amount  变化量，可正可负
        """
        if char_id not in characters:
            raise Exception("Unknown character: " + str(char_id))

        if key not in CHARACTER_VALUE_FIELDS:
            raise Exception("Unknown character field: " + str(key))

        low, high = CHARACTER_VALUE_LIMITS
        current = characters[char_id].get(key, low)
        characters[char_id][key] = _clamp(current + amount, low, high)
        return characters[char_id][key]

    def change_character_values(char_id, changes):
        """一次性修改角色的多个字段。

        changes 形如 {"affection": 5, "trust": -2}
        """
        for key, amount in changes.items():
            change_character_value(char_id, key, amount)

    def unlock_character_route(char_id):
        """解锁角色个人路线。"""
        if char_id not in characters:
            raise Exception("Unknown character: " + str(char_id))
        characters[char_id]["route_unlocked"] = True

    def advance_character_story(char_id, amount=1):
        """推进角色个人剧情进度。"""
        if char_id not in characters:
            raise Exception("Unknown character: " + str(char_id))
        characters[char_id]["story_stage"] = characters[char_id].get("story_stage", 0) + amount

    # ---------- 剧情标记 ----------

    def set_flag(flag, value=True):
        """设置剧情标记。"""
        story_flags[flag] = value

    def get_flag(flag, default=False):
        """读取剧情标记，不存在时返回 default。"""
        return story_flags.get(flag, default)

    def has_flag(flag):
        """剧情标记是否为真。"""
        return bool(story_flags.get(flag, False))

    # ---------- 查询辅助（供界面使用） ----------

    def top_character():
        """返回好感度最高的角色 id（并列时按定义顺序取前者）。"""
        best_id = None
        best_value = -1
        for char_id in characters:
            value = characters[char_id].get("affection", 0)
            if value > best_value:
                best_value = value
                best_id = char_id
        return best_id
