# Five-minute Quick Start

Use this guide to install the FDE operating-analysis Skill into a disposable Git repository and run one operating analysis. The Skill returns a decision-oriented minimum operating solution; it does not prove enterprise acceptance, authority, production readiness, or value.

## 1. Get FDE

Install Git, Make, and [uv](https://docs.astral.sh/uv/), then clone the repository:

```bash
git clone https://github.com/CarlLee1983/FDE.git
cd FDE
make verify
```

You may instead download and unpack a source archive for Skill installation. `make verify` requires a Git checkout because release scenarios and Pages content are selected from tracked files.

## 2. Install into a test repository

Create a temporary Git repository and install independent Codex and Claude Code copies:

```bash
target_dir="$(mktemp -d)"
git -C "$target_dir" init
scripts/install-skill.sh --target "$target_dir" --agent both
```

For a real project, replace `$target_dir` with its repository root. The equivalent Make command is:

```bash
make install-skill TARGET=/path/to/project AGENT=both
```

## 3. Confirm the installation

```bash
test -f "$target_dir/.agents/skills/fde-project-work/SKILL.md"
test -f "$target_dir/.claude/skills/fde-project-work/SKILL.md"
test ! -L "$target_dir/.agents/skills/fde-project-work"
test ! -L "$target_dir/.claude/skills/fde-project-work"
```

The installer does not edit the target's `AGENTS.md`, `CLAUDE.md`, README, or other settings.

Each installed copy includes the required FDE method snapshots, scenario schema, and validator. It never resolves FDE guidance through similarly named files in the target repository. Large synthetic examples, translations, and method rationale remain optional fixed-version online references in the installed `references/source-map.md`; the installed Skill does not need them to work.

## 4. Call the Skill

Start Codex or Claude Code from the target repository. In Codex, paste the full prompt below. In Claude Code, invoke `/fde-project-work`, then paste the same operating problem; the full text below also states the intended Skill explicitly.

```text
Use $fde-project-work to analyze this operating problem:

每週五，營運人員手動下載合作商 CSV，重新命名固定欄位、
移除缺少帳號的資料、轉換日期、去除重複列後交給匯入人員。
規則已固定且有版本，這項工作每週約花二十分鐘。
請判斷下一步應該做什麼，以及是否需要 AI。
```

The expected answer has five sections:

1. Operating problem and outcome.
2. Current-work diagnosis.
3. Technology-neutral target workflow.
4. Intervention and AI-fit decision, with evidence limits.
5. Next accountable action.

For this prompt, the stable transformation rules should be considered for deterministic software before AI. The Skill should label assumptions and evidence gaps instead of inventing enterprise evidence.

## 5. Validate a scenario from either host

`uv` is the validator's only tool dependency. Run it from the installed Skill directory, so the same command works in a Codex-only or Claude-only project:

```bash
cd /path/to/project/.agents/skills/fde-project-work # Codex
# or: cd /path/to/project/.claude/skills/fde-project-work # Claude Code
./scripts/validate-scenario.sh /path/to/scenario.json
```

## 6. Update or remove

The installer intentionally refuses to overwrite an existing Skill. To update, review or back up local Skill changes, update the FDE checkout, remove only the installed Skill directory, and run the installer again:

```bash
git -C /path/to/FDE pull --ff-only
rm -r -- /path/to/project/.agents/skills/fde-project-work
rm -r -- /path/to/project/.claude/skills/fde-project-work
/path/to/FDE/scripts/install-skill.sh --target /path/to/project --agent both
```

To remove the Skill, run only the applicable `rm -r` command above. No other target-repository file was created or changed by the installer.

For project boundaries and deeper references, continue with the [README](../README.md).
