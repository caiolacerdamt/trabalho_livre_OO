import json
import os
import datetime 
from typing import Dict, List, Any
from package.models import Transacao, Categoria

class PersistenciaDados:
    def __init__(self, nome_arquivo: str = "dados_financeiros.json"):
        self._nome_arquivo = nome_arquivo

    def salvar_dados(self, data: Dict[str, List[Any]]):
        try:
            with open(self._nome_arquivo, 'w', encoding='utf-8') as f:
                serializable_data = {
                    "transacoes": [t.to_dict() for t in data.get("transacoes", [])],
                    "categorias": [c.to_dict() for c in data.get("categorias", [])]
                }
                json.dump(serializable_data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Erro ao salvar dados: {e}")
        except Exception as e:
            print(f"Erro inesperado durante a serialização: {e}")


    def carregar_dados(self) -> Dict[str, List[Any]]:
        if not os.path.exists(self._nome_arquivo) or os.path.getsize(self._nome_arquivo) == 0:
            print(f"Arquivo '{self._nome_arquivo}' não encontrado ou vazio. Iniciando com dados vazios.")
            return {"transacoes": [], "categorias": []}

        try:
            with open(self._nome_arquivo, 'r', encoding='utf-8') as f:
                data = json.load(f)
                transacoes_carregadas = []
                categorias_carregadas = []
                for c_data in data.get("categorias", []):
                    try:
                        categorias_carregadas.append(Categoria.from_dict(c_data))
                    except ValueError as e:
                        print(f"Aviso: Não foi possível carregar categoria '{c_data.get('nome', 'N/A')}': {e}")
                
                categorias_map = {c.id: c for c in categorias_carregadas}

                for t_data in data.get("transacoes", []):
                    try:
                        transacoes_carregadas.append(Transacao.from_dict(t_data))
                    except ValueError as e:
                        print(f"Aviso: Não foi possível carregar transação '{t_data.get('descricao', 'N/A')}': {e}")
                    except Exception as e:
                        print(f"Erro inesperado ao carregar transação '{t_data.get('descricao', 'N/A')}': {e}")


                return {
                    "transacoes": transacoes_carregadas,
                    "categorias": categorias_carregadas
                }
        except json.JSONDecodeError as e:
            print(f"Erro de decodificação JSON ao carregar dados: {e}")
            return {"transacoes": [], "categorias": []}
        except IOError as e:
            print(f"Erro ao carregar dados (IOError): {e}")
            return {"transacoes": [], "categorias": []}
        except Exception as e: 
            print(f"Erro inesperado ao carregar dados: {e}")
            return {"transacoes": [], "categorias": []}