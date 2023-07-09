from unicodedata import category
from pydantic import BaseModel
from typing import Optional, List


class FuncionarioBodySchema(BaseModel):
    nome: str = "NOME DO FUNCIONARIO"
    cnpj: str = "CNPJ DO FUNCIONARIO"
    telefone: str = "TELEFONE DO FUNCIONARIO"
    logradouro: Optional[str] = "LOGRADOURO DO FUNCIONARIO"
    numero: Optional[str] = "NUMERO DO FUNCIONARIO"
    complemento: Optional[str] = "NUMERO DO FUNCIONARIO"
    bairro: Optional[str] = "BAIRRO DO FUNCIONARIO"
    cidade: Optional[str] = "CIDADE QUE FUNCIONARIO ESTÁ LOCALIZADO"
    estado: Optional[str] = "ESTADO QUE FUNCIONARIO ESTÁ LOCALIZAD"

class FuncionarioBuscaSchema(BaseModel):
    id: Optional[int] = 1
    nome: Optional[str] = "NOME DO FUNCIONARIO"

class FuncionarioViewSchema(BaseModel):
    id: int = 1
    nome: str = "NOME DO FUNCIONARIO"
    cpf: str = "TELEFONE DO FUNCIONARIO"
    data_insercao: str = "2023-07-09T15:17:41"

class FuncionarioDelSchema(BaseModel):
    message: str
    id: int

def apresenta_funcionario(funcionario):

    return {
        "id": funcionario.id,
        "nome": funcionario.nome,
        "cpf": funcionario.cpf,
        "data_insercao": funcionario.data_insercao
    }


class FuncionarioListaViewSchema(BaseModel):
    funcionarios: List[FuncionarioViewSchema]


def apresenta_lista_funcionario(funcionarios):
    result = []
    for funcionario in funcionarios:
        result.append(apresenta_funcionario(funcionario))
    return {"funcionarios": result}