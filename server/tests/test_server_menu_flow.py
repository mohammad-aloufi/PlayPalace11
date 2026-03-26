"""Tests for chat and keybind flows in core.server.Server."""

from types import SimpleNamespace

import pytest

from server.core.server import Server
from server.core.users.network_user import NetworkUser
from server.core.users.base import TrustLevel


class DummyConnection:
    def __init__(self):
        self.sent = []

    async def send(self, payload):
        self.sent.append(payload)


def make_network_user(name="Player", locale="en", trust=TrustLevel.USER, approved=True):
    user = NetworkUser(name, locale, DummyConnection(), approved=approved)
    user.set_trust_level(trust)
    user.set_approved(approved)
    return user


@pytest.fixture
def server(tmp_path):
    db_path = tmp_path / "menu.db"
    srv = Server(db_path=str(db_path), locales_dir="locales", config_path=tmp_path / "missing.toml")
    return srv


@pytest.mark.asyncio
async def test_handle_chat_local_not_in_table_reaches_lobby(server):
    host = make_network_user("Host")
    lobby_friend = make_network_user("LobbyFriend")
    in_table = make_network_user("InTable")
    pending = make_network_user("Pending", approved=False)
    server._users = {
        host.username: host,
        lobby_friend.username: lobby_friend,
        in_table.username: in_table,
        pending.username: pending,
    }

    class DummyTable:
        def __init__(self):
            self.members = [SimpleNamespace(username="InTable")]

    table = DummyTable()

    def find_user_table(username):
        return table if username == "InTable" else None

    server._tables = SimpleNamespace(find_user_table=find_user_table)

    client = SimpleNamespace(username=host.username)
    await server._handle_chat(client, {"convo": "local", "message": "hi"})

    assert lobby_friend.connection.sent
    assert lobby_friend.connection.sent[-1]["type"] == "chat"
    assert lobby_friend.connection.sent[-1]["message"] == "hi"
    assert host.connection.sent
    assert host.connection.sent[-1]["type"] == "chat"
    assert host.connection.sent[-1]["message"] == "hi"
    assert not in_table.connection.sent
    assert not pending.connection.sent


@pytest.mark.asyncio
async def test_handle_keybind_whos_at_table_when_not_in_game(server):
    caller = make_network_user("Caller")
    lobby_friend = make_network_user("LobbyFriend")
    in_table = make_network_user("InTable")
    server._users = {
        caller.username: caller,
        lobby_friend.username: lobby_friend,
        in_table.username: in_table,
    }

    class DummyTable:
        pass

    table = DummyTable()

    def find_user_table(username):
        return table if username == "InTable" else None

    server._tables = SimpleNamespace(find_user_table=find_user_table)

    client = SimpleNamespace(username=caller.username)
    await server._handle_keybind(
        client,
        {"key": "w", "control": True},
    )

    messages = caller.get_queued_messages()
    assert messages, "expected speak message for ctrl+w"
    assert messages[-1]["type"] == "speak"
    assert "Caller" in messages[-1]["text"]
    assert "LobbyFriend" in messages[-1]["text"]
    assert "user" in messages[-1]["text"].lower()
