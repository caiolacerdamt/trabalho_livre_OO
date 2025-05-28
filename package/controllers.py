import datetime
from typing import List, Optional
from package.models import Transacao, Receita, Despesa, Categoria

class GerenciadorFinanceiro:
    def __init__(self):
        self._transacoes: List[Transacao] = []
        self._categorias: List[Categoria] = []
        self._next_transacao_id = 1
        self._next_categoria_id = 1

    @property
    def transacoes(self) -> List[Transacao]:
        return self._transacoes

    @transacoes.setter 
    def transacoes(self, novas_transacoes: List[Transacao]):
        self._transacoes = novas_transacoes
        if self._transacoes:
            self._next_transacao_id = max(t.id for t in self._transacoes) + 1
        else:
            self._next_transacao_id = 1

    @property
    def categorias(self) -> List[Categoria]:
        return self._categorias

    @categorias.setter 
    def categorias(self, novas_categorias: List[Categoria]):
        self._categorias = novas_categorias
        if self._categorias:
            self._next_categoria_id = max(c.id for c in self._categorias) + 1
        else:
            self._next_categoria_id = 1

    def gerar_id_transacao(self) -> int:
        new_id = self._next_transacao_id
        self._next_transacao_id += 1
        return new_id

    def gerar_id_categoria(self) -> int:
        new_id = self._next_categoria_id
        self._next_categoria_id += 1
        return new_id

    def adicionar_transacao(self, transacao: Transacao):
        if not isinstance(transacao, Transacao):
            raise TypeError("O objeto deve ser uma instância de Transacao, Receita ou Despesa.")
        self._transacoes.append(transacao)

    def remover_transacao(self, id_transacao: int) -> bool:
        original_len = len(self._transacoes)
        self._transacoes = [t for t in self._transacoes if t.id != id_transacao]
        return len(self._transacoes) < original_len

    def get_extrato(self, data_inicio: Optional[datetime.date] = None, data_fim: Optional[datetime.date] = None) -> List[Transacao]:
        extrato = sorted(self._transacoes, key=lambda t: t.data)
        if data_inicio and data_fim:
            return [t for t in extrato if data_inicio <= t.data <= data_fim]
        elif data_inicio:
            return [t for t in extrato if data_inicio <= t.data]
        elif data_fim:
            return [t for t in extrato if t.data <= data_fim]
        return extrato

    def get_saldo_atual(self) -> float:
        saldo = 0.0
        for transacao in self._transacoes:
            if transacao.get_tipo() == "Receita":
                saldo += transacao.valor
            elif transacao.get_tipo() == "Despesa":
                saldo -= transacao.valor
        return saldo

    def adicionar_categoria(self, categoria: Categoria):
        if not isinstance(categoria, Categoria):
            raise TypeError("O objeto deve ser uma instância de Categoria.")
        if not any(c.nome.lower() == categoria.nome.lower() for c in self._categorias):
            self._categorias.append(categoria)
            return True
        return False

    def get_categoria_by_nome(self, nome_categoria: str) -> Optional[Categoria]:
        return next((c for c in self._categorias if c.nome.lower() == nome_categoria.lower()), None)

    def listar_categorias(self) -> List[Categoria]:
        return sorted(self._categorias, key=lambda c: c.nome)

    def get_gastos_por_categoria(self, data_inicio: Optional[datetime.date] = None, data_fim: Optional[datetime.date] = None) -> dict:
        gastos_por_cat = {cat.nome: 0.0 for cat in self._categorias}
        for transacao in self.get_extrato(data_inicio, data_fim):
            if transacao.get_tipo() == "Despesa":
                gastos_por_cat[transacao.categoria.nome] += transacao.valor
        return gastos_por_cat