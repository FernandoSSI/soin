<div align="center">
    <picture>
      <img alt="Soin Logo" src=".github/images/banner.jpg" style="border-radius: 10px;">
    </picture>
</div>

# SOIN
### Simple Optimized Instruction Network

[![PyPI version](https://badge.fury.io/py/soin-ai.svg)](https://badge.fury.io/py/soin-ai)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight, type-safe prompt management library for Python. Manage your LLM prompts in YAML files with Jinja2 templating and Pydantic validation.

---

## Features

- **Type-Safe**: Automatic input validation with Pydantic
- **Jinja2 Templates**: Loops, conditionals, and filters in your prompts
- **YAML-Based**: Separate prompts from application code
- **Custom Types**: Register your own classes for validation
- **Zero Config**: Just point to a directory and start

---

## Installation

```bash
pip install soin-ai
```

**Requirements:** Python 3.11+, Jinja2, PyYAML, Pydantic

---

## Quick Start

### 1. Create a prompt file

**prompts/greeting.yaml:**
```yaml
name: greeting
description: Simple greeting prompt
input_vars:
  - name
  - age
template: |
  Hello, {{ name }}! You are {{ age }} years old.
  {% if age >= 18 %}You are an adult.{% endif %}
```

### 2. Use it in Python

```python
from soin_ai import Soin

soin = Soin("./prompts")
output = soin.render("greeting", name="John", age=25)
print(output)
```

**Output:**
```
Hello, John! You are 25 years old.
You are an adult.
```

---

## Documentation

### Prompt Structure

```yaml
name: prompt_name          # Required: unique identifier
description: description   # Optional: prompt description
version: 1.0.0            # Optional: version control
input_vars: [...]         # Required: input variables (list or dict)
template: |               # Required: Jinja2 template
  Your prompt here...
```

### Basic Usage

```python
from soin_ai import Soin

# Initialize
soin = Soin("./prompts")

# Render a prompt
output = soin.render("prompt_name", var1="value1", var2="value2")
```

---

## Input Validation

### Simple Validation (List)

Checks if required variables are provided:

```yaml
name: simple
input_vars:
  - username
  - message
template: |
  User: {{ username }}
  Message: {{ message }}
```

### Type Validation (Dict)

Validates data types with Pydantic:

```yaml
name: typed
input_vars:
  username: str
  age: int
  score: float
  active: bool
template: |
  User: {{ username }} ({{ age }} years old)
  Score: {{ score }}
  Status: {{ active }}
```

**Supported types:** `str`, `int`, `float`, `bool`, `list`, `dict`, `any`

```python
# Valid
soin.render("typed", username="John", age=25, score=95.5, active=True)

# Raises TypeError: age must be int
soin.render("typed", username="John", age="25", score=95.5, active=True)
```

---

## Custom Types

Register custom Python classes for validation:

```python
from dataclasses import dataclass
from soin_ai import Soin

@dataclass
class User:
    name: str
    email: str
    role: str

soin = Soin("./prompts")
soin.register_type("User", User)
```

**prompts/user.yaml:**
```yaml
name: user_prompt
input_vars:
  user: User
  action: str
template: |
  User: {{ user.name }} ({{ user.email }})
  Role: {{ user.role }}
  Action: {{ action }}
```

**Usage:**
```python
user = User(name="John", email="john@example.com", role="Admin")
output = soin.render("user_prompt", user=user, action="login")
```

### With Pydantic Models

```python
from pydantic import BaseModel
from typing import List

class Product(BaseModel):
    id: int
    name: str
    price: float

class Order(BaseModel):
    order_id: str
    products: List[Product]
    customer: str

soin = Soin("./prompts")
soin.register_type("Order", Order)
```

```yaml
name: order_summary
input_vars:
  order: Order
template: |
  Order #{{ order.order_id }}
  Customer: {{ order.customer }}

  Items:
  {% for product in order.products %}
  - {{ product.name }}: ${{ "%.2f"|format(product.price) }}
  {% endfor %}

  Total: ${{ "%.2f"|format(order.products|sum(attribute='price')) }}
```

---

## Jinja2 Templates

Full Jinja2 support with conditionals, loops, filters, and expressions:

### Conditionals
```yaml
template: |
  {% if user_type == "premium" %}
  Welcome, premium user!
  {% else %}
  Welcome, regular user!
  {% endif %}
```

### Loops
```yaml
template: |
  Tasks:
  {% for task in tasks %}
  - {{ task.title }} (Priority: {{ task.priority }})
  {% endfor %}
```

### Filters
```yaml
template: |
  Uppercase: {{ name | upper }}
  Truncate: {{ text | truncate(50) }}
  Round: {{ price | round(2) }}
```

### Expressions
```yaml
template: |
  Total: {{ price * quantity }}
  Discount: {{ total * 0.1 }}
  Final: {{ (price * quantity) - discount }}
```

---

## Error Handling

### `PromptNotFoundError`
Raised when prompt file doesn't exist:

```python
from soin_ai import Soin, PromptNotFoundError

try:
    output = soin.render("nonexistent")
except PromptNotFoundError as e:
    print(e.message)
    # Soin could not find prompt 'nonexistent' at: ./prompts
```

### `MissingVariableError`
Raised when required variables are missing:

```python
from soin_ai import MissingVariableError

try:
    output = soin.render("greeting", name="John")  # missing 'age'
except MissingVariableError as e:
    print(e.message)
    # Missing required variables for 'greeting': age
```

### `TypeError`
Raised when type validation fails:

```python
try:
    output = soin.render("typed", username="John", age="twenty")
except TypeError as e:
    print(e)
```

---

## Examples

### Code Review System

**prompts/code_review.yaml:**
```yaml
name: code_review
input_vars:
  language: str
  code: str
  focus_areas: list
template: |
  Review this {{ language }} code:

  ```{{ language }}
  {{ code }}
  ```

  Focus on:
  {% for area in focus_areas %}
  - {{ area }}
  {% endfor %}
```

**Usage:**
```python
output = soin.render(
    "code_review",
    language="python",
    code="def add(a, b): return a + b",
    focus_areas=["performance", "readability"]
)
```

### Multi-Language System

**prompts/welcome.yaml:**
```yaml
name: welcome
input_vars:
  username: str
  language: str
template: |
  {% if language == "en" %}
  Hello, {{ username }}!
  {% elif language == "es" %}
  ¡Hola, {{ username }}!
  {% elif language == "pt" %}
  Olá, {{ username }}!
  {% endif %}
```

---

## API Reference

### `Soin(path: str)`
Initialize prompt manager.

**Args:**
- `path`: Directory containing YAML prompt files

**Raises:**
- `FileNotFoundError`: If directory doesn't exist

### `render(prompt_name: str, **kwargs) -> str`
Render a prompt with variables.

**Args:**
- `prompt_name`: Name of prompt file (without .yaml)
- `**kwargs`: Variables to inject into template

**Returns:**
- Rendered prompt string

**Raises:**
- `PromptNotFoundError`: Prompt not found
- `MissingVariableError`: Required variables missing
- `TypeError`: Type validation failed

### `register_type(name: str, python_type: Any) -> None`
Register custom type for validation.

**Args:**
- `name`: Type name to use in YAML
- `python_type`: Python class or type

---

## Best Practices

### Organize Prompts
```
prompts/
├── users/
│   ├── welcome.yaml
│   └── profile.yaml
├── ai/
│   ├── review.yaml
│   └── summarize.yaml
```

### Type Safety
```yaml
# Prefer typed validation
input_vars:
  user_id: int        # Better than 'any'
  email: str          # Be explicit
  active: bool        # Type safe
```



## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request



## License

MIT License - see [LICENSE](LICENSE) file for details.




<div align="center">
  <p>If it was helpful, consider giving it a ⭐</p>
</div>
