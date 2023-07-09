from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from  model import Base

import pytz


class Cargo(Base):
    __tablename__ = 'cargo'

    id = Column("pk_cargo", Integer, primary_key=True)
    nome = Column(String(40), unique=True)
    data_insercao = Column(DateTime, default=datetime.now())


    # Definição do relacionamento entre o cargo e o cargo_empresa.
    # Essa relação é implicita, não está salva na tabela 'cargo',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    cargo_empresas = relationship("Cargo_empresa")

    def __init__(
            self, 
            nome:str, 
    ):
        """
        Cria um Cargo

        Arguments:
            nome: nome do cargo.
            data_insercao: data de quando o cargo foi inserido à base
        """

        timeZone = pytz.timezone('America/Sao_Paulo')

        self.nome = nome
        self.data_insercao = datetime.now(timeZone)