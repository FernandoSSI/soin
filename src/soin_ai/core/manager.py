import yaml
from pathlib import Path
from jinja2 import Environment, StrictUndefined
from typing import Any, Dict
from pydantic import create_model

from ..models.prompt import PromptModel
from ..exceptions.base import PromptNotFoundError, MissingVariableError

class Soin:
    def __init__(self, path: str):
        self.base_path = Path(path)
        if not self.base_path.exists():
            raise FileNotFoundError(f"Prompt directory not found: {path}")

        self._type_registry: Dict[str, Any] = {
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
            "list": list,
            "dict": dict,
            "any": Any
        }
        
        self.env = Environment(undefined=StrictUndefined)

    def register_type(self, name: str, python_type: Any):
        self._type_registry[name] = python_type

    def _load_prompt(self, prompt_name: str) -> PromptModel:
        file_path = self.base_path / f"{prompt_name}.yaml"
        if not file_path.exists():
            raise PromptNotFoundError(prompt_name, str(self.base_path))

        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return PromptModel(**data)

    def _validate_inputs(self, prompt_data: PromptModel, inputs: Dict[str, Any]):
        if not prompt_data.input_vars:
            return

        if isinstance(prompt_data.input_vars, list):
            missing = [v for v in prompt_data.input_vars if v not in inputs]
            if missing:
                raise MissingVariableError(prompt_data.name, missing)
            return

        fields = {}
        for var_name, type_key in prompt_data.input_vars.items():
            if type_key not in self._type_registry:
                raise TypeError(f"Type '{type_key}' is used in prompt '{prompt_data.name}' but was never registered in Soin.")
            python_type = self._type_registry[type_key]
            fields[var_name] = (python_type, ...)

        DynamicModel = create_model("DynamicInputModel", **fields)
        try:
            DynamicModel(**inputs)
        except Exception as e:
            raise TypeError(f"Validation failed for prompt '{prompt_data.name}':\n{e}")

    def render(self, prompt_name: str, **kwargs: Any) -> str:
        prompt_data = self._load_prompt(prompt_name)
        self._validate_inputs(prompt_data, kwargs)
        
        template = self.env.from_string(prompt_data.template)
        return template.render(**kwargs)