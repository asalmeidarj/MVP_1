from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime

from  model import Base

import pytz


class Cargo(Base):
    __tablename__ = 'cargo'

    id = Column("pk_cargo", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    data_insercao = Column(DateTime, default=datetime.now())

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