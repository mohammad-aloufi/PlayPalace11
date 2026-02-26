# Monopoly Wave 6 Mario Celebration Promotion Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Promote `mario_celebration` by adding both card remap and card cash override behavior with deterministic test coverage.

**Architecture:** Keep runtime unchanged; add celebration capability data and registry capability ads, then verify with contract tests and integration tests.

**Tech Stack:** Python 3.13, pytest, Monopoly board rule-pack modules/registry.

---

### Task 1: Add failing celebration contract tests
- Modify: `server/tests/test_monopoly_board_rules_registry.py`
- Modify: `server/tests/test_monopoly_mario_rule_packs.py`

### Task 2: Add failing celebration integration tests
- Modify: `server/tests/test_monopoly_mario_boards.py`

### Task 3: Implement celebration module mappings
- Modify: `server/games/monopoly/board_rules/mario_celebration.py`
- Modify: `server/games/monopoly/board_rules_registry.py`

### Task 4: Verify targeted suites + Monopoly regression
- Run focused tests then `pytest -k monopoly -v`.

### Task 5: Update Mario promotion notes
- Modify: `docs/plans/2026-02-26-monopoly-mario-board-anchor-notes.md`
