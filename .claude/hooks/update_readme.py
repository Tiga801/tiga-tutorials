#!/usr/bin/env python3
"""
自动扫描 tutorials/ 和 blog-summaries/ 目录，
更新 README.md 中的 AUTO-INDEX 区块。
"""

import os
import re
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
README_PATH = os.path.join(BASE_DIR, "README.md")

SECTIONS = [
    ("tutorials", "tutorials"),
    ("blog-summaries", "blog-summaries"),
]


def extract_info(filepath):
    """从 Markdown 文件中提取标题和第一段描述。"""
    title = os.path.splitext(os.path.basename(filepath))[0]
    description = ""

    try:
        with open(filepath, encoding="utf-8") as f:
            lines = f.readlines()

        # 提取一级标题
        for line in lines:
            if line.startswith("# "):
                title = line[2:].strip()
                break

        # 提取第一段描述（跳过标题、空行、分隔线）
        in_paragraph = False
        para_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("#") or stripped.startswith("---") or stripped.startswith("==="):
                if in_paragraph:
                    break
                continue
            if stripped == "":
                if in_paragraph:
                    break
                continue
            in_paragraph = True
            para_lines.append(stripped)

        description = " ".join(para_lines)
        if len(description) > 100:
            description = description[:97] + "..."

    except Exception:
        pass

    return title, description


def get_mtime(filepath):
    """返回文件最后修改时间，格式 YYYY-MM-DD。"""
    ts = os.path.getmtime(filepath)
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d")


def build_table(section_dir, rel_dir):
    """扫描目录，生成 Markdown 表格字符串。"""
    md_files = sorted(
        f for f in os.listdir(section_dir) if f.endswith(".md")
    )

    if not md_files:
        return "> 暂无文件"

    rows = ["| 文件 | 标题 | 最后修改 | 描述 |",
            "| ---- | ---- | -------- | ---- |"]

    for filename in md_files:
        filepath = os.path.join(section_dir, filename)
        title, description = extract_info(filepath)
        mtime = get_mtime(filepath)
        rel_path = f"{rel_dir}/{filename}"
        rows.append(f"| [{filename}]({rel_path}) | {title} | {mtime} | {description} |")

    return "\n".join(rows)


def update_readme():
    with open(README_PATH, encoding="utf-8") as f:
        content = f.read()

    for rel_dir, marker in SECTIONS:
        section_dir = os.path.join(BASE_DIR, rel_dir)
        if not os.path.isdir(section_dir):
            continue

        table = build_table(section_dir, rel_dir)

        pattern = (
            rf"(<!-- AUTO-INDEX:{re.escape(marker)}:START -->)"
            rf".*?"
            rf"(<!-- AUTO-INDEX:{re.escape(marker)}:END -->)"
        )
        replacement = rf"\1\n{table}\n\2"
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("README.md 索引已更新")


if __name__ == "__main__":
    update_readme()
