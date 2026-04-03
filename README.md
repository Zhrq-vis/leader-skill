<div align="center">

# 领导.skill

> *“先别急着汇报，先让领导过一遍。”*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

<br>

有些材料不是写给技术专家看的，而是写给领导拍板的。<br>
有些项目不是做不出来，而是**讲不过会、过不了会、立不了项**。<br>

**领导.skill** 用来蒸馏一位领导的管理风格、决策逻辑、关注重点和批示口径，<br>
让你在真正汇报之前，先跟“领导”过一遍。<br>

<br>

你可以提供领导讲话、汇报材料批注、会议纪要、邮件、制度文件、项目方案，<br>
系统会将其解构为两部分：<br>
**Part A — Leadership Memory（领导记忆） + Part B — Decision Persona（决策人格）**<br>
生成一个可用于预审材料、模拟问答、优化汇报的一线领导助手。

[安装](#安装) · [使用](#使用) · [效果示例](#效果示例) · [English](README_EN.md)

</div>

---

## 安装

### Claude Code

> **重要**：Claude Code 从 **git 仓库根目录** 的 `.claude/skills/` 查找 skill。请在正确的位置执行。

```bash
mkdir -p .claude/skills
git clone https://github.com/YOUR_USERNAME/leader-skill .claude/skills/create-leader

# 或安装到全局
# git clone https://github.com/YOUR_USERNAME/leader-skill ~/.claude/skills/create-leader
```

### 依赖（可选）

```bash
pip install -r requirements.txt
```

---

## 使用

在 Claude Code 中输入：

```bash
/create-leader
```

按提示录入领导名称、层级、岗位背景和风格描述，再导入原材料。完成后可通过 `/{slug}` 调用该领导 Skill。

### 管理命令

| 命令 | 说明 |
|------|------|
| `/list-leaders` | 列出所有已生成的领导 Skill |
| `/{slug}` | 完整模式：像领导一样评估、批示、追问 |
| `/{slug}-memory` | 领导档案模式：查看领导经历、偏好、常见关注点 |
| `/{slug}-persona` | 决策人格模式：仅保留领导的风格和拍板方式 |
| `/leader-rollback {slug} {version}` | 回滚到历史版本 |
| `/delete-leader {slug}` | 删除 |

---

## 效果示例

> 输入：`某央企研发条线领导，结果导向，重风险、重落地、讨厌空话，喜欢“三点讲清楚”。`

**场景一：预审项目方案**

```text
用户        ❯ 这个量子交通优化项目，领导会不会支持？

领导.skill  ❯ 方向可以谈，但别一上来讲“颠覆式创新”。
              我会先看三件事：
              第一，现网是不是不用大改；
              第二，试点范围是不是收得住；
              第三，效果是不是能量化到通行效率、排队长度、群众感知。

              现在这个方案技术味太重，业务闭环还不够。
              建议先按“小范围、可验证、可复用”重写。
```

**场景二：改领导汇报口径**

```text
用户        ❯ 帮我把这段技术汇报改成领导能接受的版本。

领导.skill  ❯ 这段最大的问题不是不专业，而是没有先说结论。
              改成：
              “目前已完成四路口实测数据接入和区域仿真验证，初步结果表明车辆通行效率较基线方案有明显提升。
              下一步拟在不改变现有信号控制总体机制的前提下，开展小范围试点优化验证。”
```

**场景三：模拟会场追问**

```text
用户        ❯ 领导可能会追问我什么？

领导.skill  ❯ 我大概率会追问：
              1. 这件事不做会怎样，为什么现在做？
              2. 试点边界在哪里，出问题谁兜底？
              3. 和现有方案相比，提升到底有多少，怎么算出来的？
```

---

## 功能特性

### 数据源

| 来源 | 格式 | 备注 |
|------|------|------|
| 领导讲话/会议纪要 | TXT / MD / PDF / 截图 | 提取关注重点、口头偏好、批示风格 |
| 汇报材料批注 | PDF / Word 转文本 / 图片 | 提取领导真实修改偏好 |
| 邮件/聊天记录 | txt / html / csv / 导出记录 | 提取问责方式、表达习惯、决策逻辑 |
| 制度文件/工作方案 | MD / TXT / PDF | 提取领导长期强调的原则和底线 |
| 直接口述 | 纯文本 | 补充你对领导风格的理解 |

### 生成的 Skill 结构

每个领导 Skill 由两部分组成：

| 部分 | 内容 |
|------|------|
| **Part A — Leadership Memory** | 任职背景、常抓重点、业务偏好、风险底线、常见关注问题、典型批示 |
| **Part B — Decision Persona** | 5 层决策人格：硬规则 → 身份锚点 → 语言风格 → 决策模式 → 会场行为 |

运行逻辑：`收到材料/问题 → Decision Persona 判断领导会怎么看、怎么问、怎么表态 → Leadership Memory 补充背景、约束和历史偏好 → 输出领导式评审/批示`

### 典型用途

- 立项前预审
- PPT/汇报材料改写
- 模拟领导追问
- 批示意见生成
- 项目风险体检
- “能不能批、怎么批、先批到哪一步” 的决策演练

### 进化机制

- **追加材料**：导入新的讲话、会议纪要、批示记录，自动增量融合
- **人工纠偏**：你可以说“这个领导不会这么讲”“他更关注风险不是创新”，即时修正
- **版本管理**：每次更新自动存档，支持回滚

---

## 项目结构

```text
create-leader/
├── SKILL.md
├── prompts/
│   ├── intake.md
│   ├── leader_analyzer.md
│   ├── decision_analyzer.md
│   ├── memory_builder.md
│   ├── persona_builder.md
│   ├── merger.md
│   └── correction_handler.md
├── tools/
│   ├── wechat_parser.py
│   ├── qq_parser.py
│   ├── social_parser.py
│   ├── photo_analyzer.py
│   ├── skill_writer.py
│   └── version_manager.py
├── leaders/
├── docs/PRD.md
├── requirements.txt
└── LICENSE
```

---

## 注意事项

- 这不是“万能领导模拟器”，而是 **基于材料证据的领导风格蒸馏器**。
- 原材料越接近真实决策场景，还原度越高。**讲话 + 批注 + 会议纪要** 的组合最好。
- 建议优先提供：
  1. 领导改过的材料
  2. 领导在会上否掉/通过某事的真实表达
  3. 领导反复强调的风险点、边界和底线
  4. 领导喜欢的汇报结构
- 适合用于预演和复盘，不适合作为对真实领导意图的绝对替代。

---

## 致谢

感谢以下开源思路带来的启发：

- colleague-skill
- ex-partner-skill
- yourself-skill
- OpenAI skills / AgentSkills 生态
- GPT-5.4
- Claude Code
- VS Code
