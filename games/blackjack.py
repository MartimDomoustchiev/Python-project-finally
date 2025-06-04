import pygame
import random
from account.user import update_user_credits

def play_blackjack(username, credits):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Segoe UI", 26)
    big_font = pygame.font.SysFont("Segoe UI Black", 48, bold=True)

    suits = ['♠', '♥', '♦', '♣']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def card_value(card):
        rank = card[0]
        if rank in ['J', 'Q', 'K']:
            return 10
        elif rank == 'A':
            return 11
        else:
            return int(rank)

    def hand_value(hand):
        value = sum(card_value(card) for card in hand)
        aces = sum(1 for card in hand if card[0] == 'A')
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    deck = [r + s for r in ranks for s in suits]
    random.shuffle(deck)

    status = "Въведи залог (ENTER):"
    input_text = ""
    bet = 0
    input_mode = "bet"
    player_hand = []
    dealer_hand = []
    result_msg = ""
    game_over = False

    while True:
        screen.fill((20, 10, 30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return credits

                if input_mode == "bet":
                    if event.key == pygame.K_RETURN:
                        try:
                            bet = int(input_text)
                            if bet <= 0 or bet > credits:
                                status = "Невалиден залог. Въведи отново:"
                                input_text = ""
                            else:
                                credits -= bet
                                player_hand = [deck.pop(), deck.pop()]
                                dealer_hand = [deck.pop()]
                                status = "Натисни H за Хит, S за Стенд"
                                input_text = ""
                                input_mode = "play"
                        except:
                            status = "Въведи валидно число:"
                            input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        if event.unicode.isdigit():
                            input_text += event.unicode

                elif input_mode == "play":
                    if not game_over:
                        if event.key == pygame.K_h:
                            player_hand.append(deck.pop())
                            if hand_value(player_hand) > 21:
                                result_msg = "Преброи: " + str(hand_value(player_hand)) + ". Загуба!"
                                game_over = True
                                status = "Натисни ENTER за нова игра или ESC за изход."
                        elif event.key == pygame.K_s:
                            while hand_value(dealer_hand) < 17:
                                dealer_hand.append(deck.pop())
                            player_score = hand_value(player_hand)
                            dealer_score = hand_value(dealer_hand)
                            if dealer_score > 21 or player_score > dealer_score:
                                winnings = bet * 2
                                credits += winnings
                                result_msg = f"Победа! Ти: {player_score}, Дилър: {dealer_score}. Спечели {winnings} кредита!"
                            elif dealer_score == player_score:
                                credits += bet
                                result_msg = f"Равенство! Ти: {player_score}, Дилър: {dealer_score}. Връщаш залога."
                            else:
                                result_msg = f"Загуба! Ти: {player_score}, Дилър: {dealer_score}."
                            game_over = True
                            status = "Натисни ENTER за нова игра или ESC за изход."
                    else:
                        if event.key == pygame.K_RETURN:
                            deck.extend(player_hand + dealer_hand)
                            random.shuffle(deck)
                            status = "Въведи залог (ENTER):"
                            input_text = ""
                            bet = 0
                            player_hand = []
                            dealer_hand = []
                            result_msg = ""
                            game_over = False
                            input_mode = "bet"

        screen.blit(big_font.render("Blackjack", True, (255, 215, 0)), (300, 20))
        screen.blit(font.render(f"Баланс: {credits} кредита", True, (255, 255, 255)), (20, 80))
        screen.blit(font.render(status, True, (255, 255, 255)), (20, 140))

        def draw_hand(hand, y):
            x = 20
            for card in hand:
                pygame.draw.rect(screen, (255, 255, 255), (x, y, 50, 70), border_radius=8)
                card_text = font.render(card, True, (0, 0, 0))
                screen.blit(card_text, (x + 10, y + 20))
                x += 60

        draw_hand(player_hand, 400)
        draw_hand(dealer_hand, 300)

        if input_mode == "bet":
            pygame.draw.rect(screen, (255, 255, 255), (20, 180, 760, 40), border_radius=8)
            input_surface = font.render(input_text, True, (0, 0, 0))
            screen.blit(input_surface, (25, 185))

        if result_msg:
            screen.blit(font.render(result_msg, True, (50, 205, 50)), (20, 230))

        pygame.display.flip()
        clock.tick(60)
