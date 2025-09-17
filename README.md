# Тестовое задание для компаний: Для каждой компании определенна собственная ветка


# My Game App (FastAPI)

Приложение для работы с игроками, бустами и наградами.

## Функционал
- Ежедневный вход игрока с начислением очков
- Выдача игровых бустов вручную или автоматически
- Выдача призов за прохождение уровней
- Экспорт данных о прохождении уровней в CSV (streaming, подходит для больших данных)


## Установка

```bash
git clone <repo>
cd my_game_app
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
pip install fastapi uvicorn sqlalchemy
```

## Запуск

```bash
uvicorn main:app --reload
```
