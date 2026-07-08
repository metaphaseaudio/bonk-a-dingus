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
3. **Log it!** Tell the user what you intend to do, **ask permission** and then
   run the bundled script. This handles all the heavy lifting for you when you
   provide the fields listed below. Note that the `--correction` must be 
   provided in a unified diff format with `---`,`+++`, and `@@` hunks. It must
   contain the full paths of the files you intend to edit.
    ```
    "${CLAUDE_PLUGIN_DATA}/.venv/bin/python" "${CLAUDE_PLUGIN_ROOT}/skills/bonk-a-dingus/scripts/log_bonk.py" \
       --rules "..." --what "..." --why "..." --correction "..."
    ```
4. **Resolve the flagged violation** This is done last to ensure all the context
   remains fresh.

## Fields for the script
| Flag           | Holds                                                                                  |
|----------------|----------------------------------------------------------------------------------------|
| `--rules`      | the file + section reference + quoted text of the rule(s) violated                     |
| `--what`       | the specific action/output that violated the rules                                     |
| `--why`        | the circumstances that lead to the violation                                           |
| `--correction` | the minimal, generic rule-edit as a unified diff (omit if nothing needs to be changed) |

## Rules

- Order is fixed. Never fix the offense before logging, or log before 
  diagnosing.
- One entry per violation
- A rule change is optional. "The existing rule was clear and adequate, I am a
  hatful pile of linear algebra that ignored it" is a valid outcome, and better
  than inventing fixes that only add noise.
- Rule edits must stay generic and encode the class of the mistake only. The
  details of what happened belong in the log, and not in the rules files.
