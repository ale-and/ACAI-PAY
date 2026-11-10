"""Suíte de Testes TDD - Conta Digital com Extrato (AçaíPay).

UFPA / FACOMP - Engenharia de Software II.
Demarcação visual dos ciclos de TDD (Red -> Green -> Refactor).
"""

import pytest
from conta_digital import Conta, Entrada, ExcecaoConta, Lancamento


# ==============================================================================
# CICLO 1: Estado Inicial - Saldo Zero
# Requisito PDF: "Ao criar uma conta: o saldo deve iniciar em 0"
# [RED]      Escrever teste esperando conta.saldo == 0 (antes de implementar)
# [GREEN]    Criar classe Conta com self._saldo = 0
# [REFACTOR] Adicionar propriedade `saldo` e método `get_saldo()`
# ==============================================================================

def test_ciclo_1_nova_conta_inicia_com_saldo_zero():
    conta = Conta()
    assert conta.saldo == 0
    assert conta.get_saldo() == 0


# ==============================================================================
# CICLO 2: Estado Inicial - Extrato Vazio e Encapsulado
# Requisito PDF: "Ao criar uma conta: o extrato (lista de lançamentos) deve iniciar vazio"
#                "Regra de encapsulamento: o extrato não pode ser alterado diretamente"
# [RED]      Escrever teste esperando get_entradas() == () e proteção contra mutação
# [GREEN]    Inicializar self._entradas = [] e retornar tuple(self._entradas)
# [REFACTOR] Garantir que alterações externas falhem (imutabilidade via tuple)
# ==============================================================================

def test_ciclo_2_nova_conta_inicia_com_extrato_vazio():
    conta = Conta()
    assert conta.get_entradas() == ()
    assert conta.getEntradas() == ()


def test_ciclo_2_extrato_nao_pode_ser_alterado_externamente():
    conta = Conta()
    extrato = conta.get_entradas()

    assert isinstance(extrato, tuple)
    with pytest.raises(AttributeError):
        # Tentativa de append deve falhar pois uma tupla é imutável
        extrato.append(Lancamento("SAQUE", 10, 90))  # type: ignore[attr-defined]


# ==============================================================================
# CICLO 3: Depósito Válido - Atualização do Saldo
# Requisito PDF: "deposito(int quantia) -> o saldo aumenta em quantia"
# [RED]      Escrever teste esperando saldo final == saldo + quantia
# [GREEN]    Implementar método deposito adicionando quantia a self._saldo
# [REFACTOR] Isolamento do cálculo e validação inicial
# ==============================================================================

def test_ciclo_3_deposito_altera_saldo_corretamente():
    conta = Conta()

    conta.deposito(100)

    assert conta.saldo == 100


# ==============================================================================
# CICLO 4: Depósito Válido - Registro no Extrato (Ledger)
# Requisito PDF: "um lançamento é adicionado ao extrato com:
#                 tipo: 'DEPOSITO', valor: quantia, saldo após a operação"
# [RED]      Testar se get_entradas() contém registro com dados exatos e imutável
# [GREEN]    Modelar Lancamento/Entrada e registrar no append de deposito()
# [REFACTOR] Usar dataclass(frozen=True) para assegurar imutabilidade do registro
# ==============================================================================

def test_ciclo_4_deposito_cria_lancamento_correto_no_extrato():
    conta = Conta()

    conta.deposito(100)

    lancamentos = conta.get_entradas()
    assert len(lancamentos) == 1
    assert lancamentos[0] == Lancamento("DEPOSITO", 100, 100)
    assert lancamentos[0].tipo == "DEPOSITO"
    assert lancamentos[0].valor == 100
    assert lancamentos[0].saldo_apos_operacao == 100


def test_ciclo_4_lancamento_e_imutavel():
    conta = Conta()
    conta.deposito(100)
    lancamento = conta.get_entradas()[0]

    with pytest.raises(AttributeError):
        lancamento.valor = 500  # type: ignore[misc]


# ==============================================================================
# CICLO 5: Saque Válido - Redução do Saldo
# Requisito PDF: "saque(int quantia) -> o saldo diminui em quantia"
# [RED]      Testar saque após depósito prévio verificando redução do saldo
# [GREEN]    Implementar novo_saldo = self._saldo - quantia
# [REFACTOR] Assinatura e tipos explícitos
# ==============================================================================

