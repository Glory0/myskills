---
name: split-spec-notes
description: Split specification study markdown notes into the user's "规范精读" four-level hierarchy (spec, chapter, section, article), auto-generate Feynman-style learning notes for each article, and read embedded images / wikilinks to enrich the explanations. Use when the user says "拆分笔记", "拆分规范笔记", "拆分成规范精读笔记", "把这几个笔记拆分一下", or any request to decompose a merged spec learning note into structured spec-study notes with Feynman explanations.
---

# Split Spec Notes

Split a single merged specification study note into the user's "规范精读" four-level note hierarchy, automatically generate `## 费曼` sections for every article note, and leverage embedded images and wikilinks to produce richer, more accurate explanations.

## Quick Triggers

The user can invoke this skill with short phrases like:
- "拆分笔记"
- "帮我把这几个笔记拆分一下"
- "把这个规范笔记拆成规范精读格式"
- "拆分规范笔记"
- "拆分成规范精读笔记"
- "按条拆分成条笔记"

## Three-Step Workflow

### Step 1: Split with script
Run the bundled script with the source path and template directory:

```bash
python scripts/split_spec.py \
  --source "D:\job\201-规范\钢储罐地规【2008】3.1 学习.md" \
  --template-dir "D:\job\999-模板\规范精读模板"
```

This generates:

| Type | File name | Template used |
|:---|:---|:---|
| Spec | `钢储罐地规【2008】.md` | 规范精读-规范.md |
| Chapter | `钢储罐地规【2008】3.md` | 规范精读-章.md |
| Section | `钢储罐地规【2008】3.1.md` | 规范精读-节.md |
| Articles | `钢储罐地规【2008】3.1.1.md` ~ `3.1.9.md` | 规范精读-条.md |

### Step 2: Read embedded images and wikilinks (MANDATORY)
Before writing the `## 费曼` sections, you MUST inspect the source note and the newly-generated article notes for:

1. **Image references** (`![[Pasted image ...]]` or `![[...]]`)
   - Try `D:\job\900-附件\<filename>` first.
   - If not found, search recursively under `D:\job\`.
   - Use `ReadMediaFile` to view the image, extract tables / charts / diagrams, and summarize the visual data in plain text inside the relevant `## 费曼` or `## ` body.

2. **Wikilinks** (`[[note name]]` or `[[note name|alias]]`)
   - Resolve the link to an actual `.md` file under `D:\job\`.
   - Read the linked note with `ReadFile` if it helps explain the current article.
   - Reference the linked content in `### 条文关联` or `### 大白话解释` when relevant.

### Step 3: Auto-generate Feynman sections (MANDATORY)
**You MUST read each newly-generated article note and replace the empty `## 费曼` placeholder with a complete Feynman section.** Do NOT skip this step even if the user only said "拆分笔记".

For each article, the `## 费曼` block must contain exactly these sub-sections:

1. **### 一句话总结** — One-sentence plain-Chinese summary of the core rule.
2. **### 大白话解释** — 2-4 bullet points breaking down the logic, key numbers, limits, and consequences. If the article contains tables or charts from Step 2, describe the key numeric patterns here.
3. **### 条文关联** — Explicit links to related articles in the same section. **All referenced article numbers MUST be written as Obsidian wikilinks** using the alias syntax: `[[钢储罐地规【2008】3.1.5|3.1.5]]`. This enables direct navigation between article notes. Also reference any linked notes discovered in Step 2.
4. **### 类比** — A quotable everyday-life analogy.
5. **### 记忆口诀** — A short, rhyming or rhythmic mnemonic in a blockquote.

Append the filled `## 费曼` content just before `## 同节规范`. Preserve everything else in the note.

## Expected Source File Format

The source markdown file must follow this exact structure:

- **Line 1**: Full specification name (e.g. `钢制储罐地基基础设计规范 GB 50473-2008`)
- **Level-1 heading**: Chapter (e.g. `# 3 基本规定`)
- **Level-2 heading**: Section (e.g. `## 3.1 一般规定`)
- **Level-3 heading**: Article number only (e.g. `### 3.1.1`)
- **Article body**: Paragraphs under the article heading
- **Level-4 heading**: Optional article explanation (e.g. `#### 条文说明`)

Source file name format: `规范简写【年份】节号 学习.md` (e.g. `钢储罐地规【2008】3.1 学习.md`)

## Behavior

- **Frontmatter**: Fill `规范名称`, `规范章名称`, `规范节名称`, `简述` automatically.
- `规范章名称` is filled as `{章号} {章名}` (e.g. `3 基本规定`).
- `规范节名称` is filled as `{节号} {节名}` (e.g. `3.1 一般规定`).
- `简述` must be a **concise summary of the entire article** (not just a copy of the first sentence). It should capture the core rule in 15–30 Chinese characters. Kimi should manually craft it based on the full article body after the script runs.
- `aliases` should be populated with relevant keywords derived from the `简述`, separated by commas. These aliases help with Obsidian linking and search discovery.
- **Skip existing**: If any target file already exists, it is skipped and not overwritten.
- **Article body**: Inserted into the blank `## ` heading area in the article template. The script uses a regex `^## \n` to locate the exact empty H2, avoiding false matches inside `#### 条文说明`. Image references and wikilinks in the original body are preserved.
- **简述 auto-extraction**: The script extracts the first sentence ending with `。`、`：` or `；` (up to 80 chars). If the extracted text is too generic, Kimi should manually rewrite it into a concise 15–30 character summary.
- **Corrections**: If the source line-1 spec number is wrong (e.g. GB 50073 instead of GB 50473), correct it in the generated files.
- **Feynman generation**: The article template already contains an empty `## 费曼` skeleton. You must populate it for every newly-created article note.
- **Image enrichment**: When tables or diagrams appear in images, transcribe the critical data into the `## 费曼`大白话解释 so the knowledge is text-searchable.

## Obsidian Markdown Formatting Rules (MANDATORY)

All generated content must be compatible with Obsidian's Markdown parser. Follow these rules strictly:

### Tables
- **A blank line is REQUIRED immediately before every table.** Without it, Obsidian Live Preview will not render the table and will display it as plain text.
- A blank line after the table is also recommended for consistency.
- Every table must have a separator row (`|---|---|`) immediately after the header row.
- Inside table cells, if you use wikilinks with aliases (`[[note|alias]]`), you MUST escape the pipe: `[[note\|alias]]`.

### Paragraphs and Headings
- Separate paragraphs with a blank line. Do not rely on single line breaks.
- Leave a blank line before and after headings when possible.
- Do not mix heading levels inconsistently within the same block.

### Lists
- Use consistent indentation for nested list items.
- Do not place a table directly after a list item without a blank line in between.

### Blockquotes
- Start each blockquote line with `>`.
- If a blockquote contains multiple paragraphs, use `>` on the blank line between them as well.

### Verification
Before finishing, scan the generated note for any table that is immediately preceded by text or a heading without a blank line. If found, insert a blank line.

## Post-run Checks

1. Confirm that the script output shows the expected number of CREATE/SKIP lines.
2. Read a sample article note to verify the `## 费曼` block is fully populated and any images/wikilinks were leveraged.
3. Verify that the generated Markdown is valid under Obsidian rules (especially tables have a blank line before them).
4. Verify that the Obsidian `base` views in the chapter/section/spec notes correctly list the children.
