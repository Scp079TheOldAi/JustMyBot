Полный проект Telegram-бота (python-telegram-bot 13.15)

Структура:
- main.py        : Запуск бота
- prestart.py    : Проверки (telegram доступ, прокси)
- watchdog.py    : Автоперезагрузка модулей при изменениях
- core/          : Ядро (errors, safe executor, autosplit, module guard)
- config/        : config/config.py (запрос токена, защита сессии)
- utils/         : proxies, logger, rate_limit
- modelloads/    : загрузчик модулей + CommandError
- modules/       : пример модулей (echo, admin, fun)
- items/proxie/  : proxie.txt (файл прокси)
- logs/          : место для логов

Запуск:
1) Установи зависимости: pip install -r requirements.txt
2) Запусти: python main.py
3) Введи токен при первом запуске (config/session.json создастся)
