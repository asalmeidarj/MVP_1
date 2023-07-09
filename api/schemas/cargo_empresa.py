from pydantic import BaseModel
from typing import Optional, List

from share.utils.date import formatDatetimeISO8601


class CargoEmpresaBodySchema(BaseModel):
    cargo_id: int = 1
    empresa_id: int = 1
    valor_contrato_diaria: float = 300.00
    valor_pago_diaria: float = 200.00

class CargoEmpresaBuscaSchema(BaseModel):
    cargo_id: int = 1
    empresa_id: int = 1

class CargoEmpresaViewSchema(BaseModel):
    id: int = 1
    cargo_id: int = 1
    cargo_nome: str = "NOME DO CARGO"
    empresa_id: int = 1
    empresa_nome: str = "NOME DA EMREPSA"
    valor_contrato_diaria: float = 500
    valor_pago_diaria: float = 200
    data_insercao: str = "2023-07-09T15:17:41"

class CargoListaViewSchema(BaseModel):
    cargo_empresas: List[CargoEmpresaViewSchema]


def apresenta_cargo_empresa(cargo_empresa):

    return {
        "id": cargo_empresa.id,
        "cargo_id": cargo_empresa.cargo.id,
        "cargo_nome": cargo_empresa.cargo_nome,
        "empresa_id": cargo_empresa.empresa.id,
        "empresa_nome": cargo_empresa.empresa_nome,
        "valor_contrato_diaria": cargo_empresa.valor_contrato_diaria,
        "valor_pago_diaria": cargo_empresa.valor_pago_diaria,
        "data_insercao": formatDatetimeISO8601(cargo_empresa.data_insercao)
    }


def apresenta_lista_cargoEmpresa(cargo_empresas):
    result = []
    for cargo in cargo_empresas:
        result.append(apresenta_cargo_empresa(cargo))
    return {"cargo_empresas": result}