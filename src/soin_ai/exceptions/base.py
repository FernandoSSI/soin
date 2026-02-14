class SoinError(Exception):
    pass

class PromptNotFoundError(SoinError):
    def __init__(self, prompt_name: str, path: str):
        self.message = f"Soin could not find prompt '{prompt_name}' at: {path}"
        super().__init__(self.message)

class MissingVariableError(SoinError):
    def __init__(self, prompt_name: str, missing_vars: list):
        self.message = f"Missing required variables for '{prompt_name}': {', '.join(missing_vars)}"
        super().__init__(self.message)