import pygame
import random
from account.user import update_user_credits

def play_slot(username, credits):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Segoe UI", 28)
    big_font = pygame.font.SysFont("Segoe UI Black", 48, bold=True)

    symbols = ['1', '3', '5', '7', '9']
    status = "Въведи залог (ENTER):"
    input_text = ""
    bet = 0
    input_mode = "bet"
    result_msg = ""

    while True:
        screen.fill((40, 0, 60))
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
                                reels = [random.choice(symbols) for _ in range(3)]
                                if reels[0] == reels[1] == reels[2]:
                                    winnings = bet * 15
                                    credits += winnings
                                    result_msg = f"Печеливша серия! Спечели {winnings} кредита!"
                                else:
                                    winnings = 0
                                    result_msg = f"Резултат: {' '.join(reels)}. Загуба."
                                update_user_credits(username, credits)
                                status = "Натисни ENTER за нова игра или ESC за изход."
                                input_mode = "done"
                        except:
                            status = "Въведи валидно число:"
                            input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        if event.unicode.isdigit():
                            input_text += event.unicode

                elif input_mode == "done":
                    if event.key == pygame.K_RETURN:
                        status = "Въведи залог (ENTER):"
                        input_text = ""
                        result_msg = ""
                        input_mode = "bet"

        screen.blit(big_font.render("Слот машини", True, (255, 215, 0)), (300, 20))
        screen.blit(font.render(f"Баланс: {credits} кредита", True, (255, 255, 255)), (20, 80))
        screen.blit(font.render(status, True, (255, 255, 255)), (20, 140))

        pygame.draw.rect(screen, (255, 255, 255), (20, 180, 760, 40), border_radius=8)
        input_surface = font.render(input_text, True, (0, 0, 0))
        screen.blit(input_surface, (25, 185))

        if result_msg:
            screen.blit(font.render(result_msg, True, (50, 205, 50)), (20, 230))

        pygame.display.flip()
        clock.tick(60)
