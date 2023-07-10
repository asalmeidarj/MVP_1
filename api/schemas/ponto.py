from unicodedata import category
from pydantic import BaseModel
from typing import Optional, List

from share.utils.date import formatDatetimeISO8601, formatDatetime


class PontoBodySchema(BaseModel):
    cargo_empresa_id: int = 1
    funcionario_id: int = 1
    dia: int = 9,
    mes: int = 7,
    ano: int = 2023,
    hora_entrada: int = 17
    minutos_entrada: int = 0
    hora_saida: int = 2
    minutos_saida: int = 0
    inicio_hora_intervalo: int = 22
    inicio_minutos_intervalo: int = 0
    final_hora_intervalo: int = 23
    final_minutos_intervalo: int = 0
    eh_dia_extra: bool = False

class PontoBuscaSchema(BaseModel):
    funcionario_id: Optional[int] = 1
    funcionario_cpf: Optional[str] = "CPF DO FUNCIONARIO"

class PontoViewSchema(BaseModel):
    id: int = 1
    funcionario_nome: str = "NOME DO FUNCIONARIO"
    funcionario_cpf: str = "TELEFONE DO FUNCIONARIO"
    empresa_id: int = 1
    empresa_nome: str = "NOME DA EMPRESA"
    data: str = "2023-07-09"
    hora_entrada: str = "17:35"
    hara_saida: str = "2:45"
    inicio_intervalo: str = "22:00"
    final_intervalo: str = "23:00"
    minutos_extras: int = 10,
    minutos_noturno: int = 240
    valor_a_pagar: float = 80
    valor_a_receber: float = 160
    data_insercao: str = "2023-07-09T15:17:41-03:00"

class PontoDelSchema(BaseModel):
    message: str
    id: int

def apresenta_ponto(ponto):

    hora_entrada = f"0{ponto.hora_entrada}" if ponto.hora_entrada < 10 else f"{ponto.hora_entrada}"
    minutos_entrada = f"0{ponto.minutos_entrada}" if ponto.minutos_entrada < 10 else f"{ponto.minutos_entrada}"
    hora_entrada += f":{minutos_entrada}"


    hora_saida = f"0{ponto.hora_saida}" if ponto.hora_saida < 10 else f"{ponto.hora_saida}"
    minutos_saida = f"0{ponto.minutos_saida}" if ponto.minutos_saida < 10 else f"{ponto.minutos_saida}"
    hora_saida += f":{minutos_saida}"

    inicio_intervalo = f"0{ponto.inicio_hora_intervalo}" if ponto.inicio_hora_intervalo < 10 else f"{ponto.inicio_hora_intervalo}"
    inicio_minutos_intervalo = f"0{ponto.inicio_minutos_intervalo}" if ponto.inicio_minutos_intervalo < 10 else f"{ponto.inicio_minutos_intervalo}"
    inicio_intervalo += f":{inicio_minutos_intervalo}"

    final_intervalo = f"0{ponto.final_hora_intervalo}" if ponto.final_hora_intervalo < 10 else f"{ponto.final_hora_intervalo}"
    final_minutos_intervalo = f"0{ponto.final_minutos_intervalo}" if ponto.final_minutos_intervalo < 10 else f"{ponto.final_minutos_intervalo}"
    final_intervalo += f":{final_minutos_intervalo}"

    return {
        "id": ponto.id,
        "funcionario_id": ponto.funcionario_id,
        "funcionario_nome": ponto.funcionario_nome,
        "funcionario_cpf": ponto.funcionario_cpf,
        "funcionario_cargo": ponto.cargo_nome,
        "data": formatDatetime(ponto.data),
        "empresa_id": ponto.empresa_id,
        "empresa_nome": ponto.empresa_nome,
        "hora_entrada": hora_entrada,
        "hora_saida": hora_saida,
        "inicio_intervalo": inicio_intervalo,
        "final_intervalo": final_intervalo,
        "minutos_extras": ponto.minutos_extras,
        "minutos_noturno": ponto.minutos_noturno,
        "valor_a_pagar": ponto.valor_a_pagar,
        "valor_a_receber": ponto.valor_a_receber,
        "data_insercao": formatDatetimeISO8601(ponto.data_insercao)
    }


class PontoListaViewSchema(BaseModel):
    pontos: List[PontoViewSchema]


def apresenta_lista_ponto(pontos):
    result = []
    for ponto in pontos:
        result.append(apresenta_ponto(ponto))
    return {"pontos": result}