# 0002 — Build evaluation harness

Status: Implemented  
Depends on: [0001](./0001-align-skill-validator.md)  
Unblocks: 0003, 0004, 0006  
Source: [`0000-skill-evaluation-hardening.md`](./0000-skill-evaluation-hardening.md)

## Goal

Ship one repository-level command that runs skill evals in isolated context and
persists comparable results.

## Work

1. Add a maintainer command (not copied into installed skill payloads) that:
   - discovers published skills and their `evals/eval_queries.json` and
     `evals/evals.json` datasets;
   - runs each trigger query three times in a clean context;
   - honors a documented train/validation partition;
   - runs each output case with the candidate skill and a declared baseline
     (no-skill or a snapshot of the previous skill version);
   - records model, duration, token usage, outputs, assertion evidence, and
     failures;
   - writes per-case grading plus an aggregate `benchmark.json`;
   - classifies infrastructure failures (rate limits, missing credentials,
     host outages) separately from skill assertion failures;
   - excludes infrastructure failures from skill pass-rate calculations;
   - exits non-zero only for defined quality gates, not for missing optional
     telemetry.
2. Persist run artifacts outside installed skill directories (for example
   `maintenance/evals-out/` or a gitignored workspace). Compact, stable
   fixtures stay with the skill; generated workspaces do not.
3. Document the command, required environment, and how to name a baseline.
4. Add a dry or fixture-backed test that the harness:
   - discovers a sample skill;
   - writes grading and benchmark files;
   - does not count a simulated rate-limit as a skill fail.

## Completion

- One named command is the evaluation entry point.
- Isolated three-run trigger execution and with-skill versus baseline output
  execution are implemented.
- Infrastructure failures are reported and excluded from pass-rate.
- Generated results are not part of the install payload.
- A repository test covers discovery, persistence, and infrastructure
  classification without calling a live model if that would be flaky.

## Out of scope

Authoring the missing per-skill eval datasets. That is 0003. First live
benchmark recording is 0006.
