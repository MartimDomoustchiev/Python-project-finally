### Python Casino Game Project ###

Това е финален проект, разработен на Python от Martin Domoustchiev and Denislav Maksimov, представляващ **казино приложение с няколко мини игри**, потребителска регистрация и управление на кредити.



## Предлагани игри

- **Рулетка (Roulette)**
- **Blackjack**
- **Колело на късмета (Wheel)**
- **Слот машина (Slot)**
- **High & Low**



## Функционалности

- Регистрация на потребители
- Вход със запазена парола
- Начален баланс: `5000 кредита`
- Управление на баланса (добавяне, изваждане)
- Игри, в които се залагат кредити
- Проверка и обновяване на кредити



## Структура на проекта

Python-project-finally/
- main.py                # Главен файл за стартиране на приложението
- requirements.txt       # Зависимости за проекта
- users.txt              # Файл с регистрирани потребители

- account/               # Управление на потребителите и техните финанси
  - __init__.py
  - account.py
  - user.py
  - wallet.py

- games/                 # Реализация на казино игрите
  - __init__.py
  - roulette.py
  - highlow.py
  - blackjack.py
  - wheel.py
  - slot.py

- ui/                    # Потребителски интерфейс
  - __init__.py
  - simple_ui.py

- tests/                 # Pytest тестове
  - __init__.py
  - test_games.py

- README.md              # Описание на проекта



## Тестване

Проектът съдържа unit тестове с помощта на **pytest**.
За да стартираш тестовете:

```bash
pytest tests/test_games.py



## Стартиране

python main.py
Инсталирай нужните зависимости с: pip install -r requirements.txt

