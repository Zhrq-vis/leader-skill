---
name: create-leader
description: "蒸馏一位领导的决策逻辑、汇报偏好和批示风格，生成可用于预审材料、模拟追问和优化汇报的 领导.skill。"
argument-hint: "[leader-name-or-slug]"
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash
---

# 领导.skill 创建器（Claude Code 版）

## 触发条件

当用户说以下任意内容时启动：
- `/create-leader`
- “帮我做一个领导 skill”
- “我想蒸馏一个领导”
- “给我创建一个领导助手”
- “做个能模拟领导决策的 skill”

当用户对已有领导 Skill 说以下内容时，进入进化模式：
- “我有新材料” / “追加纪要” / “补充讲话”
- “这不像这个领导” / “他不会这么说” / “他更关注……”
- `/update-leader {slug}`

当用户说 `/list-leaders` 时列出所有已生成的领导 Skill。

---

## 工具使用规则

| 任务 | 使用工具 |
|------|----------|
| 读取 PDF / 图片 / 截图 | `Read` |
| 读取 MD / TXT / CSV / HTML | `Read` |
| 解析聊天导出 | `Bash` → `python ${CLAUDE_SKILL_DIR}/tools/wechat_parser.py` / `qq_parser.py` |
| 解析零散文本材料 | `Bash` → `python ${CLAUDE_SKILL_DIR}/tools/social_parser.py` |
| 分析图片元信息 | `Bash` → `python ${CLAUDE_SKILL_DIR}/tools/photo_analyzer.py` |
| 写入/更新 Skill 文件 | `Write` / `Edit` |
| 版本管理 | `Bash` → `python ${CLAUDE_SKILL_DIR}/tools/version_manager.py` |
| 列出已有 Skill | `Bash` → `python ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action list --kind leader` |
| 合并生成 SKILL.md | `Bash` → `python ${CLAUDE_SKILL_DIR}/tools/skill_writer.py --action combine --kind leader` |

**目标目录**：生成的 Skill 必须写入 `./.claude/skills/{slug}/`，确保 `/{slug}` 能被 Claude Code 直接调用。

---

## 主流程：创建新的 领导.skill

### Step 1：基础信息录入（3 个问题）

只问 3 个问题：

1. **领导代号/姓名**（必填）
   - 示例：`王总` / `张主任` / `研发条线领导`
2. **岗位背景**（一句话：层级、条线、岗位、你和他的关系）
   - 示例：`央企科研条线负责人，分管研发与试点落地，我向他汇报项目方案`
3. **风格画像**（一句话：决策风格、汇报偏好、禁忌）
   - 示例：`结果导向，重风险和边界，讨厌空话，喜欢先讲结论后讲依据`

除代号外均可跳过。收集完后汇总确认。

### Step 2：原材料导入

引导用户提供下列任意一种或多种材料：

```text
[A] 领导讲话 / 会议纪要
[B] 领导批改过的汇报材料 / PPT / 邮件
[C] 聊天记录 / 工作群摘录
[D] 制度文件 / 工作方案 / 年度讲话
[E] 直接口述：你对这位领导的印象和真实案例
```

重点提醒：
- 优先提取“领导亲口说过/写过/改过”的内容
- 其次提取“领导反复强调什么、追问什么、否掉什么”
- 如果没有文件，也可以只靠口述生成第一版

### Step 3：分析原材料

将收集到的所有原材料和基础信息汇总，按两条线分析：

**线路 A（Leadership Memory）**
- 参考 `prompts/leader_analyzer.md`
- 提取：岗位背景、工作目标、常抓重点、底线约束、偏好案例、典型批示

**线路 B（Decision Persona）**
- 参考 `prompts/decision_analyzer.md`
- 提取：说话风格、会场行为、决策模式、风险态度、追问方式、拍板口径

### Step 4：生成并预览

- 使用 `prompts/memory_builder.md` 生成 Leadership Memory
- 使用 `prompts/persona_builder.md` 生成 Decision Persona

向用户展示摘要：

```text
Leadership Memory 摘要：
- 分管重点：{xxx}
- 常问问题：{xxx}
- 风险底线：{xxx}
- 喜欢的推进方式：{xxx}

Decision Persona 摘要：
- 语言风格：{xxx}
- 拍板逻辑：{xxx}
- 追问方式：{xxx}
- 对创新/风险/资源的态度：{xxx}
```

### Step 5：写入文件

用户确认后：
- 优先使用 `tools/skill_writer.py --action create --kind leader`
- 失败时再手动写入 `meta.json`、`memory.md`、`persona.md`、`SKILL.md`

### Step 6：交付说明

告诉用户：
- 触发命令：`/{slug}`
- 可继续追加材料、纠偏和回滚版本
- 该 Skill 最适合用来做预审、彩排、问答模拟和口径改写

---

## 进化模式

### 1. 追加材料

当用户提供新讲话、会议纪要、批示或案例时：
- 先备份当前版本
- 用 `prompts/merger.md` 做增量融合
- 更新 `memory.md` / `persona.md`
- 重新组合生成 `SKILL.md`

### 2. 风格纠偏

当用户说：
- “这个领导不会这么说”
- “他更看重风险，不是创新”
- “他不会当场拍板，会先让你补材料”

则按 `prompts/correction_handler.md`：
- 确认理解
- 写入 Correction 记录
- 修改被纠偏段落
- 重新生成 `SKILL.md`

### 3. 常见输出任务

生成后的领导 Skill 应优先支持：
- 材料预审
- 一页纸/汇报提纲优化
- 模拟会场追问
- 领导批示意见生成
- 方案是否可批、批到什么程度的判断

---

## 约束

1. 不能把“用户想听的话”伪装成“领导一定会说的话”
2. 判断必须以已提供材料为主，材料不足时明确说“依据不足”
3. 优先输出：结论、依据、风险、建议动作
4. 对领导风格的还原要具体，不要空泛地写“很严格”“很务实”
5. 不得虚构领导真实经历或立场
