# Conta Digital com Extrato — Python

Adaptação do exercício Java de Conta Digital com Extrato (Ledger) para Python.

## Requisitos

- Python 3.10 ou superior
- pytest para executar os testes

## Estrutura

```text
conta_digital_python/
├── pyproject.toml
├── README.md
├── src/
│   └── conta_digital/
│       ├── __init__.py
│       └── conta.py
└── tests/
    └── test_conta.py
```

## Instalação

No terminal, dentro da pasta do projeto:

```bash
python -m venv .venv
```

Ative o ambiente virtual:

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

Instale as dependências de desenvolvimento:

```bash
python -m pip install -e ".[dev]"
```

## Executar os testes

```bash
python -m pytest
```

## Exemplo de uso

```python
from conta_digital import Conta

conta = Conta()
conta.deposito(100)
conta.saque(30)

print(conta.saldo)       # 70
print(conta.get_entradas())
```

## Regras implementadas

- A conta começa com saldo zero e extrato vazio.
- Depósitos e saques exigem quantias inteiras positivas.
- Cada operação válida registra tipo, valor e saldo após a operação.
- O extrato é exposto como tupla e seus lançamentos são imutáveis.
- Saque acima do saldo é recusado sem alterar saldo ou extrato.
- Transferência entre contas está incluída como bônus e valida tudo antes de alterar as contas.
