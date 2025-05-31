import random
from account.user import update_user_credits

def deal_card():
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]  
    return random.choice(cards)

def calculate_score(hand):
    score = sum(hand)
    if 11 in hand and score > 21:
        hand[hand.index(11)] = 1
        score = sum(hand)
    return score

def display_hand(player, hand):
    print(f"{player} карти: {hand} | Точки: {calculate_score(hand)}")

def play_blackjack(username, credits):
    print("Играеш: Блекджек")
    try:
        bet = int(input("Залог: "))
        if bet <= 0 or bet > credits:
            print("Невалиден залог.")
            return credits
    except ValueError:
        print("Въведи валидна сума.")
        return credits

    player_hand = [deal_card(), deal_card()]
    dealer_hand = [deal_card(), deal_card()]
    
    game_over = False

    while not game_over:
        display_hand("Ти", player_hand)
        print(f"Карта на дилъра: [{dealer_hand[0]}, ?]")

        if calculate_score(player_hand) == 21:
            print("BLACKJACK! Печелите 1.5x!")
            credits += int(bet * 1.5)
            update_user_credits(username, credits)
            return credits

        choice = input("[h] Вземи карта  |  [s] Спри: ").lower()
        if choice == 'h':
            player_hand.append(deal_card())
            if calculate_score(player_hand) > 21:
                display_hand("Ти", player_hand)
                print("Загуби! Губиш залога.")
                credits -= bet
                update_user_credits(username, credits)
                return credits
        elif choice == 's':
            game_over = True
        else:
            print("Невалиден избор.")

    while calculate_score(dealer_hand) < 17:
        dealer_hand.append(deal_card())

    print()
    display_hand("Ти", player_hand)
    display_hand("Дилър", dealer_hand)

    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)

    if dealer_score > 21 or player_score > dealer_score:
        print("Печелите!")
        credits += bet
    elif player_score == dealer_score:
        print("Равенство. Връщаш си залога.")
    else:
        print("Загуби.")
        credits -= bet

    update_user_credits(username, credits)
    return credits
