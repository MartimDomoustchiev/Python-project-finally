import pygame
import random
from account.user import update_user_credits

def play_roulette(username, credits):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Рулетка")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Segoe UI", 28)
    big_font = pygame.font.SysFont("Segoe UI Black", 48, bold=True)

    red_numbers = {
        1, 3, 5, 7, 9, 12, 14, 16, 18,
        19, 21, 23, 25, 27, 30, 32, 34, 36
    }
    black_numbers = {
        2, 4, 6, 8, 10, 11, 13, 15, 17,
        20, 22, 24, 26, 28, 29, 31, 33, 35
    }

    bet = 0
    choice = None
    input_text = ""
    input_mode = "bet"
    message = "Въведи залог (ENTER):"
    result = None
    win = False
    finished = False

    def reset_game():
        nonlocal bet, choice, input_text, input_mode, message, result, win, finished
        bet = 0
        choice = None
        input_text = ""
        input_mode = "bet"
        message = "Въведи залог (ENTER):"
        result = None
        win = False
        finished = False

    reset_game()

    while True:
        screen.fill((10, 10, 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return credits

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return credits

                if event.key == pygame.K_RETURN:
                    if input_mode == "bet":
                        try:
                            bet_val = int(input_text)
                            if bet_val <= 0:
                                message = "Залогът трябва да е положително число:"
                            elif bet_val > credits:
                                message = "Недостатъчно кредити:"
                            else:
                                bet = bet_val
                                input_mode = "choice"
                                message = "Избери: r (червено), b (черно), 0-36:"
                            input_text = ""
                        except ValueError:
                            message = "Невалиден залог. Въведи число:"
                            input_text = ""

                    elif input_mode == "choice":
                        ch = input_text.strip().lower()
                        valid = ch in ['r', 'b'] or (ch.isdigit() and 0 <= int(ch) <= 36)
                        if not valid:
                            message = "Невалиден избор. Опитай пак:"
                            input_text = ""
                        else:
                            choice = ch
                            result = random.randint(0, 36)
                            if choice == 'r' and result in red_numbers:
                                win = True
                                credits += bet * 0.5
                            elif choice == 'b' and result in black_numbers:
                                win = True
                                credits += bet * 0.5
                            elif choice.isdigit() and int(choice) == result:
                                win = True
                                credits += bet * 18
                            else:
                                win = False
                                credits -= bet
                            update_user_credits(username, credits)
                            input_mode = "done"

                    elif input_mode == "done":
                        if credits <= 0:
                            message = "Нямаш кредити."
                            return credits
                        else:
                            reset_game()

                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 6:
                        input_text += event.unicode

        # Рендеринг
        screen.blit(big_font.render("Рулетка", True, (255, 215, 0)), (300, 20))
        screen.blit(font.render(f"Баланс: {credits} кредита", True, (255, 255, 255)), (20, 80))
        screen.blit(font.render(message, True, (255, 255, 255)), (20, 140))

        # Входно поле
        pygame.draw.rect(screen, (255, 255, 255), (20, 180, 760, 40), border_radius=8)
        input_surface = font.render(input_text, True, (0, 0, 0))
        screen.blit(input_surface, (25, 185))

        # Резултати
        if input_mode == "done" and result is not None:
            color_emoji = "🟢"
            if result in red_numbers:
                color_emoji = "🔴"
            elif result in black_numbers:
                color_emoji = "⚫"
            result_text = f"Резултат: {result} {color_emoji}"
            screen.blit(font.render(result_text, True, (255, 215, 0)), (20, 240))

            win_text = "Печелиш! 🎉" if win else "Губиш!"
            win_color = (0, 255, 0) if win else (255, 100, 100)
            screen.blit(font.render(win_text, True, win_color), (20, 280))

            screen.blit(font.render("Натисни ENTER за нова игра или ESC за изход", True, (180, 180, 180)), (20, 330))

        pygame.display.flip()
        clock.tick(60)
