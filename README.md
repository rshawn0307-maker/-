# 🧰 rshawn-skills

Shawn 的个人 AI Agent Skill 合集，遵循 Agent Skills 开放标准。每个 skill 都是自包含目录（`SKILL.md` + 可选 `scripts/`、`references/`），适用于 Claude Code、Codex、Cursor、Trae 等支持 Agent Skills 的工具。

## Skill 目录

| Skill | 一句话说明 | 讲解 |
| --- | --- | --- |
| [gongkao](#gongkao) | 公考面试结构化讲义全产品工具（6 个工作流） | [查看](#gongkao) |
| [leader](#leader) | 把一句话想法拆成 AI agent 能独立跑完的目标任务书 | [查看](#leader) |
| [human-writing](#human-writing) | 通用中文创作与改稿，去 AI 味儿 | [查看](#human-writing) |
| [ima-skill](#ima-skill) | 统一的 IMA 笔记与知识库操作技能 | [查看](#ima-skill) |
| [pe-lecture](#pe-lecture) | 教师编笔试"举一反三"讲稿生成与反例沉淀 | [查看](#pe-lecture) |
| [pe-trial](#pe-trial) | 体育试讲稿教学产物全流程生成 | [查看](#pe-trial) |
| [structured-post](#structured-post) | "结构化每日一练"帖子 docx 自动生成 | [查看](#structured-post) |
| [zhankai](#zhankai) | "展开说说"系列小红书长帖 docx 自动生成 | [查看](#zhankai) |

## 安装（通用方法）

### 方法一：让 Agent 帮你安装

对你的 Agent 说：

> 帮我安装这个 skill：`https://github.com/rshawn0307-maker/rshawn-skills/tree/main/skills/<skill 名>`

支持从 GitHub 安装 Skill 的工具会自动 clone 并注册。

### 方法二：手动复制目录

将 `skills/<skill 名>/` 整个目录复制到你的工具对应的 skills 目录：

- Claude Code：`~/.claude/skills/<skill 名>/`
- Codex：`~/.codex/skills/<skill 名>/`
- Cursor：`.cursor/skills/<skill 名>/`
- Trae：`~/.trae-cn/skills/<skill 名>/`
- 其他 runtime：参考对应工具的 skills 目录约定

### 方法三：不支持 Skill 的工具

复制 `SKILL.md` 的内容作为项目规则文件（如 `CLAUDE.md` / `AGENTS.md`）的参考，或直接粘贴给 Agent 作为系统提示词。

> 提示：少数 skill 依赖同仓库的兄弟 skill（例如 structured-post、zhankai 依赖 human-writing，ima-skill 供多个 skill 调用），建议一起安装到同一个 skills 根目录。

## Skill 详解

### gongkao

公考面试结构化讲义全产品工具。覆盖题目生成、方法论提炼、框架模板、过渡句库、素材库、讲义组装 6 个工作流，支持从单题生成到完整讲义产品的全生命周期。每道题含 frontmatter 元信息、题干、思路大纲和 800-1000 字逐字稿，并经 Python 多模式验证（字数 + AI 痕迹 + 用语禁忌 + 结构完整性）后写入对应目录。

触发词：面试题库、出面试题、公考面试题、批量出题、题库填充、面试逐字稿、生成方法论、生成框架、生成过渡句、生成素材、组装讲义、更新讲义、导出讲义。

### leader

把一句话的想法拆成 AI agent 能独立跑完的目标任务书。先进代码库实测、必要时联网调研，再一次性提问（≤5 个），产出一份 ≤4000 字符、直接粘进 /goal 就能跑的任务书，含实测数字、白名单地界、防作弊验收和断点续跑。

触发词：帮我给 agent 写个目标、详细拆一下这个目标、写个任务书/brief、写个 goal 提示词、把活分给几个 agent 并行。

### human-writing

通用中文创作与改稿 Skill。用于知乎回答、公众号文章、博客、评论、人物故事、历史叙事、教程、评测、小说、口播和演讲稿等，默认写成一个见过事、查过材料、愿意把来龙去脉讲清楚的人在说话，保留中文互联网长文的活人感和自然韵律。成稿正文严禁冒号、破折号、"不是……而是……"及同类翻案句，并清除商业黑话和模型惯用黑话。

### ima-skill

统一的 IMA OpenAPI 技能，支持笔记管理和知识库操作：搜索/浏览/创建/追加笔记，上传文件、添加网页到知识库、知识库内容搜索与原文获取。需要自行配置 IMA OpenAPI 凭证（`IMA_OPENAPI_CLIENTID` / `IMA_OPENAPI_APIKEY` 或 `~/.config/ima/`）。

触发词：知识库、笔记、备忘录、帮我记一下、上传文件到知识库、搜一下知识库里有没有 XX。

### pe-lecture

教师编体育笔试"举一反三"讲稿的成体系生成与反例沉淀。基于招教体育讲义库，按 8 节结构 + 引用/口诀/双链硬约束批量产出讲稿，并内置 R1-R18 实战反例、10 条学员稿红线自查与 docx 合并发布流程。

> 注意：本 skill 涉及大量业务工作区路径，文档中统一使用 `<项目根>`、`<用户目录>`、`<临时目录>`、`<Python 环境>` 占位符，使用前请替换为实际路径。

### pe-trial

生成体育试讲稿教学产物（教学设计/试讲稿/队形图/自检表），含初始化、子技术识别、并行生产、六维度横评、问题修复、备考讲义生成全流程，支持基于教材批量开发新运动项目。

> 注意：`generate_lecture.py` 顶部的 `BASE_DIR` / `OUTPUT_PATH` 使用 `<项目根>` 占位符，运行前请替换为实际路径。

### structured-post

自动化生成"结构化每日一练"小红书/公众号帖子 docx。基于固定 docx 模板 + python-docx 脚本，自动替换题目文本框、正文段落、分页符并保留配图/引流段样式，答题须经 human-writing 去 AI 味儿。

触发词：答一道、出题、做一篇结构化帖子、每日一练。

### zhankai

自动化生成"考官想听的·展开说说"系列小红书长帖 docx。站在公务员结构化面试考官视角剖析答题思路，按小红书节奏打磨（标题钩子/短句/emoji/互动钩子/话题标签），基于固定 docx 模板（48 段 + 1 表格）自动替换内容。

触发词：展开说说、做一篇考官想听的、出一期长帖、跑第 N 期。

## 许可

本仓库为个人作品，供学习交流使用。部分 skill 内容涉及具体业务场景与个人工作流，请按需修改后使用。
