import pygame
from account.user import login, register, get_user_credits, update_user_credits
from ui.simple_ui import draw_button
from games.roulette import play_roulette
from games.highlow import play_highlow
from games.blackjack import play_blackjack
from games.wheel import play_wheel
from games.slot import play_slot

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Казино Приложение")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Segoe UI", 32)
TITLE_FONT = pygame.font.SysFont("Segoe UI Black", 64, bold=True)

current_user = None
credits = 0

def input_screen(prompt):
    input_text = ""
    active = True
    font = pygame.font.SysFont("Segoe UI", 28)

    while active:
        screen.fill((10, 10, 40))
        prompt_surf = font.render(prompt, True, (255, 215, 0))
        screen.blit(prompt_surf, (100, 150))

        input_rect = pygame.Rect(100, 200, 600, 40)
        pygame.draw.rect(screen, (255, 255, 255), input_rect, 2, border_radius=8)
        input_surf = font.render(input_text, True, (255, 255, 255))
        screen.blit(input_surf, (input_rect.x + 10, input_rect.y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text.strip():
                        return input_text.strip()
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 20:
                        input_text += event.unicode

        pygame.display.flip()
        clock.tick(60)

def login_screen():
    global current_user, credits
    while True:
        screen.fill((10, 10, 40))
        title_surf = TITLE_FONT.render("Вход", True, (255, 215, 0))
        screen.blit(title_surf, (400 - title_surf.get_width() // 2, 50))

        username = input_screen("Въведи потребителско име:")
        password = input_screen("Въведи парола:")

        if login(username, password):
            current_user = username
            credits = get_user_credits(current_user)
            return True
        else:
            error_font = pygame.font.SysFont("Segoe UI", 24)
            error_surf = error_font.render("Грешно потребителско име или парола! Опитай пак.", True, (255, 0, 0))
            screen.blit(error_surf, (400 - error_surf.get_width() // 2, 300))
            pygame.display.flip()
            pygame.time.wait(1500)  

def register_screen():
    global current_user, credits
    while True:
        screen.fill((10, 10, 40))
        title_surf = TITLE_FONT.render("Регистрация", True, (255, 215, 0))
        screen.blit(title_surf, (400 - title_surf.get_width() // 2, 50))

        username = input_screen("Избери потребителско име:")
        password = input_screen("Избери парола:")

        if register(username, password):
            current_user = username
            credits = get_user_credits(current_user)
            return True
        else:
            error_font = pygame.font.SysFont("Segoe UI", 24)
            error_surf = error_font.render("Потребителското име е заето! Опитай друго.", True, (255, 0, 0))
            screen.blit(error_surf, (400 - error_surf.get_width() // 2, 300))
            pygame.display.flip()
            pygame.time.wait(1500)

def main_menu():
    global credits, current_user
    running = True

    while running:
        screen.fill((20, 30, 50))
        title = TITLE_FONT.render("КАЗИНО", True, (255, 215, 0))
        screen.blit(title, (400 - title.get_width() // 2, 50))

        if current_user:
            user_text = FONT.render(f"Потребител: {current_user} | Кредити: {credits}", True, (255, 255, 255))
            screen.blit(user_text, (20, 150))

        buttons = [
            ("Рулетка", lambda: play_game(play_roulette)),
            ("High-Low", lambda: play_game(play_highlow)),
            ("Blackjack", lambda: play_game(play_blackjack)),
            ("Колело", lambda: play_game(play_wheel)),
            ("Машинки", lambda: play_game(play_slot)),
            ("Изход", exit_game)
        ]

        for i, (label, action) in enumerate(buttons):
            if draw_button(screen, label, (400, 220 + i * 70)):
                action()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

        pygame.display.flip()
        clock.tick(60)

def play_game(game_func):
    global credits
    credits = game_func(current_user, credits)
    update_user_credits(current_user, credits)

def exit_game():
    pygame.quit()
    exit()

if __name__ == "__main__":
    while True:
        screen.fill((10, 10, 40))
        title = TITLE_FONT.render("Добре дошъл в Казино!", True, (255, 215, 0))
        screen.blit(title, (400 - title.get_width() // 2, 100))

        if draw_button(screen, "Вход", (400, 250), FONT):
            if login_screen():
                main_menu()
        if draw_button(screen, "Регистрация", (400, 330), FONT):
            if register_screen():
                main_menu()
        if draw_button(screen, "Изход", (400, 410), FONT):
            exit_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()

        pygame.display.flip()
        clock.tick(60)
