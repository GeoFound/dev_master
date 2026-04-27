default:
    just check

check:
    rg -n "schema_version|policy_version|ruleset_version|Gate E|Gate F|Phase 4|Phase 5|九大 AI" *.md AGENTS.md && exit 1 || true

docs:
    just check
