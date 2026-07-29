# Session Log

## Session — 2026-07-28

### Done
- Completed exercises 1-4 in the Module 1 notebook (notebooks/01_claude_code_intro.ipynb).
- Created a new /summarize skill (.claude/commands/summarize.md) and tested it.

### Broke / Struggled
- The first cold run of /summarize had no prior session content to summarize, so it produced nothing useful until context was clarified.

### Learned
- The /summarize skill depends on real conversation history and can't infer session activity from git status alone.

---

## Session — 2026-07-29

### Done
- Completed Exercises 1-3b.
- Extended the GFF filter script with featuretype and positionrange options.

### Broke / Struggled
- Path issues requiring `../` to reference files correctly.
- Variable name mismatch (`gff_df` vs `df`).
- Confusion between `.iat` and `.iloc`.

### Learned
- pandas GFF loading options.
- Performance difference between `iterrows()` and vectorized operations.
- The concept of variable scope in the notebook kernel.

---
