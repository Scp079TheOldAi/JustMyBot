from telegram.error import TelegramError, BadRequest, Forbidden, RetryAfter, Conflict
import traceback
import logging

logger = logging.getLogger("bot_error_handler")

def format_error(update, error: Exception):
    """Создаёт читаемый текст ошибки."""
    user = None
    if update and update.effective_user:
        user = f"{update.effective_user.id} ({update.effective_user.full_name})"

    return (
        f"⚠ Ошибка!\n"
        f"Пользователь: {user}\n"
        f"Тип: {type(error).__name__}\n"
        f"Описание: {error}\n"
    )


async def global_error_handler(update, context):
    error = context.error
    text = format_error(update, error)

    logger.error(text)
    logger.error("Full traceback:\n" + "".join(traceback.format_exception(None, error, error.__traceback__)))

    # ------ Специализированные ошибки -------
    if isinstance(error, RetryAfter):
        wait = error.retry_after
        logger.warning(f"Flood control: ждём {wait} секунд")
        await asyncio.sleep(wait)
        return

    if isinstance(error, BadRequest):
        return  # тихо игнорим

    if isinstance(error, Forbidden):
        return  # бот заблокирован — игнор

    if isinstance(error, Conflict):
        logger.error("⚠ Бот запущен в нескольких процессах одновременно!")
        return

    # -------- На все остальные ошибки отправляем сообщение пользователю -------
    try:
        if update and update.effective_message:
            await update.effective_message.reply_text("⚠ Произошла ошибка. Уже разбираюсь…")
    except:
        pass
