# prestart.py
import logging
import requests
from utils.proxies import load_proxies, check_proxy_list

logger = logging.getLogger("PRESTART")
TELEGRAM_API = "https://api.telegram.org"

def _check_direct(token, timeout=5):
    url = f"{TELEGRAM_API}/bot{token}/getMe"
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code == 200:
            return True, r.elapsed.total_seconds()
        return False, None
    except Exception as e:
        logger.info("Direct check failed: %s", e)
        return False, None

def prestart_check(token):
    proxies = load_proxies()
    direct_ok, direct_latency = _check_direct(token)
    if direct_ok:
        logger.info("Telegram без прокси доступен (latency=%.3fs)", direct_latency)
    else:
        logger.warning("Telegram без прокси недоступен")

    if not proxies:
        logger.info("Прокси не найдены — работаем без прокси")
        return []

    good = check_proxy_list(proxies, token, baseline_latency=direct_latency, keep_if_direct_failed=not direct_ok)
    logger.info("Найдено %d рабочих прокси", len(good))
    return good
