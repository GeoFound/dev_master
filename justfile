default:
    just check

check:
    bash scripts/check_ai_base.sh
    bash scripts/check_phase1_kernel.sh

docs:
    just check

cold-start:
    bash scripts/check_ai_base.sh
    sed -n '1,220p' 24-ai-cold-start.md
    sed -n '1,220p' tasks/current.md

validate-contract:
    bash scripts/check_ai_base.sh
    rg -n 'runner_contract_version: "software-change-runner-v1"' contracts templates 04-pipeline.md 05-quality.md 00-index.md AGENTS.md

phase1-check:
    bash scripts/check_ai_base.sh
    bash scripts/check_phase1_kernel.sh

phase1-runner:
    python3 runner/local_worktree_runner.py --requested-change "Manual Phase 1 runner facts emission" --menmery-context-ref "manual" --trace-id "manual-phase1-runner" --output /tmp/dev_master-runner-facts.yaml --allow-empty

phase1-verify-fixtures:
    python3 verifier/verifier.py --facts tests/fixtures/good_runner_facts.yaml --expect-decision allow
    python3 verifier/verifier.py --facts tests/fixtures/bad_runner_facts.yaml --expect-decision block

drift-check:
    bash scripts/check_ai_base.sh
    test -f reports/drift/2026-04-27-ai-cold-start-base.md

gate-a:
    bash scripts/check_ai_base.sh
    test -f reports/gate-a-design-freeze.md
