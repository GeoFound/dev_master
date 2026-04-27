default:
    just check

check:
    bash scripts/check_ai_base.sh

docs:
    just check

cold-start:
    bash scripts/check_ai_base.sh
    sed -n '1,220p' 24-ai-cold-start.md
    sed -n '1,220p' tasks/current.md

validate-contract:
    bash scripts/check_ai_base.sh
    rg -n 'runner_contract_version: "software-change-runner-v1"' contracts templates 04-pipeline.md 05-quality.md 00-index.md AGENTS.md

drift-check:
    bash scripts/check_ai_base.sh
    test -f reports/drift/2026-04-27-ai-cold-start-base.md

gate-a:
    bash scripts/check_ai_base.sh
    test -f reports/gate-a-design-freeze.md
