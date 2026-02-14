from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Union

class PromptModel(BaseModel):
    name: str
    description: Optional[str] = "No description provided."
    version: Optional[str] = "1.0.0"
    input_vars: Union[List[str], Dict[str, str]] = Field(default_factory=list)
    template: str

    @field_validator('template')
    @classmethod
    def template_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("The 'template' field cannot be empty.")
        return v