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

    spin_cost = 1000  

    wheel_sectors = [
        ("🎉 Джакпот!", 10),
        ("💸 Двойна печалба!", 2),
        ("➕ Малка печалба", 1.5),
        ("➖ Минимална печалба", 1.1),
        ("0️⃣ Нищо", 0),
        ("💀 Загуба", 0),
        ("💀 Загуба", 0),
        ("💀 Загуба", 0),
        ("➖ Малка печалба", 1.2),
        ("💸 Двойна печалба!", 2),
        ("0️⃣ Нищо", 0),
        ("🎯 Голяма печалба", 5),
    ]

    message = ""
    spinning = False
    spin_ticks = 0
    spin_duration = 120 
    result_desc = ""
    result_multiplier = 0
    finished = False

    while True:
        screen.fill((10, 10, 40))

        title = big_font.render("Колелото на късмета", True, (255, 215, 0))
        screen.blit(title, (400 - title.get_width() // 2, 30))

        credits_surf = font.render(f"Кредити: {credits}", True, (255, 255, 255))
        screen.blit(credits_surf, (20, 100))

        cost_surf = font.render(f"Цена за завъртане: {spin_cost} кредита", True, (255, 255, 255))
        screen.blit(cost_surf, (20, 140))

        if not spinning and not finished:
            if credits < spin_cost:
                message = "Нямате достатъчно кредити за завъртане!"
                msg_color = (255, 100, 100)
            else:
                message = "Натиснете ENTER, за да завъртите колелото. "
                msg_color = (255, 255, 255)

            message_surf = font.render(message, True, msg_color)
            screen.blit(message_surf, (400 - message_surf.get_width() // 2, 220))

        elif spinning:
            spin_ticks += 1
            current_sector = wheel_sectors[spin_ticks % len(wheel_sectors)]
            desc, multiplier = current_sector

            spin_text = big_font.render(desc, True, (255, 215, 0))
            screen.blit(spin_text, (400 - spin_text.get_width() // 2, 220))

            if spin_ticks >= spin_duration:
                spinning = False
                result_desc = desc
                result_multiplier = multiplier
                finished = True
                winnings = int(spin_cost * multiplier)
                if winnings > 0:
                    message = f"Печелите {winnings} кредита! 🎉"
                else:
                    message = "За съжаление, загуба. Опитайте пак."
                credits += winnings
                update_user_credits(username, credits)

        else:
            result_surf = big_font.render(result_desc, True, (255, 215, 0))
            screen.blit(result_surf, (400 - result_surf.get_width() // 2, 220))

            message_surf = font.render(message, True, (255, 255, 255))
            screen.blit(message_surf, (400 - message_surf.get_width() // 2, 300))

            prompt = font.render("Натиснете ENTER за ново завъртане или ESC за връщане", True, (180, 180, 180))
            screen.blit(prompt, (400 - prompt.get_width() // 2, 550))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return credits
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return credits  
                if event.key == pygame.K_RETURN:
                    if finished:
                        if credits < spin_cost:
                            message = "Нямате достатъчно кредити за завъртане!"
                            finished = False
                        else:
                            credits -= spin_cost
                            spinning = True
                            spin_ticks = 0
                            finished = False
                    elif not spinning:
                        if credits >= spin_cost:
                            credits -= spin_cost
                            spinning = True
                            spin_ticks = 0

        pygame.display.flip()
        clock.tick(60)
