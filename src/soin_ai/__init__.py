from .core.manager import Soin
from .exceptions.base import SoinError, PromptNotFoundError, MissingVariableError

__version__ = "0.1.0"
__all__ = ["Soin", "SoinError", "PromptNotFoundError", "MissingVariableError"]