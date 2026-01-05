# modelloads/ModelLoads.py
import importlib
import os
import logging
import threading
from watchdog import watch_modules
from core.module_guard import is_valid_module

logger = logging.getLogger('MODELLOADS')

class ModuleLoader:
    def __init__(self, dispatcher):
        self.dp = dispatcher
        # mapping module_name -> list of handler objects added by module
        self.module_handlers = {}

    def load_modules(self, folder):
        if not os.path.exists(folder):
            logger.error('Modules folder not found: %s', folder)
            return
        for f in os.listdir(folder):
            if not f.endswith('.py'):
                continue
            name = f[:-3]
            self._load_module(name, folder)

        # start watchdog thread to monitor changes
        t = threading.Thread(target=watch_modules, args=(folder, self.reload_module), daemon=True)
        t.start()

    def _load_module(self, name, folder):
        module_path = f"{folder}.{name}" if '.' not in name else name
        try:
            module = importlib.import_module(module_path)
            importlib.reload(module)
            if hasattr(module, 'setup'):
                handlers = module.setup(self.dp)
                # some modules may return handlers they added; if not, store empty list
                self.module_handlers[name] = handlers or []
                logger.info('Module %s loaded', name)
            else:
                logger.warning('Module %s has no setup(dp)', name)
        except Exception as e:
            logger.exception('Failed to load module %s: %s', name, e)
            self._write_error_file(name, e)

    def reload_module(self, name):
        logger.info('Reloading module: %s', name)
        try:
            # remove old handlers if we tracked them
            old = self.module_handlers.get(name, [])
            for h in old:
                try:
                    self.dp.remove_handler(h)
                except Exception:
                    # older PTB versions may not support remove by object for some handler types
                    try:
                        self.dp.remove_handler(h, group=0)
                    except Exception:
                        pass
            # re-import and setup
            module_path = f"modules.{name}"
            module = importlib.import_module(module_path)
            importlib.reload(module)
            handlers = module.setup(self.dp)
            self.module_handlers[name] = handlers or []
            logger.info('Module %s reloaded successfully', name)
        except Exception as e:
            logger.exception('Error reloading module %s: %s', name, e)
            self._write_error_file(name, e)

    def _write_error_file(self, module_name, exc):
        os.makedirs('modelloads/errors', exist_ok=True)
        with open(f'modelloads/errors/{module_name}_error.txt', 'w', encoding='utf-8') as f:
            f.write(str(exc))
