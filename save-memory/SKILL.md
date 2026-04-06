---
name: save-memory
description: Save the current conversation context into an Obsidian memory note for cross-device recovery, and support网状 memory restoration by reading linked memories and preloaded files. Use when the user says "保存记忆", "保存本次记忆", "记忆保存", or asks to archive the conversation. Also use when the user says "恢复记忆", "恢复上下文", or asks to resume a previous session.
---

# Save Memory

Capture the current conversation as a structured Markdown note in the user's Obsidian vault, and restore context by reading linked memories and key files.

## Quick Triggers — Save

- "保存记忆"
- "保存本次记忆"
- "记忆保存"
- "把这次对话记下来"
- "归档本次会话"

## Quick Triggers — Restore

- "恢复记忆"
- "恢复上下文"
- "继续上次的工作"
- "接上之前的进度"

---

## Part A: Saving Memory

### Step 1: Determine the topic
Ask the user for a **short Chinese topic name** if it is not obvious from the conversation. Examples:
- If the whole chat was about `split-spec-notes`, the topic is `规范精读拆分`.
- If it was about learning article 3.1.4, the topic is `钢储罐地规-3.1.4学习`.
- If it was a general Q&A, the topic is `通用问答`.

### Step 2: Summarize the conversation
Extract and structure the following sections in Chinese:

1. **会话主题** — One-line summary.
2. **关键决策** — Bullet list of important decisions, agreements, or file changes made during the chat.
3. **修改/创建的文件** — Bullet list of every file created or modified, with full paths. Mark skill files, templates, and generated notes clearly.
4. **未完成事项** — Bullet list of TODOs or open questions.
5. **快速恢复指令** — A short paragraph the user can copy-paste into Kimi on another device to resume work.

### Step 3: Identify related memories and preload files
Automatically derive two frontmatter lists:

- **`关联记忆`** — Search `D:\job\400-软件\480-kimicode\记忆\` for files with the **same topic** or **overlapping keywords** in the filename. Include up to 3 recent ones (within the last 7 days). If none, leave empty.
- **`预读文件`** — Extract up to 5 key file paths from the "修改/创建的文件" section. Prioritize:
  1. The relevant `SKILL.md`
  2. Template files (`规范精读-*.md`)
  3. Source study notes (`*学习.md`)
  4. Representative generated article notes (`*3.1.4.md` etc.)

### Step 4: Save with script
Run the bundled script:

```bash
python scripts/save_memory.py \
  --topic "规范精读拆分" \
  --content-file "D:\job\temp_memory.md" \
  --related-memories "D:\job\400-软件\480-kimicode\记忆\XXX-会话-2026-04-01.md" \
  --preload-files "D:\job\999-模板\规范精读模板\规范精读-条.md"
```

Notes:
- If `--related-memories` or `--preload-files` have multiple items, pass them as **space-separated, quoted paths**.
- The script stores them as YAML list strings in the frontmatter.

The script will:
- Create or append to `<主题>-会话-YYYY-MM-DD.md`
- Place it in `D:\job\400-软件\480-kimicode\记忆\`
- Print the saved filename

### File Naming Rule

- **New session on a new day**: `规范精读拆分-会话-2026-04-02.md`
- **Same topic, same day, multiple saves**: The script automatically appends a separator (`---`) and the new content to the existing file.

---

## Part B: Restoring Memory (网状恢复)

When the user asks to restore memory, follow this **网状 recovery workflow** strictly:

### Step 1: Locate the primary memory file
Search `D:\job\400-软件\480-kimicode\记忆\` for the most recent file matching the user's topic keyword.

If the user gives a path, use it directly.

### Step 2: Read the primary memory file
Use `ReadFile` to load the primary memory note. Parse its YAML frontmatter for:
- `主题`
- `关联记忆` (list of related memory file paths)
- `预读文件` (list of key file paths)

### Step 3: Read linked memories (MANDATORY)
**You MUST read every file listed in `关联记忆`.** These provide historical context from previous days or related sub-topics.

### Step 4: Read preloaded files (MANDATORY)
**You MUST read every file listed in `预读文件`.** These are the skill definitions, templates, and sample notes that define the current working state.

### Step 5: Synthesize and report
Summarize the restored context for the user:
- What was the overall project/theme?
- What key decisions were made across all linked memories?
- What files are currently in play?
- What unfinished items remain?
- Ask: "Which unfinished item would you like to continue with?"

---

## Cross-Device Setup

On a new computer, after坚果云 sync finishes, re-establish the Junction:

```powershell
$cloudSkills = "D:\坚果云\1C - work - 个人设置\kimi code\skills"
$localSkills = "$env:USERPROFILE\.kimi\skills"
if (Test-Path $localSkills) { rd /S /Q $localSkills }
cmd /c "mklink /J ""$localSkills"" ""$cloudSkills"""
```

Then simply say:

> "恢复规范精读拆分的记忆"
