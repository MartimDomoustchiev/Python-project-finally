import pygame
import random
from account.user import update_user_credits

def play_highlow(username, credits):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Segoe UI", 28)
    big_font = pygame.font.SysFont("Segoe UI Black", 48, bold=True)

    status = "Въведи залог (ENTER):"
    input_text = ""
    bet = 0
    streak = 0
    input_mode = "bet"
    current = None
    result_msg = ""

    while True:
        screen.fill((15, 70, 30))
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
                                streak = 0
                                current = random.randint(1, 50)
                                status = f"Текущо число: {current}. По-голямо (g) или по-малко (m)?"
                                input_text = ""
                                input_mode = "guess"
                        except:
                            status = "Въведи валидно число:"
                            input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        if event.unicode.isdigit():
                            input_text += event.unicode

                elif input_mode == "guess":
                    guess = event.unicode.lower()
                    if guess in ['g', 'm']:
                        next_num = random.randint(1, 50)
                        correct = (guess == 'g' and next_num > current) or (guess == 'm' and next_num < current)
                        if correct:
                            streak += 1
                            current = next_num
                            result_msg = f"Поздравления! Следващо число: {next_num} | Серия: {streak}"
                            if streak == 10:
                                winnings = bet * 25
                                credits += winnings
                                update_user_credits(username, credits)
                                status = f"Победа! Спечели {winnings} кредита! Натисни ENTER за нова игра или ESC за изход."
                                input_mode = "done"
                        else:
                            result_msg = f"Загуба! Следващо число: {next_num}. Загуби залога си."
                            update_user_credits(username, credits)
                            status = "Натисни ENTER за нова игра или ESC за изход."
                            input_mode = "done"
                    else:
                        status = "Избери 'g' или 'm'!"

                elif input_mode == "done":
                    if event.key == pygame.K_RETURN:
                        status = "Въведи залог (ENTER):"
                        input_text = ""
                        result_msg = ""
                        input_mode = "bet"

        screen.blit(big_font.render("High-Low", True, (255, 215, 0)), (400 - 120, 20))
        screen.blit(font.render(f"Баланс: {credits} кредита", True, (255, 255, 255)), (20, 80))
        screen.blit(font.render(status, True, (255, 255, 255)), (20, 140))
        pygame.draw.rect(screen, (255, 255, 255), (20, 180, 760, 40), border_radius=8)
        input_surface = font.render(input_text, True, (0, 0, 0))
        screen.blit(input_surface, (25, 185))
        if result_msg:
            screen.blit(font.render(result_msg, True, (50, 205, 50)), (20, 230))

        pygame.display.flip()
        clock.tick(60)
