import random
from account.user import update_user_credits

def play_highlow(username, credits):
    print("Играеш: Висока-ниска сума")
    current = random.randint(1, 50)
    print(f"Начално число: {current}")

    streak = 0
    bet = 0

    while True:
        if streak == 0:
            try:
                bet = int(input("Залог (или 0 за отказ): "))
                if bet == 0:
                    return credits
                if bet > credits:
                    print("Нямаш толкова кредити.")
                    continue
                credits -= bet
            except ValueError:
                print("Въведи число.")
                continue

        guess = input("Следващото число по-голямо или по-малко? (g/m): ").lower()
        if guess not in ["g", "m"]:
            print("Невалиден избор.")
            continue

        next_num = random.randint(1, 50)
        print(f"Следващо число: {next_num}")

        if (guess == "g" and next_num > current) or (guess == "m" and next_num < current):
            streak += 1
            print(f"Познахте! Победна серия: {streak}")
            current = next_num
            if streak == 10:
                winnings = bet * 2
                print(f"Познахте 10 пъти! Печелите {winnings} кредита!")
                credits += winnings
                update_user_credits(username, credits)
                return credits
        else:
            print("Загуба. Ти загуби залога си.")
            update_user_credits(username, credits)
            return credits
