import os

USERS_FILE = "users.txt"

def register(username, password):
    if user_exists(username):
        return False
    with open(USERS_FILE, "a") as f:
        f.write(f"{username},{password},5000\n")
    return True

def user_exists(username):
    if not os.path.exists(USERS_FILE):
        return False
    with open(USERS_FILE, "r") as f:
        for line in f:
            if line.strip().split(",")[0] == username:
                return True
    return False

def login(username, password):
    if not os.path.exists(USERS_FILE):
        return None
    with open(USERS_FILE, "r") as f:
        for line in f:
            user, pwd, credits = line.strip().split(",")
            if user == username and pwd == password:
                return username
    return None

def get_user_credits(username):
    if not os.path.exists(USERS_FILE):
        return 0
    with open(USERS_FILE, "r") as f:
        for line in f:
            user, pwd, credits = line.strip().split(",")
            if user == username:
                return int(credits)
    return 0

def update_user_credits(username, new_credits):
    if not os.path.exists(USERS_FILE):
        return
    lines = []
    with open(USERS_FILE, "r") as f:
        lines = f.readlines()
    with open(USERS_FILE, "w") as f:
        for line in lines:
            user, pwd, credits = line.strip().split(",")
            if user == username:
                f.write(f"{user},{pwd},{new_credits}\n")
            else:
                f.write(line)
