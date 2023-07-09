from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
from datetime import datetime

from  model import Base, Cargo, Empresa

import pytz


class Cargo_empresa(Base):
    __tablename__ = 'cargo_empresa'

    id = Column("pk_cargo_empresa", Integer, primary_key=True) 
    cargo_id = Column(Integer, ForeignKey("cargo.pk_cargo"), nullable=False)
    cargo_nome = Column(String(40))
    empresa_id = Column(Integer, ForeignKey("empresa.pk_empresa"), nullable=False)
    empresa_nome = Column(String(40))
    cargo = relationship('Cargo')
    empresa = relationship('Empresa')
    valor_contrato_diaria = Column(Float)
    valor_pago_diaria = Column(Float)
    uq_cargo_empresa_id = Column(String(40), unique=True)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(
            self, 
            cargo: Cargo,
            empresa: Empresa,
            valor_contrato_diaria: float,
            valor_pago_diaria: float,
            uq_cargo_empresa_id: str
    ):
        """
        Cria um Cargo_empresa

        Arguments:
            nome: nome do cargo_empresa.
            data_insercao: data de quando o cargo_empresa foi inserido à base
        """

        timeZone = pytz.timezone('America/Sao_Paulo')

        self.cargo = cargo
        self.cargo_nome = cargo.nome
        self.empresa = empresa
        self.empresa_nome = empresa.nome
        self.valor_contrato_diaria = valor_contrato_diaria
        self.valor_pago_diaria = valor_pago_diaria
        self.uq_cargo_empresa_id = uq_cargo_empresa_id
        self.data_insercao = datetime.now(timeZone)