import random
from account.user import update_user_credits

symbols = ["🍒", "🔔", "🍋", "⭐", "7️⃣", "💎"]
payouts = {
    ("🍒", "🍒", "🍒"): 2,
    ("🔔", "🔔", "🔔"): 3,
    ("🍋", "🍋", "🍋"): 4,
    ("⭐", "⭐", "⭐"): 5,
    ("7️⃣", "7️⃣", "7️⃣"): 10,
    ("💎", "💎", "💎"): 20,
}

def spin():
    return [random.choice(symbols) for _ in range(3)]

def play_slot(username, credits):
    print("Играеш: Машинки")
    
    try:
        bet = int(input("Въведи залог: "))
        if bet <= 0 or bet > credits:
            print("Невалиден залог.")
            return credits
    except ValueError:
        print("Въведи валидна стойност.")
        return credits

    result = spin()
    print("Завъртане...")
    print(" | ".join(result))

    if tuple(result) in payouts:
        multiplier = payouts[tuple(result)]
        win = bet * multiplier
        print(f"СПЕЧЕЛИ! Печалба x{multiplier}: {win} кредита!")
        credits += win
    else:
        print("Загуби залога.")
        credits -= bet

    update_user_credits(username, credits)
    return credits
