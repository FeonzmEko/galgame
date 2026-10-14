# 王国经营 × 视觉小说 Demo

> 女王即位三日，每一道政令都将改变王国的命运。

## 简介

玩家扮演新即位的女王，在 3 天内通过政务决策与剧情事件管理王国数值（国库、稳定度、外交、情报），推进三位女主（艾琳 / 瑟琳娜 / 莉莉丝）的好感与信任，最终达成不同结局。

### 三位女主

| 角色 | 身份 | 关键数值 |
|------|------|---------|
| 艾琳 | 骑士团长 | 好感 / 信任 |
| 瑟琳娜 | 宫廷财政顾问 | 好感 / 信任 |
| 莉莉丝 | 首席情报官 | 好感 / 信任 |

### 政务选项

| 政务 | 效果 |
|------|------|
| 拨款骑士团 | 国库 -200，稳定度 +8，艾琳好感/信任 +5 |
| 调查财政 | 国库 +150，稳定度 -4，瑟琳娜信任 +6 |
| 整顿密探 | 国库 -100，情报 +8，莉莉丝好感 +3 / 信任 +5 |

### 结局

- **平淡结局** (neutral) — 3 天结束，无人好感达 30
- **个人路线结局** — 某位女主好感 ≥ 30 时解锁
- **繁荣结局** / **覆灭结局** — 由王国稳定度与国库决定

## 运行

### 环境要求

- Ren'Py 8.5.3 SDK
- Windows / macOS / Linux

### 启动游戏

```powershell
D:\tools\renpy-sdk\renpy-8.5.3-sdk\renpy.exe D:\code\galgame
```

或通过 Ren'Py Launcher 打开项目目录。

### 玩法

1. 阅读序幕对白
2. 每天早晨查看 **晨间报告**（王国状态 + 角色信息）
3. 进入 **早朝议事**，选择一项政务
4. 处理 **剧情事件**（可能包含选项，影响角色数值与剧情走向）
5. 查看 **当日结算**（政务效果 + 财政收支 + 数值变化）
6. 进入下一天，直到第 3 天结束进入结局

## 开发

### Lint 检查

```powershell
D:\tools\renpy-sdk\renpy-8.5.3-sdk\renpy.exe D:\code\galgame lint
```

### 运行测试

```powershell
# 完整流程测试（23 个断言）
D:\tools\renpy-sdk\renpy-8.5.3-sdk\renpy.exe D:\code\galgame test test_flow

# 规则单元测试（数值 clamp / 异常校验 / 事件去重 / 结算顺序）
D:\tools\renpy-sdk\renpy-8.5.3-sdk\renpy.exe D:\code\galgame test test_state_rules

# 存读档测试（6 个断言）
D:\tools\renpy-sdk\renpy-8.5.3-sdk\renpy.exe D:\code\galgame test test_save_load
```

### 项目结构

```
game/
├── script.rpy              主流程编排
├── variables.rpy           状态变量（default 声明）
├── characters.rpy          Character 对象
├── images.rpy              占位图像
├── tests.rpy               自动化测试
├── screens/                UI 面板
├── systems/                游戏逻辑系统
│   ├── state_manager.rpy   状态变更接口
│   ├── daily_manager.rpy   政务与结算
│   ├── event_manager.rpy   事件系统
│   └── ending_manager.rpy  结局判定
└── events/                 每日剧情事件
```

### 架构约定

- **所有数值变更** 必须通过 `state_manager` 函数（自动 clamp + 校验）
- **事件 id 唯一**，执行后标记完成不可重复
- **结算与推进** 由 `daily_manager` 统一执行，面板只提交选择
- **所有状态变量** 用 `default` 声明在 `variables.rpy`，确保存档/回滚兼容

详细指南见 [AGENTS.md](AGENTS.md)。

## 技术栈

- **引擎**: Ren'Py 8.5.3
- **分辨率**: 1920×1080
- **语言**: 中文
- **美术**: 占位纯色（Solid），后续替换为正式美术资源
