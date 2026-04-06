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

## Environment Detection (MANDATORY)

Before saving or restoring, **detect the current environment** and use the correct paths:

| Environment | Detection Method | Obsidian Vault | Skills Directory | Memory Directory |
|-------------|------------------|----------------|------------------|------------------|
| **Kimi Claw** | Linux path `/root/.openclaw/` | `/root/.openclaw/workspace/job/` | `/root/.openclaw/workspace/skills/` | `/root/.openclaw/workspace/job/400-软件/480-kimicode/记忆/` |
| **VSCode Local** | Windows path `D:\job\` | `D:\job\` | `C:\Users\yj198\AppData\Roaming\Code\User\globalStorage\moonshot-ai.kimi-code\bin\kimi_internal\kimi_cli\skills` | `D:\job\400-软件\480-kimicode\记忆\` |

**Auto-detection rule**: If the current working directory starts with `/root/.openclaw/`, use **Kimi Claw paths**. Otherwise, use **VSCode Local paths**.

## Part A: Saving Memory

### Step 1: Determine the topic

Ask the user for a **short Chinese topic name** if it is not obvious from the conversation. Examples:

- If the whole chat was about `split-spec-notes`, the topic is `规范精读拆分`.
- If it was about learning article 3.1.4, the topic is `钢储罐地规-3.1.4学习`.
- If it was a general Q&A, the topic is `通用问答`.

### Step 2: Summarize the conversation

Extract and structure the following sections in **Chinese**:

- **会话主题** — One-line summary.
- **关键决策** — Bullet list of important decisions, agreements, or file changes made during the chat.
- **修改/创建的文件** — Bullet list of every file created or modified, with full paths. **Use paths appropriate to the current environment** (Linux paths for Kimi Claw, Windows paths for VSCode).
- **未完成事项** — Bullet list of TODOs or open questions.
- **快速恢复指令** — A short paragraph the user can copy-paste to resume work.

### Step 3: Identify related memories and preload files

Automatically derive two frontmatter lists:

- **`关联记忆`** — Search the **current environment's memory directory** for files with the **same topic** or **overlapping keywords** in the filename. Include up to 3 recent ones (within the last 7 days). If none, leave empty.
  - Kimi Claw: `/root/.openclaw/workspace/job/400-软件/480-kimicode/记忆/`
  - VSCode: `D:\job\400-软件\480-kimicode\记忆\`
- **`预读文件`** — Extract up to 5 key file paths from the "修改/创建的文件" section. Prioritize:
  - The relevant `SKILL.md`
  - Template files (`规范精读-*.md`)
  - Source study notes (`*学习.md`)
  - Representative generated article notes (`*3.1.4.md` etc.)

### Step 4: Save with script

Run the bundled script with environment-appropriate paths:

**For Kimi Claw:**
```bash
python3 scripts/save_memory.py \
  --topic "规范精读拆分" \
  --content-file "/tmp/temp_memory.md" \
  --memory-dir "/root/.openclaw/workspace/job/400-软件/480-kimicode/记忆/" \
  --related-memories "/root/.openclaw/workspace/job/400-软件/480-kimicode/记忆/XXX-会话-2026-04-01.md" \
  --preload-files "/root/.openclaw/workspace/skills/split-spec-notes/SKILL.md"
```

**For VSCode Local:**
```bash
python scripts/save_memory.py \
  --topic "规范精读拆分" \
  --content-file "D:\job\temp_memory.md" \
  --memory-dir "D:\job\400-软件\480-kimicode\记忆\" \
  --related-memories "D:\job\400-软件\480-kimicode\记忆\XXX-会话-2026-04-01.md" \
  --preload-files "C:\Users\yj198\AppData\Roaming\Code\User\globalStorage\moonshot-ai.kimi-code\bin\kimi_internal\kimi_cli\skills\split-spec-notes\SKILL.md"
