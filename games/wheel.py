import random
from account.user import update_user_credits

def play_wheel(username, credits):
    print("Играеш: Колелото на късмета")

    try:
        spin_cost = int(input("Въведи сума за завъртане на колелото: "))
        if spin_cost <= 0 or spin_cost > credits:
            print("Невалидна сума.")
            return credits
    except ValueError:
        print("Моля въведи валидна сума.")
        return credits

    credits -= spin_cost

    wheel_sectors = [
        ("🎉 Джакпот!", 10),
        ("💸 Двойна печалба!", 2),
        ("➕ Малка печалба", 1.5),
        ("➖ Минимална печалба", 1.1),
        ("0️⃣ Нищо", 0),
        ("💀 Загуба", 0),
        ("💀 Загуба", 0),
        ("💀 Загуба", 0),
        ("➖ Малка печалба", 1.2),
        ("💸 Двойна печалба!", 2),
        ("0️⃣ Нищо", 0),
        ("🎯 Голяма печалба", 5),
    ]

    result = random.choice(wheel_sectors)
    description, multiplier = result
    winnings = int(spin_cost * multiplier)
    print(f"Завъртане... Сектор: {description}")
    print(f"Печелите: {winnings} кредита!")
    credits += winnings
    
    update_user_credits(username, credits)
    return credits
