#!/usr/bin/env bash
set -euo pipefail

fail=0

require_file() {
  local path="$1"
  if [[ ! -f "$path" ]]; then
    printf 'missing required file: %s\n' "$path" >&2
    fail=1
  fi
}

require_dir() {
  local path="$1"
  if [[ ! -d "$path" ]]; then
    printf 'missing required directory: %s\n' "$path" >&2
    fail=1
  fi
}

require_text() {
  local path="$1"
  local pattern="$2"
  if ! rg -q "$pattern" "$path"; then
    printf 'missing required text in %s: %s\n' "$path" "$pattern" >&2
    fail=1
  fi
}

active_docs=(
  "00-index.md"
  "02-tools-cost.md"
  "03-ai-roles.md"
  "04-pipeline.md"
  "05-quality.md"
  "06b-state-persistence.md"
  "07-governance.md"
  "08-repo-structure.md"
  "09-roadmap.md"
  "13-appendix.md"
  "14-master-program.md"
  "15-phase-gates.md"
  "16-drift-control.md"
  "17-task-templates.md"
  "18-master-execution-task.md"
  "19-human-governance-boundary.md"
  "20-layered-program-map.md"
  "21-agent-behavior-guidelines.md"
  "22-three-plane-architecture.md"
  "23-menmery-integration.md"
  "24-ai-cold-start.md"
  "25-implementation-language-baseline.md"
  "AGENTS.md"
  "README.md"
  "ai-instructions.md"
)

required_files=(
  "AGENTS.md"
  "ai-instructions.md"
  "00-index.md"
  "20-layered-program-map.md"
  "23-menmery-integration.md"
  "24-ai-cold-start.md"
  "25-implementation-language-baseline.md"
  "tasks/current.md"
  "tasks/backlog.md"
  "contracts/software-change-runner-v1.yaml"
  "templates/build-task.md"
  "templates/verify-task.md"
  "templates/drift-check.md"
  "templates/gate-report.md"
  "templates/activation-proposal.md"
  "templates/runner-facts.yaml"
  "templates/verification-report.md"
  "reports/gate-a-design-freeze.md"
  "reports/drift/2026-04-27-ai-cold-start-base.md"
  "scripts/check_ai_base.sh"
  "justfile"
)

required_dirs=(
  "tasks"
  "templates"
  "contracts"
  "reports"
  "reports/drift"
  "scripts"
)

for path in "${required_dirs[@]}"; do
  require_dir "$path"
done

for path in "${required_files[@]}"; do
  require_file "$path"
done

if [[ "$fail" -ne 0 ]]; then
  exit "$fail"
fi

for path in "${active_docs[@]}"; do
  require_file "$path"
done

for path in \
  "contracts/software-change-runner-v1.yaml" \
  "templates/runner-facts.yaml" \
  "templates/verify-task.md" \
  "templates/verification-report.md"; do
  require_text "$path" 'runner_contract_version: "software-change-runner-v1"'
done

require_text "tasks/current.md" 'current_phase: "Phase 0 - Design Freeze"'
require_text "tasks/current.md" 'last_completed_task: "phase-0-ai-cold-start-base"'
require_text "tasks/current.md" 'last_completed_task_2: "phase-0-implementation-language-baseline"'
require_text "tasks/current.md" 'task_id: "gate-a-design-freeze-review"'
require_text "24-ai-cold-start.md" 'tasks/current.md'
require_text "24-ai-cold-start.md" 'just check'
require_text "24-ai-cold-start.md" '25-implementation-language-baseline.md'
require_text "25-implementation-language-baseline.md" 'runner / harness / verifier | Python'
require_text "25-implementation-language-baseline.md" 'repository commands | `just` \+ small Bash scripts'
require_text "25-implementation-language-baseline.md" 'Go belongs to `auto_router`'
require_text "25-implementation-language-baseline.md" 'Do not introduce TypeScript or JavaScript for Phase 1 core implementation'
require_text "AGENTS.md" '24-ai-cold-start.md'
require_text "AGENTS.md" '25-implementation-language-baseline.md'
require_text "ai-instructions.md" '24-ai-cold-start.md'
require_text "ai-instructions.md" '25-implementation-language-baseline.md'
require_text "justfile" 'check_ai_base.sh'

forbidden_pattern='schema_version|policy_version|ruleset_version|Gate E|Gate F|Phase 4|Phase 5|九大 AI'
if rg -n "$forbidden_pattern" "${active_docs[@]}"; then
  printf 'forbidden active-scope wording found\n' >&2
  fail=1
fi

if rg -n 'implementation_deliverables_included: true' templates reports tasks contracts; then
  printf 'activation proposal must not include implementation deliverables\n' >&2
  fail=1
fi

if rg -n 'method: "remember"' reports tasks contracts; then
  printf 'claimed remember writeback found without explicit evidence ref\n' >&2
  fail=1
fi

exit "$fail"