```

Notes:

- If `--related-memories` or `--preload-files` have multiple items, pass them as **space-separated, quoted paths**.
- The script stores them as YAML list strings in the frontmatter.

The script will:

- Create or append to `<主题>-会话-YYYY-MM-DD.md`
- Place it in the environment's memory directory
- Print the saved filename

### File Naming Rule

- **New session on a new day**: `<主题>-会话-YYYY-MM-DD.md`
- **Same topic, same day, multiple saves**: The script automatically appends a separator (`---`) and the new content to the existing file.

## Part B: Restoring Memory (网状恢复)

When the user asks to restore memory, follow this **网状 recovery workflow** strictly:

### Step 1: Detect environment and locate memory

First, determine whether you're running in **Kimi Claw** or **VSCode Local** by checking the working directory.

Then search the appropriate memory directory for the most recent file matching the user's topic keyword.

If the user gives a path directly, use it (the path itself indicates the environment).

### Step 2: Read the primary memory file

Use `ReadFile` to load the primary memory note. Parse its YAML frontmatter for:

- `主题`
- `关联记忆` (list of related memory file paths)
- `预读文件` (list of key file paths)

### Step 3: Read linked memories (MANDATORY)

**You MUST read every file listed in `关联记忆`.** These provide historical context from previous days or related sub-topics.

**Environment adaptation**: The paths in `关联记忆` may be from a different environment (e.g., user saved in VSCode but is now in Kimi Claw). 

- If a path doesn't exist, try translating it:
  - `D:\job\` → `/root/.openclaw/workspace/job/`
  - `/root/.openclaw/workspace/job/` → `D:\job\`
- If translation fails, note it in the report.

### Step 4: Read preloaded files (MANDATORY)

**You MUST read every file listed in `预读文件`.** These are the skill definitions, templates, and sample notes that define the current working state.

**Environment adaptation**: Similar to Step 3, translate paths if necessary:
- Skills: `C:\Users\yj198\...\skills\` → `/root/.openclaw/workspace/skills/`
- Skills: `/root/.openclaw/workspace/skills/` → `C:\Users\yj198\...\skills\` (if running locally)

### Step 5: Synthesize and report

Summarize the restored context for the user:

- What was the overall project/theme?
- What key decisions were made across all linked memories?
- What files are currently in play?
- What unfinished items remain?
- Note any environment translation that occurred
- Ask: "Which unfinished item would you like to continue with?"

## Cross-Device Setup

### VSCode Local → Kimi Claw

1. Ensure Obsidian vault is synced via Obsidian Sync or坚果云
2. In Kimi Claw, the vault is at `/root/.openclaw/workspace/job/` (via Headless Sync)
3. Skills are at `/root/.openclaw/workspace/skills/`

### Kimi Claw → VSCode Local

1. Ensure skills are synced (via GitHub or坚果云)
2. On Windows, establish the Junction for skills:

```powershell
$cloudSkills = "D:\坚果云\1C - work - 个人设置\kimi code\skills"
$localSkills = "$env:USERPROFILE\.kimi\skills"
if (Test-Path $localSkills) { rd /S /Q $localSkills }
cmd /c "mklink /J ""$localSkills"" ""$cloudSkills"""
```

Or for the VSCode-specific path:
```powershell
$cloudSkills = "D:\坚果云\1C - work - 个人设置\kimi code\skills"
$vscodeSkills = "C:\Users\yj198\AppData\Roaming\Code\User\globalStorage\moonshot-ai.kimi-code\bin\kimi_internal\kimi_cli\skills"
# Copy or junction the skills to the VSCode path
```

### Unified Workflow

After setup, simply say in either environment:

> "恢复规范精读拆分的记忆"

The skill will auto-detect the environment and translate paths as needed.

## Path Translation Reference

| Component | Kimi Claw Path | VSCode Local Path |
|-----------|----------------|-------------------|
| Obsidian Vault | `/root/.openclaw/workspace/job/` | `D:\job\` |
| Skills | `/root/.openclaw/workspace/skills/` | `C:\Users\yj198\AppData\Roaming\Code\User\globalStorage\moonshot-ai.kimi-code\bin\kimi_internal\kimi_cli\skills` |
| Memory Directory | `/root/.openclaw/workspace/job/400-软件/480-kimicode/记忆/` | `D:\job\400-软件\480-kimicode\记忆\` |
| Temp Files | `/tmp/` | `D:\job\temp\` or `%TEMP%` |
