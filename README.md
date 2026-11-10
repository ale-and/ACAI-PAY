# AçaíPay - Conta Digital com Extrato (Ledger)

Projeto desenvolvido como parte da disciplina de **Engenharia de Software II** (UFPA / FACOMP - Prof. Dr. Victor Santiago). O objetivo é implementar o núcleo de uma fintech educacional utilizando a metodologia **TDD (Test-Driven Development)** em ciclos curtos:
1. **Red**: Escrever um teste pequeno que falha;
2. **Green**: Implementar o mínimo necessário para passar;
3. **Refactor**: Melhorar o design e estrutura sem alterar o comportamento.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **Pytest**

---

## 🔄 Ciclos de Desenvolvimento TDD

O código de teste e de produção foi estruturado com marcações visuais explícitas para demonstrar cada ciclo de TDD:

| Ciclo | Descrição / Requisito | Status |
|---|---|---|
| **Ciclo 1** | Estado Inicial: saldo deve iniciar em 0 | ✅ Documentado & Testado |
| **Ciclo 2** | Estado Inicial: extrato vazio e protegido contra alterações externas (encapsulamento) | ✅ Documentado & Testado |
| **Ciclo 3** | Depósito Válido: saldo aumenta na quantia informada | ✅ Documentado & Testado |
| **Ciclo 4** | Depósito no Extrato: criação de registro imutável com tipo `"DEPOSITO"`, valor e saldo após operação | ✅ Documentado & Testado |
| **Ciclo 5** | Saque Válido: saldo diminui na quantia informada | ✅ Documentado & Testado |
| **Ciclo 6** | Saque no Extrato: criação de registro com tipo `"SAQUE"`, valor e saldo após operação | ✅ Documentado & Testado |
| **Ciclo 7** | Validação: depósito com quantia `<= 0` lança exceção | ⏳ Próxima etapa |
| **Ciclo 8** | Validação: saque com quantia `<= 0` lança exceção | ⏳ Próxima etapa |
| **Ciclo 9** | Saldo Insuficiente: saque maior que saldo lança exceção sem efeito colateral | ⏳ Próxima etapa |
| **Ciclo 10** | Bônus: Transferência entre contas com validações e registros cruzados | ⏳ Próxima etapa |

---

## 🚀 Como Executar

### 1. Criar e ativar o ambiente virtual (opcional se já tiver o `.venv`):
```bash
python -m venv .venv

# Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Linux / Mac:
source .venv/bin/activate
```

### 2. Instalar as dependências de desenvolvimento:
```bash
pip install -e ".[dev]"
```

### 3. Executar os testes automatizados com Pytest:
```bash
pytest
```
Ou com saída detalhada:
```bash
pytest -v
```
