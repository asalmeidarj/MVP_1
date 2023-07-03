from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime

from  model import Base

import pytz


class Empresa(Base):
    __tablename__ = 'empresa'

    id = Column("pk_empresa", Integer, primary_key=True)
    nome = Column(String(140))
    cnpj = Column(String(14), unique=True)
    descricao = Column(String(4000))
    logradouro = Column(String(30))
    numero = Column(String(6))
    complemento = Column(String(50))
    bairro = Column(String(30))
    cidade = Column(String(20))
    estado = Column(String(20))
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(
            self, 
            nome:str, 
            cnpj:str, 
            descricao:str = None,
            logradouro:str = None,
            numero:str = None,
            complemento:str = None,
            bairro:str = None,
            cidade:str = None,
            estado:str = None,
    ):
        """
        Cria uma Empresa

        Arguments:
            nome: nome da empresa.
            descricao: descrição da empresa.
            data_insercao: data de quando o empresa foi inserido à base
        """

        timeZone = pytz.timezone('America/Sao_Paulo')

        self.nome = nome
        self.cnpj = cnpj
        self.descricao = descricao
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.data_insercao = datetime.now(timeZone)