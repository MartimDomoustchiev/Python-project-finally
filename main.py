from colorama import init
init(autoreset=True)

from account.user import login, register, get_user_credits
from games.roulette import play_roulette
from games.highlow import play_highlow
from games.blackjack import play_blackjack
from games.wheel import play_wheel
from games.slot import play_slot


import pygame
from ui.simple_ui import main_menu

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Казино Приложение")
main_menu(screen)
pygame.quit()

def main():
    print("Добре дошли в КАЗИНОТО!")
    while True:
        choice = input("1. Регистрация\n2. Вход\n3. Изход\nИзбор: ")
        if choice == "1":
            register()
        elif choice == "2":
            username = login()
            if username:
                credits = get_user_credits(username)
                while True:
                    print("\n--- Меню Игри ---")
                    print("1. Рулетка")
                    print("2. High-Low")
                    print("3. Blackjack")
                    print("4. Колело на късмета")
                    print("5. Машинки")
                    print("6. Изход")
                    game_choice = input("Избери игра: ")
                    if game_choice == "1":
                        credits = play_roulette(username, credits)
                    elif game_choice == "2":
                        credits = play_highlow(username, credits)
                    elif game_choice == "3":
                        credits = play_blackjack(username, credits)
                    elif game_choice == "4":
                        credits = play_wheel(username, credits)
                    elif game_choice == "5":
                        credits = play_slot(username, credits)
                    elif game_choice == "6":
                        break
                    else:
                        print("Невалиден избор.")
            else:
                print("Грешен вход.")
        elif choice == "3":
            print("Довиждане!")
            break
        else:
            print("Невалиден избор.")

if __name__ == "__main__":
    main()
