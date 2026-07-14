---
name: bonk-a-dingus
description: Backpressure/memory mechanism to use when an agent has violated the rules in a CLAUDE.md/AGENTS.md, or needs new ones.
---

# Bonk a Dingus

## Overview

Turn a flagged rule violation, or displeasing behaviour into a learning
opportunity with the following steps in order:

1. root-cause it
2. decide whether this is a new rule, or an existing rule needs to change and 
   how.
3. log it with the bundled script

Rules may live in a repository's `CLAUDE.md`/`AGENTS.md` files, globally in 
`~/CLAUDE.md`, `~/.claude/CLAUDE.md`, in a project's memory files, or in rules
files referenced in any of the above.

 ## Procedure

Follow these steps **in order** (order *really* matters.) Create a todo per step
so the order is stable.

1. **Identify and reflect.** Quote the exact rule(s) and the file they in which
   they live (or the new rule if this is a new rule.) State the specific action
   or output that broke the rules, and root-cause why that action was taken. If
   the rule which applies is genuinely unclear, say so and ask rather than guess.
2. **Determine the modifications.** Decide whether the rule itself should change
   (ie. ambiguous, missed a case, was generally weak, etc.) or whether the rule
   was adequate and ignored without cause. **DO NOT fabricate a rule change just
   for the sake of it!** If changing a rule, write the minimal edit that would
   have caught this exact class of mistake, and keep it generic so the 
   always-loaded rules files do not accumulate noise specific to sessions.
   Identify the fix for whatever was flagged as a part of this step.
3. **Log it, applying a fix if there is one.** Tell the user what you intend
   to do, then call the bundled `log_bonk` MCP tool directly — no bash
   script, no CLI flags.
   - Call `log_bonk` with `rules`, `what`, `why`, and (if, and only if, step
     2 concluded a rule file itself needs to change) `correction` as a
     unified diff (`---`, `+++`, `@@` hunks, full paths). In one call this
     both applies the diff (if given) and writes the log entry — the two
     never happen separately, so the log always reflects exactly what was
     applied.
   - This tool always requires explicit user approval, regardless of any
     permission mode already granted — treat a denial as a final "no": do
     not retry with a different diff to route around it, and do not fall
     back to Edit/Write on the rules file instead. Nothing is applied or
     logged if denied.
   - If applying the diff fails, re-read the file, regenerate the diff
     against current content, and call `log_bonk` again; this is not
     something to catch and log around.
4. **Resolve the flagged violation** This is done last to ensure all the context
   remains fresh.

## Fields for the tool
| Tool        | Parameter    | Holds                                                                |
|-------------|--------------|-----------------------------------------------------------------------|
| `log_bonk`  | `rules`      | file + section reference + quoted text of the rule(s) violated        |
| `log_bonk`  | `what`       | the specific action/output that violated the rules                    |
| `log_bonk`  | `why`        | the circumstances that led to the violation                           |
| `log_bonk`  | `correction` | the rule-edit as a unified diff (omit if none), format below          |

`correction` header paths must be plain absolute paths — no `a/`/`b/` prefix:
```
--- /full/path/to/CLAUDE.md
+++ /full/path/to/CLAUDE.md
@@ ...
```

## Rules

- Order is fixed. Never fix the offense before logging, or log before 
  diagnosing.
- One entry per violation
- A rule change is optional. "The existing rule was clear and adequate, I am a
  hatful pile of linear algebra that ignored it" is a valid outcome, and better
  than inventing fixes that only add noise.
- Rule edits must stay generic and encode the class of the mistake only. The
  details of what happened belong in the log, and not in the rules files.
