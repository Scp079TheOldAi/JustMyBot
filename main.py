import logging
import atexit
import sys
from telegram.ext import ApplicationBuilder
from config.config import Config
from utils.logger import setup_logger
from prestart import prestart_check
from modelloads.ModelLoads import ModuleLoader
import core.errors as core_errors

def exit_handler():
    """Функция, вызываемая при выходе из программы"""
    logger = logging.getLogger("MAIN")
    logger.info("Завершение работы программы...")
    print("\n" + "="*50)
    print("Программа завершена. Нажмите Enter для закрытия окна...")
    input()

def main():
    # Регистрируем обработчик выхода
    atexit.register(exit_handler)
    
    setup_logger()
    logger = logging.getLogger("MAIN")

    cfg = Config()
    token = cfg.bot_token

    proxies = prestart_check(token)

    logger.info("Создаём ApplicationBuilder...")

    builder = ApplicationBuilder().token(token)
    if proxies:
        builder.proxy_url = proxies[0]

    app = builder.build()
    app.add_error_handler(core_errors.global_error_handler)

    loader = ModuleLoader(app)
    loader.load_modules("modules")

    # Старт polling
    logger.info("Запуск бота...")
    
    try:
        app.run_polling()
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
