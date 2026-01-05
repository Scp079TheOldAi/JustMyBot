# core/module_guard.py
import importlib
import logging

logger = logging.getLogger('MODULE_GUARD')

def is_valid_module(module_path):
    try:
        module = importlib.import_module(module_path)
        return hasattr(module, 'setup')
    except Exception as e:
        logger.debug("Module validation error for %s: %s", module_path, e)
        return False
