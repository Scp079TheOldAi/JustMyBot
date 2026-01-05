# core/runtime.py
# Runtime state holder (можно расширять)
class RuntimeState:
    def __init__(self):
        self.modules = {}

runtime = RuntimeState()
