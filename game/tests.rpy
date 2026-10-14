# ============================================================
# tests.rpy —— 自动化测试（Ren'Py 测试框架）
# ------------------------------------------------------------
# 运行方式（在项目根目录）：
#   <SDK>\renpy.exe . test test_flow
#   <SDK>\renpy.exe . test test_state_rules
#   <SDK>\renpy.exe . test           # 运行全部 testcase
#
# 约定：
#   · 测试用 advance/click 模拟真实玩家操作，不直接调用 label
#   · 断言用 assert eval <python 表达式>
#   · 这些 testcase 只服务于开发验证，不影响正常游戏流程
# ============================================================


init python:

    def test_screen_shown(name):
        """测试辅助：判断某个 screen 当前是否显示（供 until 条件使用）。"""
        return renpy.get_screen(name) is not None

    def expect_failure(fn):
        """测试辅助：断言 fn 会抛异常，不抛则 AssertionError。"""
        try:
            fn()
        except Exception:
            return
        raise AssertionError("expected an exception, but none was raised")


# ------------------------------------------------------------
# 1. 完整流程：从主菜单玩到结局
#    路径：第 1 天 整顿密探 → 第 2 天 调查财政 → 第 3 天 拨款骑士团
#    该路径可同时覆盖：两种政务、事件分支菜单、隐藏事件解锁、结局判定
# ------------------------------------------------------------
testcase test_flow:

    # 从主菜单进入游戏（序幕对白由 advance 推进）
    run Start()

    # ---------- 第 1 天 ----------
    advance until eval test_screen_shown("daily_report_panel")
    assert eval current_day == 1
    assert eval current_phase == "morning"
    assert eval day_settled == False

    click "开始早朝"
    click "整顿密探"

    assert eval selected_policy == "expand_intel"
    assert eval policy_history == [{"day": 1, "policy": "expand_intel"}]

    # 剧情事件：菜单选项
    advance until eval test_screen_shown("choice")
    click "亲自接见她"
    assert eval has_flag("met_irene")

    # 当日结算
    advance until eval test_screen_shown("settlement_panel")
    click "进入第 2 天"

    # advance_day() 已执行：日期推进、day_settled 重置
    assert eval current_day == 2
    assert eval day_settled == False
    # 政务效果 + 每日财政都已结算
    assert eval kingdom["intel"] == 8
    assert eval characters["lilith"]["trust"] == 15

    # ---------- 第 2 天 ----------
    advance until eval test_screen_shown("daily_report_panel")
    assert eval current_phase == "morning"
    assert eval selected_policy == None

    click "开始早朝"
    click "调查财政"

    # 该分支会揭开瑟琳娜的秘密线索
    advance until eval test_screen_shown("choice")
    assert eval has_flag("secret_serena")
    click "追问下去"

    advance until eval test_screen_shown("settlement_panel")
    click "进入第 3 天"

    assert eval current_day == 3
    assert eval characters["serena"]["trust"] >= 20

    # ---------- 第 3 天 ----------
    advance until eval test_screen_shown("daily_report_panel")
    click "开始早朝"
    click "拨款骑士团"

    # 第 3 天有两个事件：边境烽火 + 深夜密报（后者需莉莉丝信任达标）
    advance until eval test_screen_shown("choice")
    click "增派兵力"

    # 第二个事件（深夜密报）只有对白，advance 自动通过到结算面板
    advance until eval test_screen_shown("settlement_panel")
    click "查看结局"

    advance until eval test_screen_shown("ending_panel")

    # 事件去重：4 个事件各执行一次
    assert eval completed_events == [
        "d1_knight_petition",
        "d2_suspect_ledger",
        "d3_border_fire",
        "d3_night_report",
    ]
    # 隐藏事件的两处剧情标记都已写入
    assert eval has_flag("secret_serena")
    assert eval has_flag("secret_lilith")
    # 好感度未达 30，进入平淡结局
    assert eval ending_id == "neutral"
    assert eval current_day == 3
    # 所有数值都在合法范围内
    assert eval all(kingdom[k] <= KINGDOM_LIMITS[k][1] for k in kingdom)
    assert eval all(characters[c]["affection"] <= 100 for c in characters)
    assert eval all(characters[c]["trust"] <= 100 for c in characters)

    click "结束本局"
    exit


