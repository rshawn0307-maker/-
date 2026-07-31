#!/usr/bin/env python3
"""
公考面试题验证脚本：字数统计 + AI痕迹/用语禁忌扫描

用法：
  python validate_question.py <md文件路径> [md文件路径...]
  python validate_question.py 综合分析_01_指尖形式主义.md
  python validate_question.py 综合分析_*.md   (批量)

输出：
  每个文件的字数、AI痕迹命中、用语禁忌命中、破折号使用、三段式检测
  最终汇总：全部通过 / 存在需修正的文件
"""

import sys
import re
import os
import glob

# ============================================================
# AI痕迹关键词（6类）—— 对应 SKILL.md 的 humanizer-zh 集成清单
# ============================================================
AI_PATTERNS = {
    "AI标志性短语": [
        "标志着", "彰显了", "体现了", "不断演变", "至关重要", "不可或缺",
        "深远影响", "深刻变革", "不可磨灭", "深深植根", "关键转折点",
        "为…奠定基础", "为…做出贡献",
    ],
    "AI连接词/填充短语": [
        "此外", "然而", "值得注意的是", "综上所述", "总而言之",
        "更重要的是", "深入探讨", "为了实现这一目标",
        "在这个时间点",
    ],
    "模糊归因": [
        "专家认为", "业内人士表示", "观察者指出",
        "一些批评者认为", "行业报告显示",
    ],
    "否定式排比": [
        "不仅…而且", "这不仅仅是", "不仅…更是",
    ],
    "万能收束": [
        "总之", "综上", "总而言之", "未来可期", "任重道远",
        "前景光明", "追求卓越",
    ],
    "公考高危词": [
        "深入推进", "全面落实", "持续优化", "多措并举",
        "综合施策", "协同推进", "切实保障", "有效提升",
        "有力推动",
    ],
}

# ============================================================
# 用语禁忌关键词（4类）—— 对应 SKILL.md 的公考面试用语禁忌
# ============================================================
FORBIDDEN_WORDS = {
    "贬义比喻词": [
        "落水狗", "狼狈", "龟孙", "痛打", "狼狈为奸",
    ],
    "网络流行词": [
        "韭菜", "小白", "键盘侠", "内卷", "摆烂", "躺平",
        "yyds", "绝绝子",
    ],
    "情绪化表达": [
        "气死", "笑死", "巨坑", "血亏", "无语", "离谱",
    ],
    "政治风险词": [
        "上面不作为", "领导拍脑袋",
    ],
}

# ============================================================
# 字数统计
# ============================================================

def extract_answer_text(content):
    """提取'## 答题逐字稿'之后到末尾'---'之前的内容"""
    match = re.search(r'##\s*答题逐字稿\s*\n(.*?)(?:\n---\s*\n|\n---\s*$|\Z)', content, re.DOTALL)
    if not match:
        # 尝试匹配到文件末尾
        match = re.search(r'##\s*答题逐字稿\s*\n(.*)', content, re.DOTALL)
    if not match:
        return None
    text = match.group(1)
    # 去掉 markdown 标记行（以 # 开头的行）
    lines = []
    for line in text.split('\n'):
        stripped = line.strip()
        if stripped.startswith('#'):
            continue
        if stripped.startswith('---'):
            continue
        lines.append(line)
    text = '\n'.join(lines)
    return text


def count_chars(text):
    """统计字符数（含中文标点，不含空格和换行）"""
    text = text.replace(' ', '').replace('\n', '').replace('\r', '').replace('\t', '')
    return len(text)


# ============================================================
# AI痕迹扫描
# ============================================================

def scan_ai_patterns(text):
    """扫描AI痕迹，返回 {类别: [命中词, ...]}"""
    hits = {}
    for category, patterns in AI_PATTERNS.items():
        matched = []
        for p in patterns:
            # 处理含省略号的模式（如 "不仅…而且"）
            if '…' in p:
                parts = p.split('…')
                # 构建正则：part0 + 任意字符 + part1
                regex = re.escape(parts[0]) + '.*' + re.escape(parts[1])
                if re.search(regex, text):
                    matched.append(p)
            elif p in text:
                matched.append(p)
        if matched:
            hits[category] = matched
    return hits


# ============================================================
# 破折号统计
# ============================================================

def count_dashes(text):
    """统计破折号使用情况，返回使用超过1个的段落列表 [(段号, 数量)]"""
    paragraphs = [p for p in text.split('\n') if p.strip()]
    overuse = []
    for i, para in enumerate(paragraphs):
        count = para.count('——')
        if count > 1:
            overuse.append((i + 1, count))
    return overuse


# ============================================================
# 用语禁忌扫描
# ============================================================

def scan_forbidden_words(text):
    """扫描用语禁忌词，返回 {类别: [命中词, ...]}"""
    hits = {}
    for category, words in FORBIDDEN_WORDS.items():
        matched = [w for w in words if w in text]
        if matched:
            hits[category] = matched
    return hits


