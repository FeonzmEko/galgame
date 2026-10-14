# AGENTS.md — AI Agent 上下文指南

> 本文件为 AI 编码助手提供项目上下文。编辑代码前请先通读此文件。

## 项目概述

**王国经营 × 视觉小说** Demo。玩家扮演女王，在 3 天内通过政务决策与剧情事件管理王国数值、推进三位女主（艾琳 / 瑟琳娜 / 莉莉丝）的好感与信任，最终达成不同结局。

- **引擎**: Ren'Py 8.5.3（纯原生，无 Web 前端）
- **分辨率**: 1920×1080
- **语言**: 中文
- **Demo 天数**: 3 天（`DEMO_MAX_DAY`）

## 开发环境

```
项目根目录:  D:\code\galgame
Ren'Py SDK:  D:\tools\renpy-sdk\renpy-8.5.3-sdk
```

### 常用命令

```powershell
# 运行游戏
D:\tools\renpy-sdk\renpy-8.5.3-sdk\renpy.exe D:\code\galgame

# Lint 检查
D:\tools\renpy-sdk\renpy-8.5.3-sdk\renpy.exe D:\code\galgame lint

# 运行单个测试
D:\tools\renpy-sdk\renpy-8.5.3-sdk\renpy.exe D:\code\galgame test test_flow
D:\tools\renpy-sdk\renpy-8.5.3-sdk\renpy.exe D:\code\galgame test test_state_rules
D:\tools\renpy-sdk\renpy-8.5.3-sdk\renpy.exe D:\code\galgame test test_save_load
```

> **注意**: 必须使用 `renpy.exe`，不能用 `python renpy.py`（会报 `ModuleNotFoundError`）。

## 文件结构

```
game/
├── script.rpy              # 主流程编排（start → prologue → main_loop → ending_flow）
├── variables.rpy           # 所有 default 状态变量（save/rollback 的基础）
├── characters.rpy          # Character 对象定义
├── images.rpy              # 占位图像（Solid 纯色）
├── tests.rpy               # 自动化测试（3 个 testcase）
├── options.rpy             # Ren'Py 引擎配置
├── gui.rpy                 # GUI 样式配置
├── screens/
│   ├── kingdom_panel.rpy   # 早朝议事面板（选政务）
│   ├── character_panel.rpy # 角色信息面板
│   ├── event_panel.rpy     # 晨间报告 / 当日结算 / 结局面板
│   └── ui_common.rpy       # 共享 UI 组件（HUD、标题栏、数值条等）
├── systems/
│   ├── state_manager.rpy   # 统一状态变更接口（change/set/get + 边界 clamp）
│   ├── daily_manager.rpy   # 政务注册表 + 每日结算 + 日期推进
│   ├── event_manager.rpy   # 事件注册/查询/去重/条件判定
│   └── ending_manager.rpy  # 结局判定与结局数据
└── events/
    ├── common.rpy          # 通用事件 label（无事发生等）
    ├── day01.rpy           # 第 1 天剧情事件
    ├── day02.rpy           # 第 2 天剧情事件
    └── day03.rpy           # 第 3 天剧情事件
```

## 核心架构约定

### 1. 状态管理（state_manager.rpy）

**所有**王国/角色数值变更必须通过 `state_manager` 函数，禁止直接赋值：

```python
# ✅ 正确
change_kingdom_value("gold", -200)
set_kingdom_value("stability", 60)
change_character_value("irene", "affection", 5)
change_character_values("lilith", {"affection": 3, "trust": 5})

# ❌ 错误（绕过 clamp 和校验）
kingdom["gold"] -= 200
characters["irene"]["affection"] += 5
```

- `change_kingdom_value(key, delta)` — 增量变更，自动 clamp 到 `KINGDOM_LIMITS`
- `set_kingdom_value(key, value)` — 绝对赋值，自动 clamp
- `change_character_value(char_id, field, delta)` — 角色数值增量
- `change_character_values(char_id, changes_dict)` — 角色多字段批量变更
- `select_policy(policy_id)` — 提交政务选择（不产生数值变化，结算时才应用）
- `set_flag(name)` / `has_flag(name)` — 剧情标记管理

### 2. 事件系统（event_manager.rpy）

每个事件有唯一 `id`，执行后标记完成，不可重复：

```python
# 事件注册（init 阶段）
register_event("d1_knight_petition", day=1, label="event_day01", cond=None)

# 查询当天可用事件
events = get_available_events(1)  # 返回未完成且条件满足的事件列表

# 标记完成
mark_event_completed("d1_knight_petition")
```

- 事件条件用函数（如 `_cond_lilith_trust`），返回 bool
- `get_available_events(day)` 自动过滤已完成和条件不满足的事件

### 3. 每日循环（script.rpy main_loop）

```
晨间报告 (daily_report_panel)
  → 早朝议事 (kingdom_panel → select_policy)
  → 剧情事件 (play_daily_event → 逐个 call expression event["label"])
  → 当日结算 (settle_day → settlement_panel)
  → 结局判定 (check_ending → ending_panel if ending)
  → 下一天 (advance_day)
```

**关键约定**: 经营面板按钮只提交选择（`select_policy`），不推进日期。结算和推进由 `daily_manager` 统一执行，避免重复结算。

### 4. 存档/回滚

- 所有游戏状态用 `default` 声明在 `variables.rpy`，确保参与 save/rollback
- `settle_day()` 和 `advance_day()` 是唯一的结算/推进入口
- 测试中用 `renpy.save("1-1")` / `renpy.can_load("1-1")` 验证存档

## UI 约定

- 主色调: 金色 `#c9a227`（`KUI_ACCENT`）
- 背景色: `#141b28`（`KUI_BG`）、`#1f2937`（`KUI_PANEL`）
- 面板用 `modal True` 防止点击穿透
- 数值条用 `kui_value_bar` 复用组件
- 按钮文字用中文，`textbutton` + `action Return(value)`

## 测试

3 个 testcase 覆盖：

| testcase | 覆盖内容 | 断言数 |
|----------|---------|--------|
| `test_flow` | 完整 3 天流程 → 平淡结局 | 23 |
| `test_state_rules` | 数值 clamp / 异常校验 / 事件去重 / 结算顺序 | python block |
| `test_save_load` | 存档创建 / 多槽位独立 / can_load 验证 | 6 |

测试辅助函数在 `tests.rpy` 的 `init python` 块中定义：
- `test_screen_shown(name)` — 判断 screen 是否显示（供 `until eval` 条件使用）
- `expect_failure(fn)` — 断言 fn 抛异常

## 常见陷阱

1. **不要用 `python renpy.py`** — 必须用 `renpy.exe`
2. **不要直接赋值 kingdom/characters** — 必须走 state_manager
3. **不要在面板按钮里调用 settle_day/advance_day** — 只在 main_loop 中调用
4. **事件 id 必须唯一** — 重复 id 会在 mark_event_completed 时抛异常
5. **新增 default 变量** — 必须加在 `variables.rpy`，否则不参与 save/rollback
6. **GUI 按钮图片** — `game/gui/button/` 下需要对应的 `*_background.png` 文件
