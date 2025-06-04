import pytest
import random
from account import user

def test_register_and_login(tmp_path):
    test_file = tmp_path / "users.txt"
    user.USERS_FILE = str(test_file)

    assert user.register("testuser", "password") is True
    assert user.register("testuser", "password") is False
    assert user.user_exists("testuser") is True
    assert user.login("testuser", "password") == "testuser"
    assert user.login("testuser", "wrong") is None

def test_roulette_win_and_loss(monkeypatch):
    user.USERS_FILE = "users.txt"
    username = "rouletteplayer"
    user.register(username, "pwd")
    starting_credits = user.get_user_credits(username)

    def fake_randint(low, high):
        return 3  

    monkeypatch.setattr("random.randint", fake_randint)

    credits = starting_credits
    credits -= 1000  
    choice = 'r'    
    result = fake_randint(0, 36)
    red_numbers = {
        1, 3, 5, 7, 9, 12, 14, 16, 18,
        19, 21, 23, 25, 27, 30, 32, 34, 36
    }

    if choice == 'r' and result in red_numbers:
        credits += int(1000 * 0.5)  

    user.update_user_credits(username, int(credits))
    assert credits == user.get_user_credits(username)

def test_deposit_and_withdraw():
    from account.account import Account

    account = Account("player1")
    initial_balance = account.get_balance()

    account.deposit(1000)
    assert account.get_balance() == initial_balance + 1000

    success = account.withdraw(3000)
    assert success is True
    assert account.get_balance() == initial_balance + 1000 - 3000

    fail = account.withdraw(10000)
    assert fail is False
    assert account.get_balance() == initial_balance + 1000 - 3000

def test_user_exists_false():
    user.USERS_FILE = "users.txt"
    assert user.user_exists("nonexistentuser") is False

def test_login_none():
    user.USERS_FILE = "users.txt"
    assert user.login("nouser", "nopass") is None
