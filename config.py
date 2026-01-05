# config/config.py
import json
import os
import sys
import logging

logger = logging.getLogger("CONFIG")

CONFIG_DIR = os.path.dirname(__file__)
SESSION_FILE = os.path.join(CONFIG_DIR, "session.json")
PID_FILE = os.path.join(CONFIG_DIR, "session.pid")

class Config:
    def __init__(self):
        self.bot_token = None
        os.makedirs(CONFIG_DIR, exist_ok=True)
        self._load_or_ask()

    def _load_or_ask(self):
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                token = data.get("token")
                pid = data.get("pid")
                if token:
                    if pid and self._is_process_alive(pid):
                        logger.error("Найден процесс с PID=%s — сессия занята.", pid)
                        sys.exit("Сессия уже используется. Удалите session.json или завершите процесс.")
                    self.bot_token = token
                    self._write_pid()
                    return
            except Exception as e:
                logger.warning("Не удалось прочитать session.json: %s", e)

        while True:
            token = input("Введите BOT TOKEN: ").strip()
            if token:
                self.bot_token = token
                self._save_session()
                self._write_pid()
                break
            else:
                print("Токен не может быть пустым.")

    def _save_session(self):
        try:
            with open(SESSION_FILE, "w", encoding="utf-8") as f:
                json.dump({"token": self.bot_token, "timestamp": int(__import__('time').time())}, f, indent=2)
        except Exception as e:
            logger.exception("Не удалось сохранить session.json: %s", e)

    def _write_pid(self):
        try:
            pid = os.getpid()
            with open(PID_FILE, "w", encoding='utf-8') as f:
                f.write(str(pid))
        except Exception:
            pass

    def _is_process_alive(self, pid):
        try:
            pid = int(pid)
            import os
            if os.name == 'nt':
                # Windows: попытка os.kill(pid, 0) может привести к PermissionError, handle generically
                import ctypes
                PROCESS_QUERY_INFORMATION = 0x0400
                handle = ctypes.windll.kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, 0, pid)
                if handle:
                    ctypes.windll.kernel32.CloseHandle(handle)
                    return True
                return False
            else:
                os.kill(pid, 0)
                return True
        except Exception:
            return False
