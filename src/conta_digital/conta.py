"""Domínio de conta digital com extrato (Ledger)."""

from dataclasses import dataclass


class ExcecaoConta(ValueError):
    """Erro lançado quando uma operação da conta viola uma regra de negócio."""


@dataclass(frozen=True)
class Lancamento:
    """Registro imutável de uma operação realizada na conta."""

    tipo: str
    valor: int
    saldo_apos_operacao: int


class Conta:
    """Conta digital que mantém saldo e histórico de operações."""

    def __init__(self) -> None:
        self._saldo = 0
        self._entradas: list[Lancamento] = []

    @property
    def saldo(self) -> int:
        """Retorna o saldo atual."""
        return self._saldo

    def get_saldo(self) -> int:
        """Versão em estilo Java do acesso ao saldo."""
        return self._saldo

    def get_entradas(self) -> tuple[Lancamento, ...]:
        """Retorna uma visão imutável do extrato."""
        return tuple(self._entradas)

    @staticmethod
    def _validar_quantia(quantia: int) -> None:
        # bool é subtipo de int em Python, mas não representa uma quantia válida.
        if isinstance(quantia, bool) or not isinstance(quantia, int):
            raise ExcecaoConta("A quantia deve ser um número inteiro.")
        if quantia <= 0:
            raise ExcecaoConta("A quantia deve ser maior que zero.")

    def deposito(self, quantia: int) -> None:
        """Deposita uma quantia positiva e registra a operação."""
        self._validar_quantia(quantia)

        novo_saldo = self._saldo + quantia
        self._saldo = novo_saldo
        self._entradas.append(
            Lancamento("DEPOSITO", quantia, novo_saldo)
        )

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
