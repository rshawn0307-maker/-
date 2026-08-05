# pe-lecture

> 教师编笔试"举一反三"讲稿成体系生成与反例沉淀。体育学科向。

> **路径占位符说明**：本文档及 references/ 中的 `<项目根>`、`<用户目录>`、`<临时目录>`、`<Python 环境>` 均为占位符（原为旧 Windows 机器上的 `C:\Users\keira\...` 路径），使用前请替换为当前机器的实际路径。

## 安装

### 从 rshawn-skills 合集安装（推荐）

本 skill 已并入 [rshawn-skills](https://github.com/rshawn0307-maker/rshawn-skills) 仓库：

```bash
git clone https://github.com/rshawn0307-maker/rshawn-skills.git
# 将 skills/pe-lecture/ 目录复制到你的 skills 目录即可
```

### 手动安装

1. 从 rshawn-skills 仓库下载 `skills/pe-lecture/` 文件夹
2. 放入你的 skills 目录：
   - Claude Code: `~/.claude/skills/pe-lecture/`
   - Cursor: `~/.cursor/skills/pe-lecture/`
   - Codex: `~/.codex/skills/pe-lecture/`
   - 其他 runtime: 参考对应 runtime 的 skills 目录
3. 确保 `SKILL.md` 在文件夹根目录

## 依赖

- Python 3.8+（带 python-docx + python-pptx + openpyxl）
- 真实的讲义 docx 文件（≥350 行大讲义）

## 结构

```
pe-lecture/
├── SKILL.md                          <- 主流程（含 R1-R18 反例 + 批量产出 SOP）
├── references/                       <- 10 个配套 .md
│   ├── PPT抽取+workbuddy_venv实战_v1.md
│   ├── PPT无讲义处理_v1.md
│   ├── R11-R14反例与运动技术4篇拆点SOP_v1.7.md
│   ├── 下册docx同步工作流_v1.md
│   ├── 其他家AI稿接手_SOP.md
│   ├── 大讲义抽章节_SOP.md
│   ├── 老板参考版版式_v1.md
│   ├── 老板项目真路径_v1.md
│   ├── 输出格式样板_v1.md
│   └── 运动技术全套生成实战_v1.md
└── scripts/
    ├── merge_md_to_docx_v1.py        <- N 篇 md -> 单 docx 合并脚本
    └── r1_self_check.py              <- R1-R6 反例自查脚本
```

## 触发词

当用户说"按举一反三模板生成讲稿"且涉及体育学科时触发。

## 版本

v3.5 (2026-06-30) - Darwin Skill 2.0 优化后版本，质量评分 89.3/100
