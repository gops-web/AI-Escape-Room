
from game_logic import EscapeRoom


def test_correct_escape():
    game = EscapeRoom()

    game.examine("bookshelf")
    assert "opens" in game.unlock_drawer("3142")

    game.collect_key()
    game.examine("painting")
    game.examine("clock")

    result = game.unlock_door("0845")

    assert game.escaped is True
    assert "SUCCESS" in result


def test_wrong_drawer_code():
    game = EscapeRoom()

    game.examine("bookshelf")
    game.unlock_drawer("9999")

    assert game.drawer_open is False


def test_cannot_collect_key_early():
    game = EscapeRoom()

    game.collect_key()

    assert "brass key" not in game.inventory


def test_cannot_escape_without_clues():
    game = EscapeRoom()

    game.unlock_door("0845")

    assert game.escaped is False


def test_wrong_exit_code():
    game = EscapeRoom()

    game.examine("bookshelf")
    game.unlock_drawer("3142")
    game.collect_key()
    game.examine("painting")
    game.examine("clock")

    game.unlock_door("1234")

    assert game.escaped is False
