"""Domínio de conta digital com extrato (Ledger) - AçaíPay.

Atividade de TDD da UFPA / FACOMP - Engenharia de Software II.
"""

from dataclasses import dataclass


# ==============================================================================
# CLASSES DE APOIO / EXCEÇÕES
# ==============================================================================

class ExcecaoConta(ValueError):
    """Erro lançado quando uma operação da conta viola uma regra de negócio."""


# [CICLO 4 - GREEN/REFACTOR] Modelagem de Lançamento/Entrada no Extrato
# Atende à exigência de registro com tipo, valor e saldo após operação.
# 'frozen=True' garante a regra de negócio de imutabilidade de lançamentos.
@dataclass(frozen=True)
class Lancamento:
    """Registro imutável de uma operação realizada na conta."""

    tipo: str
    valor: int
    saldo_apos_operacao: int


# Alias para o nome sugerido no documento do professor: "Entrada"
Entrada = Lancamento


# ==============================================================================
# CLASSE DE PRODUÇÃO: CONTA
# ==============================================================================

class Conta:
    """Conta digital que mantém saldo e histórico de operações."""

    # --------------------------------------------------------------------------
    # [CICLO 1 & CICLO 2] Estado Inicial
    # Requisito 1 do PDF: Saldo inicia em 0 e extrato inicia vazio.
    # --------------------------------------------------------------------------
    def __init__(self) -> None:
        self._saldo: int = 0                    # [CICLO 1 - GREEN] Saldo inicial 0
        self._entradas: list[Lancamento] = []  # [CICLO 2 - GREEN] Extrato inicial vazio

    # --------------------------------------------------------------------------
    # [CICLO 1] Consulta de Saldo
    # --------------------------------------------------------------------------
    @property
    def saldo(self) -> int:
        """Retorna o saldo atual."""
        return self._saldo

    def get_saldo(self) -> int:
        """Acesso explícito ao saldo."""
        return self._saldo

    getSaldo = get_saldo  # Alias no formato camelCase citado nas instruções

    # --------------------------------------------------------------------------
    # [CICLO 2] Consulta e Encapsulamento do Extrato
    # Requisito 4 do PDF: O extrato não pode ser alterado diretamente por quem
    # usa a classe. O retorno em tuple garante a imutabilidade externa.
    # --------------------------------------------------------------------------
    def get_entradas(self) -> tuple[Lancamento, ...]:
        """Retorna uma visão imutável do extrato."""
        return tuple(self._entradas)

    getEntradas = get_entradas  # Alias para nome sugerido no PDF: getEntradas()

    # --------------------------------------------------------------------------
    # Validações internas auxiliares
    # --------------------------------------------------------------------------
    @staticmethod
    def _validar_quantia(quantia: int) -> None:
        # bool é subtipo de int em Python, mas não representa uma quantia válida.
        if isinstance(quantia, bool) or not isinstance(quantia, int):
            raise ExcecaoConta("A quantia deve ser um número inteiro.")
        if quantia <= 0:
            raise ExcecaoConta("A quantia deve ser maior que zero.")

    # --------------------------------------------------------------------------
    # [CICLO 3 & CICLO 4] Operação de Depósito
    # Requisito 2 do PDF:
    # - [CICLO 3] Aumentar saldo em quantia.
    # - [CICLO 4] Adicionar lançamento ("DEPOSITO", quantia, saldo_apos_operacao).
    # --------------------------------------------------------------------------
    def deposito(self, quantia: int) -> None:
        """Deposita uma quantia positiva e registra a operação no extrato."""
        self._validar_quantia(quantia)

        # [CICLO 3 - GREEN] Atualização de saldo
        novo_saldo = self._saldo + quantia
        self._saldo = novo_saldo

        # [CICLO 4 - GREEN] Registro no extrato
        self._entradas.append(
            Lancamento(
                tipo="DEPOSITO",
                valor=quantia,
                saldo_apos_operacao=novo_saldo
            )
        )

    # --------------------------------------------------------------------------
    # Operações seguintes (Saque e Transferência)
    # (Serão demarcadas visualmente nos próximos passos)
    # --------------------------------------------------------------------------
    def saque(self, quantia: int) -> None:
        """Saca uma quantia positiva, desde que haja saldo suficiente."""
        self._validar_quantia(quantia)

        if quantia > self._saldo:
            raise ExcecaoConta("Saldo insuficiente.")

        novo_saldo = self._saldo - quantia
        self._saldo = novo_saldo
        self._entradas.append(
            Lancamento("SAQUE", quantia, novo_saldo)
        )

    def transferencia_para(self, outra: "Conta", quantia: int) -> None:
        """Transfere dinheiro para outra conta (bônus do exercício).

        As validações acontecem antes de qualquer alteração, evitando
        efeitos colaterais quando a transferência falha.
        """
        self._validar_quantia(quantia)

        if not isinstance(outra, Conta):
            raise ExcecaoConta("A conta de destino é inválida.")
        if outra is self:
            raise ExcecaoConta("Não é possível transferir para a própria conta.")
        if quantia > self._saldo:
            raise ExcecaoConta("Saldo insuficiente.")

        saldo_origem = self._saldo - quantia
        saldo_destino = outra._saldo + quantia

        self._saldo = saldo_origem
        self._entradas.append(Lancamento("SAQUE", quantia, saldo_origem))

        outra._saldo = saldo_destino
        outra._entradas.append(
            Lancamento("DEPOSITO", quantia, saldo_destino)
        )

    transferenciaPara = transferencia_para  # Alias sugerido no PDF
