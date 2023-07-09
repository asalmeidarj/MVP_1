from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from  model import Base

import pytz


class Funcionario(Base):
    __tablename__ = 'funcionario'

    id = Column("pk_funcionario", Integer, primary_key=True)
    nome = Column(String(40))
    cpf = Column(String(14), unique=True)
    telefone = Column(String(12))
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
            cpf:str,
            telefone:str,
            logradouro:str = None,
            numero:str = None,
            complemento:str = None,
            bairro:str = None,
            cidade:str = None,
            estado:str = None
    ):
        """
        Cria um Funcionário

        Arguments:
            nome: nome da funcionário.
            cnpj: cnpj da funcionário.
            descricao: descrição da funcionário.
            logradouro: logradouro da funcionário.
            numero: numero da funcionário.
            complemento: complemento da funcionário.
            bairro: bairro da funcionário.
            cidade: cidade da funcionário.
            estado: estado da funcionário.
            data_insercao: data de quando o funcionário foi inserido à base.
        """

        timeZone = pytz.timezone('America/Sao_Paulo')

        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.logradouro = logradouro
        self.numero = numero
        self.complemento = complemento
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.data_insercao = datetime.now(timeZone)