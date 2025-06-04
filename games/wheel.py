import pygame
import random
from account.user import update_user_credits

def play_wheel(username, credits):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Колелото на късмета")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Segoe UI", 28)
    big_font = pygame.font.SysFont("Segoe UI Black", 48, bold=True)

    wheel_sectors = [
        ("Джакпот!", 5),
        ("Голяма печалба", 3),
        ("Голяма печалба", 3),
        ("Малка печалба", 2),
        ("Малка печалба", 2),
        ("Малка печалба", 2),
        ("Минимална печалба", 1.5),
        *[("Загуба", 0)] * 24
    ]

    bet = 0
    input_text = ""
    input_mode = "bet"
    message = "Въведи залог (ENTER):"
    result = None
    result_text = ""
    winnings = 0
    finished = False
    spinning = False
    spin_ticks = 0
    spin_duration = 90
    final_sector_index = None

    def reset_game():
        nonlocal bet, input_text, input_mode, message, result, winnings, finished, spinning, spin_ticks, final_sector_index
        bet = 0
        input_text = ""
        input_mode = "bet"
        message = "Въведи залог и натисни ENTER:"
        result = None
        winnings = 0
        finished = False
        spinning = False
        spin_ticks = 0
        final_sector_index = None

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
                                credits -= bet
                                final_sector_index = random.randint(0, len(wheel_sectors) - 1)
                                spinning = True
                                input_mode = "spinning"
                                message = ""
                        except ValueError:
                            message = "Невалиден залог. Въведи число:"
                        input_text = ""

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

        screen.blit(big_font.render("Колелото на късмета", True, (255, 215, 0)), (200, 20))
        screen.blit(font.render(f"Баланс: {credits} кредита", True, (255, 255, 255)), (20, 80))
        screen.blit(font.render(message, True, (255, 255, 255)), (20, 140))

        if input_mode == "bet":
            pygame.draw.rect(screen, (255, 255, 255), (20, 180, 760, 40), border_radius=8)
            input_surface = font.render(input_text, True, (0, 0, 0))
            screen.blit(input_surface, (25, 185))

        if spinning:
            spin_ticks += 1
            current_sector = (spin_ticks + final_sector_index) % len(wheel_sectors)
            desc, _ = wheel_sectors[current_sector]
            spinning_text = big_font.render(desc, True, (255, 215, 0))
            screen.blit(spinning_text, (400 - spinning_text.get_width() // 2, 250))

            if spin_ticks >= spin_duration:
                spinning = False
                result, multiplier = wheel_sectors[final_sector_index]
                winnings = int(bet * multiplier)
                credits += winnings
                update_user_credits(username, credits)
                input_mode = "done"
                result_text = f"Резултат: {result}"
                if winnings > 0:
                    message = f"Печелиш {winnings} кредита!"
                else:
                    message = "Губиш! "

        if input_mode == "done" and result is not None:
            result_surf = font.render(result_text, True, (255, 215, 0))
            screen.blit(result_surf, (20, 240))

            win_color = (0, 255, 0) if winnings > 0 else (255, 100, 100)
            screen.blit(font.render(message, True, win_color), (20, 280))

            screen.blit(font.render("Натисни ENTER за нова игра или ESC за изход", True, (180, 180, 180)), (20, 330))

        pygame.display.flip()
        clock.tick(60)
