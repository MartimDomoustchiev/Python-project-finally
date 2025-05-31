import random
from account.user import update_user_credits

def play_roulette(username, credits):
    print("Играеш: Рулетка")
    print("Заложи на червено (r), черно (b) или точно число (0-36)")

    try:
        bet = int(input("💰 Въведи залог (сума): "))
        if bet <= 0 or bet > credits:
            print("Невалиден залог.")
            return credits
    except ValueError:
        print("Невалидна сума.")
        return credits

    choice = input("Избор (r / b / 0-36): ").strip().lower()

    if choice not in ['r', 'b'] and not (choice.isdigit() and 0 <= int(choice) <= 36):
        print("Невалиден избор.")
        return credits

    result = random.randint(0, 36)

    red_numbers = {
        1, 3, 5, 7, 9, 12, 14, 16, 18,
        19, 21, 23, 25, 27, 30, 32, 34, 36
    }
    black_numbers = {
        2, 4, 6, 8, 10, 11, 13, 15, 17,
        20, 22, 24, 26, 28, 29, 31, 33, 35
    }

    print(f"Рулетката спря на: {result} {'🔴' if result in red_numbers else '⚫' if result in black_numbers else '🟢'}")

    win = False

    if choice == 'r' and result in red_numbers:
        win = True
        credits += bet
    elif choice == 'b' and result in black_numbers:
        win = True
        credits += bet
    elif choice.isdigit() and int(choice) == result:
        win = True
        credits += bet * 35
    else:
        credits -= bet

    if win:
        print(f"Печелите! Нов баланс: {credits}")
    else:
        print(f"Губиш! Нов баланс: {credits}")

    update_user_credits(username, credits)
    return credits
