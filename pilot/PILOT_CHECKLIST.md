# Pilot Checklist

Use this checklist to evaluate GADS adoption in a pilot repository before broad rollout. A pilot is not a source of global product or business rules.

## Baseline

- [ ] Record repository commit and working-tree state.
- [ ] Inventory existing agent instructions and project documentation.
- [ ] Identify project-specific architecture, stack, commands, and constraints.
- [ ] Record existing tests and CI gates.

## Trial

- [ ] Add GADS entry files on a dedicated branch.
- [ ] Preserve project-specific rules in `gads/PROJECT.md` or other project-owned documentation.
- [ ] Run one read-only discovery task.
- [ ] Run one bounded implementation task with tests.
- [ ] Run one independent review task.
- [ ] Evaluate clarity, token overhead, instruction conflicts, and agent adherence.

## Exit criteria

- [ ] No loss or replacement of existing project policy.
- [ ] Agent reports distinguish verified facts from assumptions.
- [ ] Relevant checks are reproducible.
- [ ] Human approval boundaries are respected.
- [ ] Team accepts the operational overhead.

## Findings

Record observations, evidence, and proposed changes here. Do not generalize a project-specific convention into GADS without separate review.