# ============================================================
# 三段式检测
# ============================================================

def detect_three_part_pattern(text):
    """检测机械三段式（第一/第二/第三 在相近位置连续出现）"""
    # 检测 "第一，...第二，...第三，" 模式
    pattern = r'第一[，,].{0,200}第二[，,].{0,200}第三[，,]'
    if re.search(pattern, text, re.DOTALL):
        return True
    return False


# ============================================================
# 主流程
# ============================================================

def validate_file(filepath):
    """验证单个md文件，返回结果字典"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {"error": f"读取失败 {filepath}: {e}"}

    text = extract_answer_text(content)
    if not text or not text.strip():
        return {"error": f"未找到'## 答题逐字稿'部分: {filepath}"}

    char_count = count_chars(text)
    ai_hits = scan_ai_patterns(text)
    forbidden_hits = scan_forbidden_words(text)
    dash_info = count_dashes(text)
    three_part = detect_three_part_pattern(text)

    all_clear = (
        800 <= char_count <= 930
        and not ai_hits
        and not forbidden_hits
        and not dash_info
        and not three_part
    )

    return {
        "file": os.path.basename(filepath),
        "char_count": char_count,
        "char_ok": 800 <= char_count <= 930,
        "ai_hits": ai_hits,
        "forbidden_hits": forbidden_hits,
        "dash_overuse": dash_info,
        "three_part_pattern": three_part,
        "all_clear": all_clear,
    }


def print_report(result):
    """打印单个文件的验证报告"""
    print(f"\n{'=' * 60}")

    if "error" in result:
        print(f"❌ {result['error']}")
        return False

    print(f"📄 {result['file']}")
    print(f"{'=' * 60}")

    # 字数
    status = "✅" if result['char_ok'] else "❌"
    print(f"{status} 字数: {result['char_count']} (目标 800-930)")

    # AI痕迹
    if result['ai_hits']:
        print(f"❌ AI痕迹命中:")
        for cat, words in result['ai_hits'].items():
            print(f"   {cat}: {', '.join(words)}")
    else:
        print(f"✅ AI痕迹: 零命中")

    # 用语禁忌
    if result['forbidden_hits']:
        print(f"❌ 用语禁忌命中:")
        for cat, words in result['forbidden_hits'].items():
            print(f"   {cat}: {', '.join(words)}")
    else:
        print(f"✅ 用语禁忌: 零命中")

    # 破折号
    if result['dash_overuse']:
        print(f"⚠️  破折号过度使用:")
        for para_num, count in result['dash_overuse']:
            print(f"   第{para_num}段: {count}个破折号 (建议≤1)")
    else:
        print(f"✅ 破折号: 正常")

    # 三段式
    if result['three_part_pattern']:
        print(f"⚠️  检测到机械三段式 (第一/第二/第三 连续)")
    else:
        print(f"✅ 三段式: 未检测到")

    # 总结
    if result['all_clear']:
        print(f"\n✅ 全部通过")
    else:
        print(f"\n❌ 存在问题，需修正")

    return result['all_clear']


def expand_wildcards(args):
    """展开通配符参数（Windows cmd 不自动展开 *.md）"""
    files = []
    for arg in args:
        if '*' in arg or '?' in arg:
            matched = sorted(glob.glob(arg))
            if matched:
                files.extend(matched)
            else:
                files.append(arg)  # 保留原样，后面会报文件不存在
        else:
            files.append(arg)
    return files


def main():
    if len(sys.argv) < 2:
        print("公考面试题验证脚本")
        print("用法: python validate_question.py <md文件路径> [md文件路径...]")
        print("示例: python validate_question.py 综合分析_01_指尖形式主义.md")
        print("      python validate_question.py *.md  (批量)")
        print("")
        print("检查项: 字数(800-930) / AI痕迹(6类) / 用语禁忌(4类) / 破折号 / 三段式")
        sys.exit(1)

    files = expand_wildcards(sys.argv[1:])
    all_clear = True
    total = 0
    passed = 0

    for filepath in files:
        if not os.path.exists(filepath):
            print(f"\n❌ 文件不存在: {filepath}")
            all_clear = False
            continue

        total += 1
        result = validate_file(filepath)
        ok = print_report(result)
        if ok:
            passed += 1
        else:
            all_clear = False

    print(f"\n{'=' * 60}")
    print(f"汇总: {passed}/{total} 文件通过验证")
    if all_clear and total > 0:
        print(f"🎉 全部通过！")
    elif total == 0:
        print(f"⚠️  没有找到可验证的文件")
    else:
        print(f"⚠️  存在需修正的文件，请按报告修改后重跑。")
    print(f"{'=' * 60}")

    # 退出码：0=全部通过，1=存在问题
    sys.exit(0 if (all_clear and total > 0) else 1)


if __name__ == "__main__":
    main()