def test_ciclo_5_saque_altera_saldo_corretamente_apos_deposito():
    conta = Conta()
    conta.deposito(100)

    conta.saque(40)

    assert conta.saldo == 60


# ==============================================================================
# CICLO 6: Saque Válido - Registro no Extrato (Ledger)
# Requisito PDF: "lançamento com tipo 'SAQUE', valor quantia, saldo pós-operação"
#                "A conta deve manter um histórico das operações na ordem"
# [RED]      Testar se registro tipo 'SAQUE' foi adicionado mantendo a ordem
# [GREEN]    Append de Lancamento("SAQUE", quantia, novo_saldo)
# [REFACTOR] Reutilização de Lancamento imutável
# ==============================================================================

def test_ciclo_6_saque_cria_lancamento_correto_no_extrato():
    conta = Conta()
    conta.deposito(100)

    conta.saque(40)

    lancamento_saque = conta.get_entradas()[-1]
    assert lancamento_saque == Lancamento("SAQUE", 40, 60)
    assert lancamento_saque.tipo == "SAQUE"
    assert lancamento_saque.valor == 40
    assert lancamento_saque.saldo_apos_operacao == 60


def test_ciclo_6_operacoes_mantem_ordem_no_extrato():
    conta = Conta()
    conta.deposito(100)
    conta.saque(25)
    conta.deposito(10)

    assert [entrada.tipo for entrada in conta.get_entradas()] == [
        "DEPOSITO", "SAQUE", "DEPOSITO"
    ]
    assert [entrada.saldo_apos_operacao for entrada in conta.get_entradas()] == [
        100, 75, 85
    ]


# ==============================================================================
# [PRÓXIMOS CICLOS] VALIDAÇÕES E TRANSFERÊNCIA
# ==============================================================================

@pytest.mark.parametrize("quantia", [0, -10])
def test_deposito_com_quantia_invalida_lanca_excecao(quantia):
    conta = Conta()

    with pytest.raises(ExcecaoConta):
        conta.deposito(quantia)

    assert conta.saldo == 0
    assert conta.get_entradas() == ()


@pytest.mark.parametrize("quantia", [0, -10])
def test_saque_com_quantia_invalida_lanca_excecao(quantia):
    conta = Conta()
    conta.deposito(100)
    saldo_anterior = conta.saldo
    extrato_anterior = conta.get_entradas()

    with pytest.raises(ExcecaoConta):
        conta.saque(quantia)

    assert conta.saldo == saldo_anterior
    assert conta.get_entradas() == extrato_anterior


def test_saque_maior_que_saldo_nao_altera_estado():
    conta = Conta()
    conta.deposito(50)
    extrato_anterior = conta.get_entradas()

    with pytest.raises(ExcecaoConta, match="Saldo insuficiente"):
        conta.saque(60)

    assert conta.saldo == 50
    assert conta.get_entradas() == extrato_anterior


def test_transferencia_atualiza_as_duas_contas_e_os_extratos():
    origem = Conta()
    destino = Conta()
    origem.deposito(100)

    origem.transferencia_para(destino, 35)

    assert origem.saldo == 65
    assert destino.saldo == 35
    assert origem.get_entradas()[-1] == Lancamento("SAQUE", 35, 65)
    assert destino.get_entradas() == (
        Lancamento("DEPOSITO", 35, 35),
    )


def test_transferencia_sem_saldo_suficiente_nao_altera_nenhuma_conta():
    origem = Conta()
    destino = Conta()
    origem.deposito(20)
    extrato_origem = origem.get_entradas()
    extrato_destino = destino.get_entradas()

    with pytest.raises(ExcecaoConta, match="Saldo insuficiente"):
        origem.transferencia_para(destino, 30)

    assert origem.saldo == 20
    assert destino.saldo == 0
    assert origem.get_entradas() == extrato_origem
    assert destino.get_entradas() == extrato_destino


def test_transferencia_para_propria_conta_e_recusada_sem_alteracoes():
    conta = Conta()
    conta.deposito(50)
    saldo_anterior = conta.saldo
    extrato_anterior = conta.get_entradas()

    with pytest.raises(ExcecaoConta):
        conta.transferencia_para(conta, 10)

    assert conta.saldo == saldo_anterior
    assert conta.get_entradas() == extrato_anterior
