# Work index

Every feature in flight or finished, one row each. Rules for this file and the feature
files it indexes are in [AGENTS.md](../AGENTS.md) under "Work flow".

Statuses: `planned`, `in-progress`, `blocked`, `review`, `done`. The status here must
match the Status field inside the feature file. When a feature becomes `done`, move its
file to `complete/` and move its row to the Complete table in the same commit.

## Active

| Feature | Owner | Status | Updated | Notes |
|---|---|---|---|---|
| [wide-table-fit](wide-table-fit.md) | unassigned | planned | 2026-09-08 | Many-column tables squeeze to unreadable columns at terminal width; needs a fit strategy |
| [blockquote-edge-lines](blockquote-edge-lines.md) | unassigned | planned | 2026-09-08 | Quote bar draws one extra segment above and below the quoted lines (Panel edges) |

## Complete

| Feature | Owner | Completed | Notes |
|---|---|---|---|
| [markdown-renderer](complete/markdown-renderer.md) | Michael Pedersen (Claude Code) | 2026-09-08 | Token-tree renderer, CLI, sample, suite and project docs (D-001 to D-007) |
