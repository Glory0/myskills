import os
import argparse
from datetime import datetime


def save_memory(topic, content, output_dir, related_memories=None, preload_files=None):
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{topic}-会话-{date_str}.md"
    filepath = os.path.join(output_dir, filename)

    related_yaml = "\n"
    if related_memories:
        for path in related_memories:
            related_yaml += f"  - \"{path}\"\n"
    else:
        related_yaml = "\n"

    preload_yaml = "\n"
    if preload_files:
        for path in preload_files:
            preload_yaml += f"  - \"{path}\"\n"
    else:
        preload_yaml = "\n"

    if os.path.exists(filepath):
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(f"\n\n---\n\n")
            f.write(content)
        print(f"APPEND: {filename}")
    else:
        frontmatter = f"""---
日期: {date_str}
tags:
  - kimi-记忆
主题: {topic}
关联记忆:{related_yaml}预读文件:{preload_yaml}---

"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(frontmatter)
            f.write(content)
        print(f"CREATE: {filename}")

    return filepath


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='保存 Kimi 会话记忆到 Obsidian 笔记')
    parser.add_argument('--topic', required=True, help='中文主题名称')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--content', help='记忆内容（Markdown 格式，直接传入）')
    group.add_argument('--content-file', help='记忆内容文件路径（避免命令行转义问题）')
    parser.add_argument('--output-dir', default=r'D:\job\400-软件\480-kimicode\记忆', help='输出目录')
    parser.add_argument('--related-memories', nargs='*', default=None, help='关联记忆文件路径列表')
    parser.add_argument('--preload-files', nargs='*', default=None, help='预读文件路径列表')
    args = parser.parse_args()

    if args.content_file:
        with open(args.content_file, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = args.content

    path = save_memory(args.topic, content, args.output_dir, args.related_memories, args.preload_files)
    print(f"SAVED: {path}")
