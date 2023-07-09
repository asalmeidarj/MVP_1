from pydantic import BaseModel
from typing import Optional, List


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
    data_insercao: str = "Sat, 08 Jul 2023 19:59:04 GMT"

class CargoListaViewSchema(BaseModel):
    cargo_empresas: List[CargoEmpresaViewSchema]


def apresenta_cargo_empresa(cargo_empresa):

    ano = cargo_empresa.data_insercao.year
    mes = cargo_empresa.data_insercao.month
    dia = cargo_empresa.data_insercao.day
    mes = f"0{mes}" if mes < 10 else mes
    dia = f"0{dia}" if dia < 10 else dia

    horas = cargo_empresa.data_insercao.hour
    minutos = cargo_empresa.data_insercao.minute
    segundos = cargo_empresa.data_insercao.second
    minutos = f"0{minutos}" if minutos < 10 else minutos
    segundos = f"0{segundos}" if segundos < 10 else segundos


    return {
        "id": cargo_empresa.id,
        "cargo_id": cargo_empresa.cargo.id,
        "cargo_nome": cargo_empresa.cargo_nome,
        "empresa_id": cargo_empresa.empresa.id,
        "empresa_nome": cargo_empresa.empresa_nome,
        "valor_contrato_diaria": cargo_empresa.valor_contrato_diaria,
        "valor_pago_diaria": cargo_empresa.valor_pago_diaria,
        "data_insercao": f"{ano}-{mes}-{dia}T{horas}:{segundos}:{minutos}"
    }


def apresenta_lista_cargoEmpresa(cargo_empresas):
    result = []
    for cargo in cargo_empresas:
        result.append(apresenta_cargo_empresa(cargo))
    return {"cargo_empresas": result}