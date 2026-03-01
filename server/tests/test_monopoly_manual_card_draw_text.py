"""Tests for manual card draw text resolution in Monopoly runtime."""

from server.games.monopoly.game import MonopolyGame, MonopolyOptions
from server.messages.localization import Localization
from server.core.users.test_user import MockUser


def _start_game(board_id: str) -> MonopolyGame:
    game = MonopolyGame(
        options=MonopolyOptions(
            preset_id="classic_standard",
            board_id=board_id,
            board_rules_mode="auto",
        )
    )
    game.add_player("Host", MockUser("Host"))
    game.add_player("Guest", MockUser("Guest"))
    game.host = "Host"
    game.on_start()
    return game


def test_manual_card_draw_text_prefers_literal_text() -> None:
    game = _start_game("star_wars_saga")
    resolved = game._resolve_card_draw_text(
        {"text": "Sith: Move to Coruscant Senate."},
        "advance_to_go",
    )
    assert resolved == "Sith: Move to Coruscant Senate."


def test_manual_card_draw_text_uses_manual_text_key_when_localized() -> None:
    game = _start_game("star_wars_saga")
    resolved = game._resolve_card_draw_text(
        {"text_key": "monopoly-card-go-to-jail"},
        "bank_dividend_50",
    )
    assert resolved == Localization.get("en", "monopoly-card-go-to-jail")


def test_manual_card_draw_text_falls_back_when_manual_text_key_missing() -> None:
    game = _start_game("star_wars_saga")
    resolved = game._resolve_card_draw_text(
        {"text_key": "monopoly-card-star-wars-saga-nonexistent"},
        "bank_dividend_50",
    )
    assert resolved == Localization.get("en", "monopoly-card-bank-dividend-50")
