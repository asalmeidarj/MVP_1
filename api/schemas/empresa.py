from unicodedata import category
from pydantic import BaseModel
from typing import Optional, List


class EmpresaBodySchema(BaseModel):
    nome: str = "NOME DA EMPRESA"
    descricao: Optional[str] = "DESCRIÇÃO DA EMPRESA"

class EmpresaBuscaSchema(BaseModel):
    id: Optional[int] = 1
    nome: Optional[str] = "NOME DA EMPRESA"

class EmpresaViewSchema(BaseModel):
    id: int = 1
    nome: str = "NOME DA EMPRESA"
    descricao: Optional[str] = "DESCRIÇÃO DA EMPRESA"

class EmpresaDelSchema(BaseModel):
    message: str
    id: int

def apresenta_empresa(empresa):

    return {
        "id": empresa.id,
        "nome": empresa.nome,
        "descricao": empresa.descricao,
    }


class EmpresaListaViewSchema(BaseModel):
    empresas: List[EmpresaViewSchema]


def apresenta_lista_empresa(empresas):
    result = []
    for empresa in empresas:
        result.append(apresenta_empresa(empresa))
    return {"empresas": result}