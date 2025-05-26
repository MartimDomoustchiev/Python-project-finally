import os

USERS_FILE = "users.txt"

def register():
    username = input("Въведите потребителско име: ")
    password = input("Въведите парола: ")
    if user_exists(username):
        print("Потребителското име вече съществува.")
        return False
    with open(USERS_FILE, "a") as f:
        f.write(f"{username},{password},5000\n")
    print("Регистрацията Ви е успешна. В момента имате 5000 кредита.")
    return True

def user_exists(username):
    if not os.path.exists(USERS_FILE):
        return False
    with open(USERS_FILE, "r") as f:
        for line in f:
            if line.split(",")[0] == username:
                return True
    return False

def login():
    username = input("Потребителско име: ")
    password = input("Парола: ")
    if not os.path.exists(USERS_FILE):
        print("Няма регистрирани потребители.")
        return None
    with open(USERS_FILE, "r") as f:
        for line in f:
            user, pwd, credits = line.strip().split(",")
            if user == username and pwd == password:
                print(f"Успешен вход. Имате {credits} кредита.")
                return username
    print("Грешно потребителско име или парола.")
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
