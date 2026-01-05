# modelloads/CommandError.py
def command_error(command, error):
    try:
        return f"Попытка вызова команды безуспешно ({command}). Ошибка: {error}"
    except Exception:
        return "Ошибка при выполнении команды."
