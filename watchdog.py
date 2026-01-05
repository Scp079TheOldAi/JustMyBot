# watchdog.py
import os
import time
import logging

logger = logging.getLogger("WATCHDOG")

def watch_modules(folder, on_change, poll_interval=1.0):
    """
    Наблюдение за папкой модулей. При изменении файла вызывает on_change(module_name)
    """
    mtimes = {}
    while True:
        try:
            time.sleep(poll_interval)
            if not os.path.exists(folder):
                continue
            for f in os.listdir(folder):
                if not f.endswith('.py'):
                    continue
                path = os.path.join(folder, f)
                try:
                    mtime = os.path.getmtime(path)
                except FileNotFoundError:
                    continue
                prev = mtimes.get(f)
                if prev is None:
                    mtimes[f] = mtime
                    continue
                if mtime != prev:
                    mtimes[f] = mtime
                    module_name = f[:-3]
                    logger.info("Change detected in module: %s", module_name)
                    try:
                        on_change(module_name)
                    except Exception as e:
                        logger.exception("Error while reloading module %s: %s", module_name, e)
        except Exception as e:
            logger.exception("Watchdog loop error: %s", e)
