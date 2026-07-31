# gongkao-interview-question

> WorkBuddy Skill：公考面试结构化答题批量生成

为公考面试结构化培训的 **Obsidian 知识库** 批量生成高质量面试题。覆盖综合分析、组织计划、人际关系、应急应变、自我认知、言语表达六类题型，每道题包含 frontmatter 元信息、题干（≤80字）、思路大纲（破题角度 + 3个核心观点）、800-900字逐字稿，集成 Python 脚本进行 AI 痕迹扫描和用语禁忌检查。

---

## 功能亮点

- **6 步标准化工流**：选题 → 撰写 → 字数验证 → AI痕迹扫描 → 写入md → 批量生产
- **6 条内容铁律**：有观点、有逻辑、有表达、避套路、拒假大空、接地气可操作
- **Python 自动化验证**：`validate_question.py` 自动统计字数、扫描 6 类 AI 痕迹 + 4 类用语禁忌
- **humanizer-zh 深度集成**：逐字稿经过去 AI 味儿处理，避免"标志着/彰显了/体现了"等套路表达
- **批量生产策略**：先样例后铺量，每道必跑验证脚本，零命中才过关
- **Obsidian 兼容**：生成标准 md 文件，含 frontmatter 元信息和三级标签体系

---

## 目录结构

```
gongkao-interview-question/
├── SKILL.md                  # skill 定义文件（核心）
├── README.md                 # 本文件
├── scripts/
│   └── validate_question.py  # Python 验证脚本（字数 + AI痕迹 + 用语禁忌）
└── test-prompts.json         # 测试用例（3 个 prompt）
```

---

## 安装方式

### 方法一：从 zip 安装

1. 下载 `gongkao-interview-question.zip`
2. 解压到 WorkBuddy 的 skills 目录：
   - **WorkBuddy Desktop**：`~/.workbuddy/skills/gongkao-interview-question/`
   - 确保目录名即为 `gongkao-interview-question`
3. 在 WorkBuddy 中即可通过触发词调用

### 方法二：从 GitHub 安装

```bash
cd ~/.workbuddy/skills/
git clone https://github.com/rshawn0307-maker/gongkao-interview-question.git
```

---

## 使用方式

在 WorkBuddy 中说以下任意触发词即可：

- "面试题库" / "出面试题" / "公考面试题"
- "批量出题" / "题库填充" / "填充题库"
- "面试逐字稿" / "出题加答题"

### 工作流示意

```
用户说出触发词
    ↓
步骤1: AI 提出选题清单 → 🛑 用户确认
    ↓
步骤2: 按 6 条铁律撰写内容
    ↓
步骤3: 跑 validate_question.py 验证字数
    ↓
步骤4: 扫描 AI 痕迹 + 用语禁忌 → 改写至零命中
    ↓
步骤5: 写入 Obsidian 题库文件夹
    ↓
步骤6: 先 6 道样例 → 🛑 用户确认 → 批量生产
```

---

## 验证脚本

`scripts/validate_question.py` 提供完整的自动化检查：

```bash
# 单文件验证
python scripts/validate_question.py 综合分析_01_指尖形式主义.md

# 批量验证
python scripts/validate_question.py 综合分析_*.md
```

检查项：
| 类别 | 内容 |
|------|------|
| 字数统计 | 逐字稿 800-930 字（含标点） |
| AI 痕迹（6类） | 标志性短语、三段式列举、破折号过度、模糊归因、否定排比、万能收束 |
| 公考高危词 | "体现/彰显/凸显""深入推进/全面落实""多措并举/综合施策"等 |
| 用语禁忌（4类） | 贬义比喻、网络流行词、情绪化表达、政治风险表述 |
| 结构检查 | 机械三段式（第一/第二/第三连续） |

---

## 适用场景

- 公考面试结构化培训的题库建设
- 公务员/事业单位面试备考资料生成
- 面试培训机构的内容标准化
- 个人面试练习的题目来源

---

## 版本

- **当前版本**：v1.0.0
- **更新日期**：2026-06-30
- **darwin-skill 优化评分**：81.3/100

---

## 许可

本 skill 为个人作品，供学习交流使用。
