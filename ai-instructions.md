# AI Instructions — dev_master

## Project Role

`dev_master` is a design reference repo, not an executable implementation. Treat markdown as architecture contracts and guidance.

## Required Reading

1. `AGENTS.md`
2. `24-ai-cold-start.md`
3. `tasks/current.md`
4. `00-index.md`
5. `23-menmery-integration.md`
6. `20-layered-program-map.md`
7. `25-implementation-language-baseline.md`
8. `03-ai-roles.md`
9. `04-pipeline.md`

## Hard Boundaries

- Use `menmery` for long-term truth, canonical evidence, audit, governance preview, and action levels.
- Use `auto_router` for LLM routing and model governance.
- Keep `dev_master` scoped to software-change runner contracts, risk facts, verifier checks, and execution boundaries.
- Use Python for Phase 1 runner/harness/verifier implementation unless a gate-approved correction changes the baseline.
- Keep `just` and Bash as command wrappers and repository checks, not complex runtime logic.
- Do not resurrect the nine-agent model.
- Do not make archived deferred/future docs active without an activation proposal.

## Local Commands

```bash
just check
just cold-start
just validate-contract
just drift-check
just gate-a
```
