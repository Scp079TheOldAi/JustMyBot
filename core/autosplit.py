# core/autosplit.py
def smart_reply(update, text):
    if update is None or getattr(update, 'effective_message', None) is None:
        return
    msg = update.effective_message
    if not isinstance(text, str):
        text = str(text)
    max_len = 4096
    if len(text) <= max_len:
        try:
            msg.reply_text(text)
            return
        except Exception:
            pass
    # split by max_len
    for i in range(0, len(text), max_len):
        try:
            msg.reply_text(text[i:i+max_len])
        except Exception:
            pass
