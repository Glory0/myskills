---
name: spec-screenshot-to-md
description: Convert screenshots of engineering design specifications and standard articles into Obsidian-compatible Markdown, preserving hierarchical structure, formulas, and tables. Use when the user provides specification screenshots and says "转成笔记", "转换为 Markdown", "规范截图转笔记", "把截图转成规范笔记", or any request to transcribe spec screenshots into structured Markdown.
---

# Spec Screenshot to Markdown

Convert screenshots of engineering design specifications into clean, Obsidian-compatible Markdown. Preserve the exact hierarchy (chapter → section → article → explanation), convert formulas to standard LaTeX, and transcribe tables with full data integrity.

## Quick Triggers

The user can invoke this skill with phrases like:
- "规范截图转笔记"
- "把这几张截图转成 Markdown"
- "转换为规范笔记格式"
- "转成 Obsidian 笔记"
- "提取截图里的规范条文"

## Core Workflow

When the user uploads one or more specification screenshots, execute the following steps in order.

### Step 1: Extract valid content only
Focus strictly on the **central white content area** of the screenshot. Ignore and exclude:
- Top navigation bars, headers, or breadcrumbs
- Bottom advertisements, copyright notices, or pagination
- Sidebars, toolbars, or UI panels
- Button text such as "添加对比", "上一节", "下一节", "收起", "展开"

### Step 2: Structural transcription
Identify and transcribe the hierarchical structure exactly as it appears:
- **章 (Chapter)** → `# 章号 名称`
- **节 (Section)** → `## 节号 名称`
- **条 (Article)** → `### 条号` or `### 条号 条文标题`
- **款/项 (Sub-items)** → Markdown list items preserving original numbering (`1.`, `2)`, `（1）`, `①`)
- **条文说明** → `#### 条文说明`

### Step 3: Element conversion
Convert embedded elements using the rules below:
- **Formulas** → LaTeX (`$inline$` or `$$block$$`)
- **Tables** → Standard Markdown tables
- **Images/diagrams** → If a diagram contains critical data (e.g., dimensions, parameters), transcribe the data into a Markdown table or descriptive list; retain the figure caption (e.g., **图3.2.3-1**)

### Step 4: Mandatory internal review (MANDATORY)
Before producing any output, you MUST silently perform the full five-phase review checklist described in the **Mandatory Internal Review** section. If any check fails, correct the draft and re-check.

### Step 5: Deliver clean output
Return ONLY the final Markdown wrapped in a ````markdown` fenced code block. Do NOT add introductory text (e.g., "以下是转换结果"). Do NOT add concluding explanations.

## Output Format Standard

### Heading hierarchy (strict)

| Spec level | Markdown | Example |
|---|---|---|
| 章 | `#` | `# 3 基本规定` |
| 节 | `##` | `## 3.1 一般规定` |
| 条 | `###` | `### 3.1.1` or `### 3.1.1 条文标题` |
| 款/项 | List items | `1.`, `2)`, `（1）` |
| 条文说明 | `####` | `#### 条文说明` |

### Article-explanation rule
- The original text "条文说明" or "收起条文说明" must be rewritten as `#### 条文说明`.
- The explanation content follows immediately as normal paragraphs. **Do NOT** use blockquotes `>` for it.
- If the explanation contains multiple paragraphs, keep them separated by blank lines.
- **Completeness check**: the entire explanation must be included without truncation.

### Formula rules
- **Syntax**: standard LaTeX math mode (`$...$` for inline, `$$...$$` for display if needed).
- **Symbols**: you MUST use raw mathematical symbols.
  - ✅ Correct: `>`, `<`, `≥`, `≤`, `≠`, `≈`
  - ❌ Forbidden: `&gt;`, `&lt;`, `&ge;`, `&le;` (HTML entities are strictly prohibited)
- **Sub/superscripts**: `_` for subscript, `^` for superscript.
- **Greek letters**: `\alpha`, `\beta`, `\omega`, `\Delta`, etc.
- **Units**: use upright text when typeset in LaTeX: `\mathrm{MPa}`, `\mathrm{m}`.
- **Formula numbers** (if present in the image) must be preserved.

### Table rules
- Convert to standard Markdown tables with a separator row immediately after the header.
- Place the table caption as bold text **above** the table: `**表3.1.4-1 每台储罐地基勘探点数量**`
- Leave a **blank line** before the caption/table and a blank line after the table.
- Alignment: numeric columns should generally be center- or right-aligned using `|:---:` or `|---:|`.
- **Merged cells**: if a table contains merged cells that cannot be expressed in pure Markdown, use inline HTML table syntax to preserve structure.
- **Footnotes** under the table must be included as normal text directly below the table.

