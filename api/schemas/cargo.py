from pydantic import BaseModel
from typing import Optional, List


class CargoBodySchema(BaseModel):
    nome: str = "NOME DO CARGO"

class CargoBuscaSchema(BaseModel):
    id: Optional[int] = 1
    nome: Optional[str] = "NOME DO CARGO"

class CargoViewSchema(BaseModel):
    id: int = 1
    nome: str = "NOME DO CARGO"

class CargoDelSchema(BaseModel):
    message: str
    id: int

def apresenta_cargo(cargo):

    return {
        "id": cargo.id,
        "nome": cargo.nome,
        "data_insercao": cargo.data_insercao
    }


class CargoListaViewSchema(BaseModel):
    cargos: List[CargoViewSchema]


def apresenta_lista_cargo(cargos):
    result = []
    for cargo in cargos:
        result.append(apresenta_cargo(cargo))
    return {"cargos": result}