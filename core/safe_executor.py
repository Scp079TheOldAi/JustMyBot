import asyncio
import logging

logger = logging.getLogger("SAFE_EXECUTOR")

async def safe_call(func, *args, **kwargs):
    try:
        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        else:
            return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Ошибка в safe_call: {e}", exc_info=True)
