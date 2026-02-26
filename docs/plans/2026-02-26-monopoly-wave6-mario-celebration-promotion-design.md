# Monopoly Wave 6 Mario Celebration Promotion Design

Date: 2026-02-26
Branch: `monopoly`
Status: approved

## Goal
Promote `mario_celebration` with both board card capabilities so gameplay differs in `board_rules` mode while `skin_only` remains baseline.

## Scope
### In scope
- Add `card_id_remap` and `card_cash_override` to `mario_celebration`.
- Mappings:
  - `("chance", "poor_tax_15") -> "bank_dividend_50"`
  - `"income_tax_refund_20" -> 60`
- Add contract tests and integration tests for board-rules vs skin-only behavior.

### Out of scope
- New runtime capability types.
- Junior Mario behavior changes.

## Architecture
Reuse existing Wave 4 runtime hooks and registry helpers. This wave is data-only in the celebration module plus capability advertising in registry.

## Success Criteria
1. Celebration remap changes Chance outcome only in `board_rules` mode.
2. Celebration cash override changes Community Chest payout only in `board_rules` mode.
3. Monopoly regression remains green.
