from pydantic import BaseModel
from typing import List, Dict, Any
from soin_ai import Soin

# --- 1. Definição dos Dados (Seu domínio de negócio) ---
class Company(BaseModel):
    name: str
    city: str

# --- 2. Setup da Soin ---
sn = Soin(path="./prompts")

# Registrando tipos especiais para o validador da Soin
# Isso permite que o YAML entenda o que é 'Company' e 'EmployeeList'
sn.register_type("Company", Company)
sn.register_type("EmployeeList", List[Dict[str, Any]])

# --- 3. Dados de Teste ---
data = {
    "company": Company(name="Soin Tech", city="Russas, CE"),
    "threshold": 5000,
    "employees": [
        {"name": "Fernando", "role": "Lead Dev", "salary": 8000},
        {"name": "Maria", "role": "AI Engineer", "salary": 6000},
        {"name": "João", "role": "Junior", "salary": 3000},
    ]
}

# --- 4. Execução ---
print("🚀 Running Soin Complex Demo...\n")

try:
    rendered = sn.render("pro_demo", **data)
    print(rendered)
    
    print("\n✅ Success! All types validated and logic processed.")

except TypeError as e:
    print(f"❌ Validation Error:\n{e}")
except Exception as e:
    print(f"🔥 Unexpected Error: {e}")

# --- 5. Teste de Erro (Descomente para ver a trava funcionando) ---
# print("\n--- Testing Validation Failure ---")
# data["employees"] = "Not a list" # Isso deve disparar o TypeError
# sn.render("pro_demo", **data)