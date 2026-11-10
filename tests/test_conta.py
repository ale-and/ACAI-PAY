import pytest

from conta_digital import Conta, ExcecaoConta, Lancamento


def test_nova_conta_inicia_com_saldo_zero():
    conta = Conta()
    assert conta.saldo == 0


def test_nova_conta_inicia_com_extrato_vazio():
    conta = Conta()
    assert conta.get_entradas() == ()


def test_deposito_altera_saldo_corretamente():
    conta = Conta()

    conta.deposito(100)

    assert conta.saldo == 100


def test_deposito_cria_lancamento_correto_no_extrato():
    conta = Conta()

    conta.deposito(100)

    assert conta.get_entradas() == (
        Lancamento("DEPOSITO", 100, 100),
    )


def test_saque_altera_saldo_corretamente_apos_deposito():
    conta = Conta()
    conta.deposito(100)

    conta.saque(40)

    assert conta.saldo == 60


def test_saque_cria_lancamento_correto_no_extrato():
    conta = Conta()
    conta.deposito(100)

    conta.saque(40)

    assert conta.get_entradas()[-1] == Lancamento("SAQUE", 40, 60)


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


def test_extrato_nao_pode_ser_alterado_externamente():
    conta = Conta()
    conta.deposito(100)

    extrato = conta.get_entradas()

    assert isinstance(extrato, tuple)
    with pytest.raises(AttributeError):
        extrato.append(Lancamento("SAQUE", 10, 90))


def test_lancamento_e_imutavel():
    conta = Conta()
    conta.deposito(100)
    lancamento = conta.get_entradas()[0]

    with pytest.raises(AttributeError):
        lancamento.valor = 500


def test_operacoes_mantem_ordem_no_extrato():
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
