import datetime
from abc import ABC, abstractmethod

class Categoria:
    def __init__(self, id_categoria: int, nome: str):
        self._id = id_categoria
        self._nome = nome
    
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def nome(self) -> str:
        return self._nome
    
    @nome.setter
    def nome(self, novo_nome: str):
        if not isinstance(novo_nome, str) or not novo_nome:
            raise ValueError("O nome da catgoria deve ser uma string não vazia.")
        self._nome = novo_nome

    def __str__(self) -> str:
        return f"Categoria(ID: {self._id}, Nome: {self._nome})"
    
    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "nome": self._nome
        }
    
    @staticmethod
    def from_dict(data: dict):
        return Categoria(data["id"], data["nome"])
    
class Transacao(ABC):
    def __init__(self, id_transacao: int, valor: float, descricao: str, data: datetime.date, categoria: Categoria):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("O Valor da transação deve ser um número positivo.")
        if not isinstance(descricao, str) or not descricao.strip():
            raise ValueError("A descrição da transação não pode ser vazia.")
        if not isinstance(data, datetime.date):
            raise ValueError("A data deve ser um objeto datetime.date")
        if not isinstance(categoria, Categoria):
            raise ValueError("A categoria deve ser um objeto Categoria.")
        
        self._id = id_transacao
        self._valor = valor
        self._descricao = descricao
        self._data = data
        self._categoria = categoria

    @property
    def id(self) -> int:
        return self._id
    
    @property
    def valor(self) -> float:
        return self._valor
    
    @property
    def descricao(self) -> str:
        return self._descricao
    
    @property
    def data(self) -> datetime.date:
        return self._data
    
    @property
    def categoria(self) -> Categoria:
        return self._categoria
    
    @abstractmethod 
    def get_tipo(self) -> str:
        pass
    
    def __str__(self) -> str:
        return (f"ID {self._id}, Valor: R${self._valor:.2f}. Descrição: {self._descricao}."
                f"Data: {self._data.strftime('%d/%m/%Y')}, Categoria: {self._categoria.nome}")
    
    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "valor": self._valor,
            "descricao": self._descricao,
            "data": self._data.isoformat(),
            "categoria": self._categoria.to_dict(), 
            "tipo": self.get_tipo() 
        }
    
    @staticmethod
    def from_dict(data: dict):
        categoria = Categoria.from_dict(data["categoria"])
        data_obj = datetime.date.fromisoformat(data["data"])
        if data["tipo"] == "Receita":
            return Receita(data["id"], data["valor"], data["descricao"], data_obj, categoria)
        elif data["tipo"] == "Despesa":
            return Despesa(data["id"], data["valor"], data["descricao"], data_obj, categoria)
        else:
            raise ValueError("Tipo de transação desconhecido.")
        

class Receita(Transacao):
    def __init__(self, id_transacao: int, valor: float, descricao: str, data: datetime.date, categoria: Categoria):
        super().__init__(id_transacao, valor, descricao, data, categoria)

    def get_tipo(self) -> str: 
        return "Receita"

    def __str__(self) -> str:
        return f"RECEITA - {super().__str__()}"
    
class Despesa(Transacao): 
    def __init__(self, id_transacao: int, valor: float, descricao: str, data: datetime.date, categoria: Categoria):
        super().__init__(id_transacao, valor, descricao, data, categoria)

    def get_tipo(self) -> str: 
        return "Despesa"

    def __str__(self) -> str:
        return f"DESPESA - {super().__str__()}"