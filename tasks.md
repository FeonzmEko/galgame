# 任务跟踪

## 已完成

### T1 — 项目初始化 ✅

- Ren'Py 8.5.3 项目骨架（`options.rpy` / `gui.rpy`）
- `variables.rpy`：所有 `default` 状态变量（王国数值、角色数据、剧情标记）
- `characters.rpy`：Character 对象（女王、大臣、旁白）
- `images.rpy`：占位背景（Solid 纯色）
- `.gitignore`：排除 saves / cache / rpyc / 日志

### T2 — 状态管理系统 ✅

- `systems/state_manager.rpy`：统一变更接口
  - `change_kingdom_value` / `set_kingdom_value` / `get_kingdom_value`
  - `change_character_value` / `change_character_values`
  - `select_policy` / `set_flag` / `has_flag`
  - 自动 clamp 到 `KINGDOM_LIMITS` / `CHARACTER_VALUE_LIMITS`
  - 未知字段抛异常，避免静默写坏状态

### T3 — UI 面板 ✅

- `screens/ui_common.rpy`：共享组件（HUD、标题栏、数值条、角色卡片）
- `screens/kingdom_panel.rpy`：早朝议事面板（3 个政务选项 + 可用性置灰）
- `screens/character_panel.rpy`：角色信息面板
- `screens/event_panel.rpy`：晨间报告 / 当日结算 / 结局面板
- 主色调金色 `#c9a227`，深色背景 `#141b28`

### T4 — 主流程 + 事件 ✅

- `script.rpy`：主循环编排（晨间报告 → 早朝 → 事件 → 结算 → 结局 → 下一天）
- `systems/daily_manager.rpy`：政务注册表 + 每日结算 + 日期推进
- `systems/event_manager.rpy`：事件注册 / 查询 / 去重 / 条件判定
- `systems/ending_manager.rpy`：结局判定（平淡 / 个人路线 / 繁荣 / 覆灭）
- `events/day01.rpy`：骑士请愿（艾琳初遇）
- `events/day02.rpy`：账簿疑云（瑟琳娜秘密线索）
- `events/day03.rpy`：边境烽火 + 深夜密报（莉莉丝隐藏事件）
- `events/common.rpy`：无事发生

### T5 — 测试 + 存读档 ✅

- `tests.rpy`：3 个 testcase
  - `test_flow`：完整 3 天流程 → 平淡结局（23 个断言）
  - `test_state_rules`：数值 clamp / 异常校验 / 事件去重 / 结算顺序
  - `test_save_load`：存档创建 / 多槽位独立 / can_load 验证（6 个断言）
- Lint 通过：37 对白块 / 3 菜单 / 5 图像 / 34 屏幕，无错误

### 项目文档 ✅

- `AGENTS.md`：AI Agent 上下文指南
- `README.md`：项目说明
- `tasks.md`：本文件

## 后续路线图

### P1 — 内容扩展

- [ ] 增加更多政务选项（外交出使、情报刺探、民生工程）
- [ ] 丰富每日事件（随机事件池 + 条件触发）
- [ ] 个人路线剧情（好感达标后解锁专属事件链）
- [ ] 更多结局变体（好感 + 王国数值组合判定）

### P2 — 美术接入

- [ ] 角色立绘（待定美术风格）
- [ ] 背景图（王座大厅、边境、书房、夜景）
- [ ] CG 插画（关键剧情节点）
- [ ] UI 图标替换（金币、稳定度、外交、情报）

### P3 — 系统增强

- [ ] 回忆模式（CG 回顾 + 事件回顾）
- [ ] 结局图鉴（已达成结局列表）
- [ ] 快速跳过 / 自动模式
- [ ] 多周目继承（部分标记或数值继承到新周目）
- [ ] 难度调节（政务效果倍率 / 事件触发阈值可调）

### P4 — 打磨

- [ ] BGM / SE 音效
- [ ] 转场动画细化
- [ ] 文字打字机效果 + 点击跳过
- [ ] 多语言支持（i18n）
