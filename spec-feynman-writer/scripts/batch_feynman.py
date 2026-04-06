"""
batch_feynman.py - 批量为规范条笔记生成费曼内容和优化 frontmatter

用法：
  1. 复制本脚本到工作目录并重命名（如 batch_feynman_xxx.py）
  2. 编辑下方的 updates 字典
  3. 运行：python batch_feynman_xxx.py
"""

import os
import re

# ==================== 在此编辑每条笔记的更新内容 ====================
updates = {
    # 格式：'X.X.X': {
    #     '简述': '15-30字的精简总结',
    #     'aliases': '关键词1, 关键词2, 关键词3',
    #     '费曼': """## 费曼
    #
    # ### 一句话总结
    # **...**
    #
    # ### 大白话解释
    # ...
    #
    # ### 条文关联
    # - [[规范名【年份】X.X.X|X.X.X]] ...
    #
    # ### 类比
    # > ...
    #
    # ### 记忆口诀
    # > ...
    # """
    # },
    #
    # 示例：
    '3.1.1': {
        '简述': '示例：储罐基础设计前应收集完整的地质和工艺资料。',
        'aliases': '示例, 资料收集, 地质勘察, 工艺资料',
        '费曼': """## 费曼

### 一句话总结
**示例：设计储罐基础前，必须把地质情况和工艺要求摸清楚。**

### 大白话解释
储罐又大又重，基础设计不能拍脑袋。必须先拿到：
1. **地质资料**：土层分布、承载力、地下水位等
2. **工艺资料**：储罐容积、直径、介质密度、操作温度等
只有资料齐全，才能算出准确的基础尺寸和沉降。

### 条文关联
- 与 [[钢储罐地规【2008】3.1.2|3.1.2]] 呼应：3.1.1 是"收集资料"，3.1.2 是"资料怎么用"。

### 类比
> 就像裁缝做衣服，必须先量好尺寸，不能凭眼睛估算。

### 记忆口诀
> **设计先收料，尺寸才能对。**
"""
    },
}
# =====================================================================

base_dir = r'D:\job\201-规范'  # 根据实际路径修改

for 条号, info in updates.items():
    文件名 = f'钢储罐地规【2008】{条号}.md'
    路径 = os.path.join(base_dir, 文件名)

    if not os.path.exists(路径):
        print(f'文件不存在，跳过: {文件名}')
        continue

    with open(路径, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. 更新 frontmatter（兼容简述原本为空或有内容的情况）
    content = re.sub(
        r'^(简述:).*$',
        f'简述: {info["简述"]}',
        content,
        flags=re.MULTILINE
    )
    content = re.sub(
        r'^(aliases:).*$',
        f'aliases: {info["aliases"]}',
        content,
        flags=re.MULTILINE
    )

    # 2. 修复空的 ## 标题
    # 精确匹配 "## \n"，避免误匹配 "#### 条文说明" 中的 "## "
    idx_extend = content.find('## 扩展')
    if idx_extend != -1:
        match = re.search(r'^## \n', content[:idx_extend], re.MULTILINE)
        if match:
            content = content[:match.start() + 3] + info['简述'] + '\n' + content[match.end():]

    # 3. 替换费曼内容（从 "## 费曼" 到 "## 同节规范" 之间的占位内容）
    idx_feynman = content.find('## 费曼')
    idx_tongjie = content.find('## 同节规范')
    if idx_feynman != -1 and idx_tongjie != -1:
        content = content[:idx_feynman] + info['费曼'] + '\n\n' + content[idx_tongjie:]

    with open(路径, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'已更新: {文件名}')

print('\n全部处理完成。建议执行校验：')
print('  1. 检查 frontmatter 中的简述和 aliases 是否正确')
print('  2. 检查 ## 标题是否已填充')
print('  3. 检查 #### 条文说明 是否未被误替换')
print('  4. 检查费曼 5 个小节是否齐全')
print('  5. 检查表格前是否有空行')
