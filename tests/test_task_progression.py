from __future__ import annotations

import unittest

from runtime_engine.task_progression import build_current_task_payload, next_available_task


class TaskProgressionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = {
            "version": "test",
            "tasks": [
                {
                    "id": "phase0.bootstrap",
                    "order": 10,
                    "title": "Bootstrap",
                    "task_type": "build-task",
                    "phase": "Phase 0",
                    "goal": "bootstrap",
                    "source_docs": ["docs/20-current-window/17-task-templates.md"],
                },
                {
                    "id": "phase0.gate-a",
                    "order": 20,
                    "title": "Gate A review",
                    "task_type": "verify-task",
                    "phase": "Phase 0",
                    "goal": "verify gate a",
                    "source_docs": ["docs/20-current-window/15-phase-gates.md"],
                    "prerequisites": {"tasks": ["phase0.bootstrap"]},
                    "gate": "A",
                },
                {
                    "id": "phase1.kernel",
                    "order": 30,
                    "title": "Kernel",
                    "task_type": "build-task",
                    "phase": "Phase 1",
                    "goal": "build kernel",
                    "source_docs": ["docs/20-current-window/REWRITE-PLAN.md"],
                    "prerequisites": {"gates": {"A": "pass"}},
                },
            ],
        }
        self.registry = {
            "documents": [
                {
                    "path": "docs/20-current-window/17-task-templates.md",
                    "role": "task-source",
                    "status": "active",
                },
                {
                    "path": "docs/20-current-window/15-phase-gates.md",
                    "role": "constraint",
                    "status": "active",
                },
                {
                    "path": "docs/20-current-window/REWRITE-PLAN.md",
                    "role": "task-source",
                    "status": "active",
                },
            ]
        }

    def test_first_available_task_is_bootstrap(self) -> None:
        state = {
            "version": "test",
            "completed_tasks": [],
            "gates": {"A": "pending", "B": "pending", "C": "pending", "D": "pending"},
        }
        task = next_available_task(self.graph, state)
        self.assertIsNotNone(task)
        self.assertEqual(task["id"], "phase0.bootstrap")

    def test_gate_review_unlocks_after_bootstrap(self) -> None:
        state = {
            "version": "test",
            "completed_tasks": ["phase0.bootstrap"],
            "gates": {"A": "pending", "B": "pending", "C": "pending", "D": "pending"},
        }
        task = next_available_task(self.graph, state)
        self.assertIsNotNone(task)
        self.assertEqual(task["id"], "phase0.gate-a")

    def test_phase1_unlocks_after_gate_pass(self) -> None:
        state = {
            "version": "test",
            "completed_tasks": ["phase0.bootstrap", "phase0.gate-a"],
            "gates": {"A": "pass", "B": "pending", "C": "pending", "D": "pending"},
        }
        task = next_available_task(self.graph, state)
        self.assertIsNotNone(task)
        payload = build_current_task_payload(task, self.graph, state, self.registry)
        self.assertEqual(payload["task"]["id"], "phase1.kernel")
        self.assertEqual(
            payload["task"]["source_docs"][0]["path"],
            "docs/20-current-window/REWRITE-PLAN.md",
        )


if __name__ == "__main__":
    unittest.main()
