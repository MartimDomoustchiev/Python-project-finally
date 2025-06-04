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
    message = ""
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

        title = big_font.render("Рулетка", True, (255, 215, 0))
        screen.blit(title, (400 - title.get_width() // 2, 30))

        credits_surf = font.render(f"Кредити: {credits}", True, (255, 255, 255))
        screen.blit(credits_surf, (20, 100))

        msg_color = (255, 255, 255)
        if "Невалиден" in message or "недостатъчно" in message:
            msg_color = (255, 100, 100)
        message_surf = font.render(message, True, msg_color)
        screen.blit(message_surf, (400 - message_surf.get_width() // 2, 180))

        if input_mode in ("bet", "choice"):
            input_label = "Залог: " if input_mode == "bet" else "Избор (r / b / 0-36): "
            input_display = font.render(input_label + input_text, True, (255, 255, 255))
            screen.blit(input_display, (100, 230))

        if finished and result is not None:
            color_emoji = "🟢"
            if result in red_numbers:
                color_emoji = "🔴"
            elif result in black_numbers:
                color_emoji = "⚫"

            result_text = f"Резултат: {result} {color_emoji}"
            result_surf = big_font.render(result_text, True, (255, 215, 0))
            screen.blit(result_surf, (400 - result_surf.get_width() // 2, 300))

            win_text = "Печелите! 🎉" if win else "Губите! 😞"
            win_surf = font.render(win_text, True, (0, 255, 0) if win else (255, 100, 100))
            screen.blit(win_surf, (400 - win_surf.get_width() // 2, 380))

            prompt = font.render("Натиснете ENTER за нова игра или ESC за изход", True, (180, 180, 180))
            screen.blit(prompt, (400 - prompt.get_width() // 2, 550))

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
                                message = "Залогът трябва да е положително число."
                                input_text = ""
                            elif bet_val > credits:
                                message = "Нямате достатъчно кредити за този залог."
                                input_text = ""
                            else:
                                bet = bet_val
                                input_mode = "choice"
                                input_text = ""
                                message = "Изберете: r(червено), b(черно) или число 0-36 и натиснете ENTER"
                        except ValueError:
                            message = "Въведи валиден залог (число)."
                            input_text = ""

                    elif input_mode == "choice":
                        ch = input_text.strip().lower()
                        valid = ch in ['r', 'b'] or (ch.isdigit() and 0 <= int(ch) <= 36)
                        if not valid:
                            message = "Невалиден избор. Опитайте пак."
                            input_text = ""
                        else:
                            choice = ch
                            result = random.randint(0, 36)
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
                                win = False
                                credits -= bet
                            update_user_credits(username, credits)
                            finished = True
                            input_mode = "result"

                    elif input_mode == "result":
                        if credits <= 0:
                            message = "Нямате кредити за игра."
                            return credits
                        else:
                            reset_game()

                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if input_mode in ("bet", "choice"):
                        if len(input_text) < 5:
                            input_text += event.unicode

        pygame.display.flip()
        clock.tick(60)