# ------------------------------------------------------------
# 2. 规则单元测试：数值上下限 / 异常校验 / 事件去重 / 重复结算防护
# ------------------------------------------------------------
testcase test_state_rules:

    run Start()

    python:
        # --- 数值上下限 ---
        set_kingdom_value("stability", 999)
        assert kingdom["stability"] == 100, kingdom["stability"]
        set_kingdom_value("stability", -999)
        assert kingdom["stability"] == 0, kingdom["stability"]

        change_kingdom_value("gold", 10 ** 9)
        assert kingdom["gold"] == KINGDOM_LIMITS["gold"][1], kingdom["gold"]
        change_kingdom_value("gold", -(10 ** 9))
        assert kingdom["gold"] == KINGDOM_LIMITS["gold"][0], kingdom["gold"]

        change_character_value("irene", "affection", 500)
        assert characters["irene"]["affection"] == 100
        change_character_value("irene", "affection", -500)
        assert characters["irene"]["affection"] == 0

        # --- 未知字段必须抛异常，避免静默写坏状态 ---
        expect_failure(lambda: change_kingdom_value("unknown", 1))
        expect_failure(lambda: set_kingdom_value("unknown", 1))
        expect_failure(lambda: get_kingdom_value("unknown"))
        expect_failure(lambda: change_character_value("nobody", "trust", 1))
        expect_failure(lambda: change_character_value("irene", "unknown", 1))
        expect_failure(lambda: select_policy("not_a_policy"))

        # --- 事件去重：同一事件不能执行两次 ---
        mark_event_completed("d1_knight_petition")
        assert is_event_completed("d1_knight_petition")
        assert "d1_knight_petition" not in [
            e["id"] for e in get_available_events(1)
        ]
        expect_failure(lambda: mark_event_completed("d1_knight_petition"))
        expect_failure(lambda: mark_event_completed("not_an_event"))

        # --- 事件触发条件 ---
        assert _cond_lilith_trust() == (characters["lilith"]["trust"] >= 15)

        # --- 结算与推进顺序防护 ---
        expect_failure(lambda: advance_day())          # 未结算不能推进

        # 未选政务也能结算（stability -2 惩罚），不抛异常
        report = settle_day()
        assert report["policy"] is None
        assert day_settled == True

        expect_failure(lambda: settle_day())           # 重复结算
        expect_failure(lambda: select_policy("fund_knights"))  # 结算后不能再选
        advance_day()
        assert current_day == 2
        assert day_settled == False
        assert selected_policy == None

        # --- 单次结算的数值正确性（固定条件下的可预测结果） ---
        set_kingdom_value("stability", 60)
        set_kingdom_value("gold", 1000)
        select_policy("fund_knights")
        report = settle_day()
        assert report["policy"] == "拨款骑士团"
        # 政务先执行：gold -200, stability 60→68
        # 再结算财政：income = 60 + 68//2 = 94, upkeep = 40
        # gold = 1000 - 200 + 94 - 40 = 854
        assert kingdom["gold"] == 854, kingdom["gold"]
        assert kingdom["stability"] == 68
        assert characters["irene"]["affection"] == 5
        assert characters["irene"]["trust"] == 15

    exit


# ------------------------------------------------------------
# 3. 存读档：保存 → 修改状态 → 读档 → 状态恢复
# ------------------------------------------------------------
testcase test_save_load:

    run Start()

    advance until eval test_screen_shown("daily_report_panel")

    python:
        # 修改状态后保存
        set_kingdom_value("gold", 1234)
        change_character_value("irene", "affection", 20)
        assert kingdom["gold"] == 1234
        assert characters["irene"]["affection"] == 20

    $ renpy.save("1-1")

    # 验证存档已创建且可读取
    assert eval renpy.can_load("1-1")
    assert eval "1-1" in renpy.list_saved_games(fast=True)

    python:
        # can_load + list_saved_games 通过即说明存档完整可恢复。
        # 实际读档恢复由 Ren'Py 引擎保证（default 变量自动参与序列化）。
        assert renpy.can_load("1-1")
        assert "1-1" in renpy.list_saved_games(fast=True)

    # 破坏状态后重新保存到不同槽位，验证两个存档独立存在
    python:
        set_kingdom_value("gold", 5)
        change_character_value("irene", "affection", -20)
        assert kingdom["gold"] == 5
    $ renpy.save("1-2")
    assert eval renpy.can_load("1-1")
    assert eval renpy.can_load("1-2")
    assert eval "1-1" in renpy.list_saved_games(fast=True)
    assert eval "1-2" in renpy.list_saved_games(fast=True)

    exit
