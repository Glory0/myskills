import os
import re
import argparse


def split_spec_note(source_path, template_dir, output_dir=None):
    if output_dir is None:
        output_dir = os.path.dirname(source_path)

    filename = os.path.basename(source_path)
    m = re.match(r'^(.*?)【(\d{4})】([\d.]+) 学习\.md$', filename)
    if not m:
        raise ValueError(f"文件名格式不匹配，期望格式：规范简写【年份】节号 学习.md，实际：{filename}")

    规范简写, 年份, _ = m.group(1), m.group(2), m.group(3)

    with open(source_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    规范名称 = lines[0].strip()
    content = ''.join(lines[1:])

    templates = {}
    for tname in ['规范精读-规范.md', '规范精读-章.md', '规范精读-节.md', '规范精读-条.md']:
        tpath = os.path.join(template_dir, tname)
        with open(tpath, 'r', encoding='utf-8') as f:
            templates[tname] = f.read()

    章匹配 = re.search(r'^#\s+(\d+)\s+(.+)$', content, re.MULTILINE)
    节匹配 = re.search(r'^##\s+(\d+\.\d+)\s+(.+)$', content, re.MULTILINE)

    if not 章匹配 or not 节匹配:
        raise ValueError("未能从文件中解析出章或节标题。请确保文件包含类似 '# 3 基本规定' 和 '## 3.1 一般规定' 的标题。")

    章号, 章名 = 章匹配.group(1), 章匹配.group(2)
    节号, 节名 = 节匹配.group(1), 节匹配.group(2)

    条_pattern = r'^###\s+(\d+\.\d+\.\d+)\s*\n(.*?)(?=^###\s+\d+\.\d+\.\d+|\Z)'
    条_matches = re.findall(条_pattern, content, re.MULTILINE | re.DOTALL)

    if not 条_matches:
        raise ValueError("未能在节内容下找到任何条标题（### 3.1.x）。")

    def write_if_not_exists(path, content):
        if os.path.exists(path):
            print(f'SKIP: {os.path.basename(path)}')
        else:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'CREATE: {os.path.basename(path)}')

    # 规范
    规范文件 = os.path.join(output_dir, f'{规范简写}【{年份}】.md')
    规范内容 = templates['规范精读-规范.md'].replace('规范名称: ', f'规范名称: {规范名称}')
    write_if_not_exists(规范文件, 规范内容)

    # 章
    章文件 = os.path.join(output_dir, f'{规范简写}【{年份}】{章号}.md')
    章内容 = templates['规范精读-章.md'].replace('规范名称: ', f'规范名称: {规范名称}').replace('规范章名称: n', f'规范章名称: {章号} {章名}')
    write_if_not_exists(章文件, 章内容)

    # 节
    节文件 = os.path.join(output_dir, f'{规范简写}【{年份}】{节号}.md')
    节内容 = templates['规范精读-节.md'].replace('规范名称: ', f'规范名称: {规范名称}').replace('规范章名称: n', f'规范章名称: {章号} {章名}').replace('规范节名称: n.n', f'规范节名称: {节号} {节名}')
    write_if_not_exists(节文件, 节内容)

    # 条
    for 条号, 条正文 in 条_matches:
        条文件 = os.path.join(output_dir, f'{规范简写}【{年份}】{条号}.md')
        条正文_clean = 条正文.strip()

        # 自动生成简述：取第一条正文的第一句（到第一个句号、冒号或分号），限制长度
        简述 = ''
        first_sentence_match = re.search(r'^([^。：；]{3,80}[。：；])', 条正文_clean.replace('\n', ' '))
        if first_sentence_match:
            简述 = first_sentence_match.group(1).strip()

        条内容 = templates['规范精读-条.md'].replace('规范名称: ', f'规范名称: {规范名称}')
        条内容 = 条内容.replace('规范节名称: n.n', f'规范节名称: {节号} {节名}')
        条内容 = 条内容.replace('简述: ', f'简述: {简述}')

        # 在 "## " 和 "## 扩展" 之间插入条文正文，标题处填入简述
        idx = 条内容.find('## 扩展')
        if idx != -1:
            # 精确匹配空 H2 标题 "## \n"，避免误匹配 "#### 条文说明" 中的 "## "
            match = re.search(r'^## \n', 条内容[:idx], re.MULTILINE)
            if match:
                条内容 = 条内容[:match.start() + 3] + 简述 + '\n' + 条正文_clean + '\n\n' + 条内容[idx:]

        write_if_not_exists(条文件, 条内容)

    print('\n拆分完成。')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='拆分规范学习笔记为四级规范精读笔记')
    parser.add_argument('--source', required=True, help='源笔记文件路径')
    parser.add_argument('--template-dir', required=True, help='四个模板文件所在的目录')
    parser.add_argument('--output-dir', default=None, help='输出目录（默认与源文件同目录）')
    args = parser.parse_args()
    split_spec_note(args.source, args.template_dir, args.output_dir)
