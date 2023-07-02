from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from typing import Union

from  model import Base


class Empresa(Base):
    __tablename__ = 'empresa'

    id = Column("pk_empresa", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    descricao = Column(String(4000))
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, nome:str, descricao:str, data_insercao:Union[DateTime, None] = None):
        """
        Cria uma Empresa

        Arguments:
            nome: nome da empresa.
            descricao: descrição da empresa.
            data_insercao: data de quando o empresa foi inserido à base
        """
        self.nome = nome
        self.descricao = descricao
        if data_insercao:
            self.data_insercao = data_insercao