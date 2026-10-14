# ============================================================
# variables.rpy —— 全局游戏状态定义（游戏状态层）
# ------------------------------------------------------------
# 规则：
#   1. 所有随存档保存的游戏状态都在此文件用 default 声明，
#      保证读档 / 回滚时状态一致，避免读取不存在的字段。
#   2. 禁止在剧情脚本中直接给这些变量赋值，必须通过
#      systems/state_manager.rpy 的统一入口函数修改。
#   3. 只在此文件放"数据"，不放逻辑；逻辑放 systems/ 下。
# ------------------------------------------------------------
# 四类状态：
#   时间状态  current_day / current_phase / day_settled
#   王国状态  kingdom / selected_policy / policy_history
#   角色状态  characters
#   剧情状态  story_flags / completed_events / ending_id
# ============================================================

# ------------------------------------------------------------
# 1. 时间状态 —— 记录当前推进到哪一天、哪个阶段
#    phase 取值：morning（早朝议事）→ event（剧情事件）→ settle（当日结算）
# ------------------------------------------------------------
default current_day = 1
default current_phase = "morning"
default day_settled = False

# ------------------------------------------------------------
# 2. 王国状态 —— 经营数值与政务决策
#    上限由 systems/state_manager.rpy 的 KINGDOM_LIMITS 统一约束
# ------------------------------------------------------------
default kingdom = {
    "gold": 1000,       # 国库（金币）
    "stability": 60,    # 稳定度 0-100
    "diplomacy": 40,    # 外交关系 0-100
    "intel": 0,         # 情报值 0-100
}

# 当天已选政务（策略 id），未选择时为 None
default selected_policy = None
# 历史政务决策，元素形如 {"day": 1, "policy": "fund_knights"}
default policy_history = []

# ------------------------------------------------------------
# 3. 角色状态 —— 每位女主的好感、信任与个人剧情进度
#    affection / trust 上限由 CHARACTER_VALUE_LIMITS 统一约束
# ------------------------------------------------------------
default characters = {
    "irene": {
        "name": "艾琳",
        "title": "骑士团长",
        "affection": 0,          # 好感度 0-100
        "trust": 10,             # 信任度 0-100
        "route_unlocked": False, # 个人路线是否解锁
        "story_stage": 0,        # 个人剧情进度（0 起）
    },
    "serena": {
        "name": "瑟琳娜",
        "title": "宫廷财政顾问",
        "affection": 0,
        "trust": 10,
        "route_unlocked": False,
        "story_stage": 0,
    },
    "lilith": {
        "name": "莉莉丝",
        "title": "首席情报官",
        "affection": 0,
        "trust": 10,
        "route_unlocked": False,
        "story_stage": 0,
    },
}

# ------------------------------------------------------------
# 4. 剧情状态 —— 关键选择、隐藏线索、路线与结局标记
#    story_flags 存剧情条件（如 found_secret_ledger），
#    不要把剧情条件混进角色属性。
# ------------------------------------------------------------
default story_flags = {}
default completed_events = []
default ending_id = None
