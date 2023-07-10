from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
from datetime import datetime

from  model import Base, Cargo_empresa, Funcionario

import pytz


class Ponto(Base):
    __tablename__ = 'ponto'

    id = Column("pk_ponto", Integer, primary_key=True) 
    cargo_empresa_id = Column(Integer, ForeignKey("cargo_empresa.pk_cargo_empresa"), nullable=False)
    funcionario_id = Column(Integer, ForeignKey("funcionario.pk_funcionario"), nullable=False)
    empresa_id = Column(Integer)
    cargo_nome = Column(String(40))
    empresa_nome = Column(String(40))
    funcionario_nome = Column(String(40))
    funcionario_cpf = Column(String(14))
    valor_contrato_diaria = Column(Float)
    valor_pago_diaria = Column(Float)
    valor_a_receber = Column(Float)
    valor_a_pagar = Column(Float)
    data = Column(DateTime)
    hora_entrada = Column(Integer)
    minutos_entrada = Column(Integer)
    hora_saida = Column(Integer)
    minutos_saida= Column(Integer)
    hora_saida = Column(Integer)
    minutos_saida = Column(Integer)
    inicio_hora_intervalo = Column(Integer)
    inicio_minutos_intervalo = Column(Integer)
    final_hora_intervalo = Column(Integer)
    final_minutos_intervalo = Column(Integer)
    minutos_extras = Column(Integer)
    minutos_noturno = Column(Integer)
    eh_dia_extra = Column(Boolean)

    data_insercao = Column(DateTime, default=datetime.now())

    cargo_empresa = relationship('Cargo_empresa')
    funcionario = relationship('Funcionario')

    def __init__(
        self, 
        cargo_empresa: Cargo_empresa,
        funcionario: Funcionario,
        dia: int,
        mes: int,
        ano: int,
        hora_entrada: int,
        minutos_entrada: int,
        hora_saida: int,
        minutos_saida: int,
        inicio_hora_intervalo: int,
        inicio_minutos_intervalo: int,
        final_hora_intervalo: int,
        final_minutos_intervalo: int,
        eh_dia_extra: bool = False
    ):
        """
        Cria um Cargo_empresa

        Arguments:
            nome: nome do cargo_empresa.
            data_insercao: data de quando o cargo_empresa foi inserido à base
        """

        minutos_trabalhado = 0
        minutos_intervalo = 0
        minutos_noturno = 0
        minutos_extras = 0

        timeZone = pytz.timezone('America/Sao_Paulo')

        self.funcionario = funcionario
        self.funcionario_id = funcionario.id
        self.funcionario_nome = funcionario.nome
        self.funcionario_cpf = funcionario.cpf
        self.cargo_empresa = cargo_empresa
        self.cargo_empresa_id = cargo_empresa.id
        self.cargo_nome = cargo_empresa.cargo_nome
        self.empresa_id = cargo_empresa.empresa_id
        self.empresa_nome = cargo_empresa.empresa_nome
        self.valor_contrato_diaria = cargo_empresa.valor_contrato_diaria
        self.valor_pago_diaria = cargo_empresa.valor_pago_diaria
        self.data = datetime(year=ano, month=mes, day=dia)
        self.hora_entrada = hora_entrada
        self.minutos_entrada = minutos_entrada
        self.hora_saida = hora_saida
        self.inicio_hora_intervalo = inicio_hora_intervalo
        self.inicio_minutos_intervalo = inicio_minutos_intervalo
        self.final_hora_intervalo = final_hora_intervalo
        self.final_minutos_intervalo = final_minutos_intervalo
        self.minutos_saida = minutos_saida
        self.eh_dia_extra = eh_dia_extra

        # Calculo de minutos trabalhados no dia
        if hora_entrada < hora_saida:
            minutos_trabalhado = (hora_saida - hora_entrada) * 60

        if hora_entrada > hora_saida:
            minutos_trabalhado = (24 - hora_entrada) * 60
            minutos_trabalhado += (hora_saida) * 60

        # Minutos trabalhados incluindo o intervalo
        minutos_trabalhado += (minutos_saida - minutos_entrada)

        # Cálculo do intervalo para refeição
        minutos_intervalo = (final_hora_intervalo - inicio_hora_intervalo) * 60
        minutos_intervalo += (final_minutos_intervalo - inicio_minutos_intervalo)

        jornada_em_minutos_corridos = hora_entrada * 60 + minutos_entrada + minutos_trabalhado

        # Minutos trabalhados menos o intervalo para refeição
        minutos_trabalhado = minutos_trabalhado - minutos_intervalo

        if jornada_em_minutos_corridos > 1320:
            minutos_noturno = jornada_em_minutos_corridos - 1320

        if inicio_hora_intervalo >= 22:
            minutos_noturno = minutos_noturno - minutos_intervalo

        if minutos_trabalhado > 480:
            minutos_extras = minutos_trabalhado - 480

        if eh_dia_extra:
            minutos_extras = minutos_trabalhado

        valor_a_receber = (cargo_empresa.valor_contrato_diaria / 480) * minutos_trabalhado
        valor_a_receber += (cargo_empresa.valor_contrato_diaria / 480) * minutos_extras * 0.5
        valor_a_receber += (cargo_empresa.valor_contrato_diaria / 480) * minutos_noturno * 0.2

        valor_a_pagar = (cargo_empresa.valor_pago_diaria / 480) * minutos_trabalhado
        valor_a_pagar += (cargo_empresa.valor_pago_diaria / 480) * minutos_extras * 0.5
        valor_a_pagar += (cargo_empresa.valor_pago_diaria / 480) * minutos_noturno * 0.2

        self.valor_a_receber = valor_a_receber
        self.valor_a_pagar = valor_a_pagar
        self.minutos_extras = minutos_extras
        self.minutos_noturno = minutos_noturno

        self.data_insercao = datetime.now(timeZone)