### List and numbering rules
- Preserve original numbering styles exactly (`1.`, `2)`, `（1）`, `①`).
- Maintain correct indentation for nested levels (2–4 spaces).
- Do NOT renumber items; use the original sequence.

## Behavior

### Content integrity (highest priority)
- **No omission**: every sentence, clause, table, formula, figure caption, footnote, and article explanation must appear in the output.
- **No rewriting**: keep original wording and technical terminology unchanged.
- **No reordering**: maintain the original sequence of paragraphs, items, and sections.
- **After transcription**, mentally compare the screenshot line-by-line with your draft to confirm nothing is missing.

### Screenshot quality handling
- If text is blurry, mark uncertain characters with `(?)` or note the ambiguity.
- If content spans multiple screenshots, keep it continuous and do NOT repeat headers unnecessarily.

### Exclusion verification
Before finalizing, confirm these UI elements have NOT leaked into the output:
- [ ] Top navigation / breadcrumbs
- [ ] Bottom ads / copyright
- [ ] Sidebar content
- [ ] Button labels ("添加对比", "上一节", "下一节", "收起")
- [ ] Page headers/footers (except true body text)

## Mandatory Internal Review

You MUST perform this checklist internally for every output. Do NOT print the checklist to the user.

### Phase 1 — Hierarchy check
- [ ] All chapters (`#`) extracted
- [ ] All sections (`##`) extracted
- [ ] All articles (`###`) extracted
- [ ] Article numbers are continuous with no gaps
- [ ] No content is cut off at the bottom of the screenshot

### Phase 2 — Article-explanation check (critical)
- [ ] Every blue-background or collapsible "条文说明" is extracted
- [ ] The explanation is complete, not truncated
- [ ] All paragraphs inside the explanation are present
- [ ] Any formulas, tables, or data inside the explanation are intact

### Phase 3 — Table check
- [ ] Every table in the screenshot is transcribed
- [ ] Caption (table number + name) is present and bolded above the table
- [ ] All rows and columns are present, no missing cells
- [ ] Table footnotes / notes are included
- [ ] Merged cells handled correctly

### Phase 4 — Formula check
- [ ] Every formula is transcribed
- [ ] Subscripts and superscripts are correct
- [ ] Raw symbols (`>`, `<`, `≥`, `≤`) are used; NO HTML entities
- [ ] Greek letters use LaTeX commands
- [ ] Formula numbers (if any) are preserved

### Phase 5 — List & format check
- [ ] All numbered items (`1.`, `2)`, `（1）`, `①`) are present
- [ ] Hierarchy is correct (article → sub-item → sub-sub-item)
- [ ] Headings use the correct Markdown levels
- [ ] Paragraphs are separated by blank lines
- [ ] A blank line exists before every table
- [ ] Output is wrapped in ````markdown` with no explanatory prefix or suffix

## Error Prevention & Correction Protocol

### High-frequency errors to avoid
1. **Missing article explanations** — the blue-background explanation box is the most commonly omitted element. Treat it as mandatory.
2. **Wrong numbering** — chapter, section, article, table, and figure numbers must match the image exactly.
3. **HTML entities in formulas** — always use raw symbols.
4. **Truncated tables** — verify every row and column.
5. **Hierarchy confusion** — ensure sections (`##`) and articles (`###`) are not swapped.
6. **Paragraph omission** — long explanations may have multiple paragraphs; capture them all.

### Self-correction trigger
If the user points out any missing content, wrong numbering, or formatting error:
1. Acknowledge the mistake immediately.
2. Re-examine the screenshot carefully.
3. Supply the missing or corrected content.
4. Explain what was missed and why (to prevent recurrence).
5. **Re-run the full Mandatory Internal Review checklist** before presenting the corrected output.

## Output Example

The final response must look exactly like this (wrapped in a Markdown code block):

````markdown
# 3 基本规定

## 3.1 一般规定

### 3.1.1
[正文内容，保持原始措辞]

#### 条文说明
[完整的条文说明内容，所有段落保留，不得截断]

### 3.1.2
[正文内容]

1. 第一款内容
2. 第二款内容

**表3.1.4-1 每台储罐地基勘探点数量**

| 储罐容量 V (m³) | 勘探点数量 (个) |
|:---:|:---:|
| V < 10000 | 2 |
| 10000 ≤ V < 30000 | 3 |
| V ≥ 30000 | 4 |

注：1 表中数据为基本要求。
````

## Final Delivery Rules

- Return **only** the ````markdown` block.
- No "以下是转换结果" or "转换完成" prefix.
- No post-script explanations.
- The Markdown must be copy-paste ready for Obsidian.
