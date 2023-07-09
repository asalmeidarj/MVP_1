from email.mime import base
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError

from flask_openapi3 import Info, Tag
from flask_openapi3 import OpenAPI
from flask_cors import CORS
from flask import redirect, request
from model import Session, Empresa, Cargo, Cargo_empresa, Funcionario
from logger import logger
from schemas import *


info = Info(title="API de controle de contratos terceirizados", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
empresa_tag = Tag(name="Empresa", description="Adição, visualização e remoção de empresas à base")
cargo_tag = Tag(name="Cargo", description="Adição, visualização e remoção de cargos à base")
cargo_empresa_tag = Tag(name="Cargo_empresa", description="Adição, visualização e remoção de cargos da empresa à base")
funcionario_tag = Tag(name="Funcionario", description="Adição, visualização e remoção de funcionarios à base")


@app.get('/')
def home():
    return redirect('/openapi')


@app.post('/empresa', tags=[empresa_tag],
          responses={"200": EmpresaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_empresa(body: EmpresaBodySchema):
    """Adiciona um novo Empresa à base de dados

    Retorna uma representação da empresa.
    """
    session = Session()
    empresa = Empresa(
        nome=body.nome.upper(),
        cnpj=body.cnpj,
        cidade=body.cidade.upper(),
        bairro=body.bairro.upper(),
        complemento=body.complemento.upper(),
        estado=body.estado.upper(),
        logradouro=body.logradouro.upper(),
        numero=body.numero,    
        descricao=body.descricao
    )
     
    logger.debug(f"Adicionando empresa de nome: '{empresa.nome}'")
    try:
        # adicionando empresa
        session.add(empresa)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado empresa de nome: '{empresa.nome}'")
        return apresenta_empresa(empresa), 200
    except IntegrityError as e:
        error_msg = "Empresa de mesmo cnpj já salvo na base :/"
        logger.warning(f"Erro ao adicionar empresa '{empresa.nome}', {error_msg}")
        return {"mesage": error_msg}, 409
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar empresa '{empresa.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/empresa', tags=[empresa_tag],
         responses={"200": EmpresaViewSchema, "404": ErrorSchema})
def get_empresa(query: EmpresaBuscaSchema):
    """Faz a busca por um Empresa a partir do id do empresa

    Retorna uma representação dos empresas.
    """
    empresa_id = query.id
    logger.debug(f"Coletando dados sobre empresa #{empresa_id}")
    session = Session()
    empresa = session.query(Empresa).filter(Empresa.id == empresa_id).first()
    if not empresa:
        error_msg = "Empresa não encontrada na base :/"
        logger.warning(f"Erro ao buscar empresa '{empresa_id}', {error_msg}")
        return {"mesage": error_msg}, 400
    else:
        logger.debug(f"Empresa econtrado: '{empresa.nome}'")
        return apresenta_empresa(empresa), 200


@app.get('/empresas', tags=[empresa_tag],
         responses={"200": EmpresaListaViewSchema, "404": ErrorSchema})
def get_empresas():
    """Lista todos os empresas cadastrados na base

    Retorna uma lista de representações de empresas.
    """
    logger.debug(f"Coletando lista de empresas")
    session = Session()
    empresas = session.query(Empresa).all()
    print(empresas)
    if not empresas:
        error_msg = "Empresa não encontrada na base :/"
        logger.warning(f"Erro ao buscar por lista de empresas. {error_msg}")
        return {"mesage": error_msg}, 400
    else:
        logger.debug(f"Retornando lista de empresas")
        return apresenta_lista_empresa(empresas), 200


@app.delete('/empresa', tags=[empresa_tag],
            responses={"200": EmpresaDelSchema, "404": ErrorSchema})
def del_empresa(query: EmpresaBuscaSchema):
    """Deleta um Empresa a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    empresa_id = query.id
    empresa_nome = query.nome

    logger.debug(f"Deletando dados sobre empresa #{empresa_id}")
    session = Session()

    if empresa_id:
        count = session.query(Empresa).filter(Empresa.id == empresa_id).delete()
    else:
        count = session.query(Empresa).filter(Empresa.nome == empresa_nome.upper()).delete()

    session.commit()
    if count:
        logger.debug(f"Deletado empresa #{empresa_id}")
        return {"mesage": "Empresa removida", "id": empresa_id}
    else: 
        error_msg = "Empresa não encontrado na base :/"
        logger.warning(f"Erro ao deletar empresa #'{empresa_id}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.post('/cargo', tags=[cargo_tag],
          responses={"200": CargoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_cargo(body: CargoBodySchema):
    """Adiciona um novo Cargo à base de dados

    Retorna uma representação do cargo.
    """
    session = Session()
    cargo = Cargo(nome=body.nome.upper())
     
    logger.debug(f"Adicionando cargo de nome: '{cargo.nome}'")
    try:
        # adicionando cargo
        session.add(cargo)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado cargo de nome: '{cargo.nome}'")
        return apresenta_cargo(cargo), 200
    except IntegrityError as e:
        error_msg = "Cargo de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar cargo '{cargo.nome}', {error_msg}")
        return {"mesage": error_msg}, 409
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar cargo '{cargo.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/cargo', tags=[cargo_tag],
         responses={"200": CargoViewSchema, "404": ErrorSchema})
def get_cargo(query: CargoBuscaSchema):
    """Faz a busca por um cargo a partir do id do cargo

    Retorna uma representação dos cargos.
    """
    cargo_id = query.id
    logger.debug(f"Coletando dados sobre cargo #{cargo_id}")
    session = Session()
    cargo = session.query(Cargo).filter(Cargo.id == cargo_id).first()
    if not cargo:
        error_msg = "Cargo não encontrada na base :/"
        logger.warning(f"Erro ao buscar cargo '{cargo_id}', {error_msg}")
        return {"mesage": error_msg}, 400
    else:
        logger.debug(f"Cargo encontrado: '{cargo.nome}'")
        return apresenta_cargo(cargo), 200


@app.get('/cargos', tags=[cargo_tag],
         responses={"200": CargoListaViewSchema, "404": ErrorSchema})
def get_cargos():
    """Lista todos os cargos cadastrados na base

    Retorna uma lista de representações de cargos.
    """
    logger.debug(f"Coletando lista de cargos")
    session = Session()
    cargos = session.query(Cargo).all()
    if not cargos:
        error_msg = "Cargo não encontrada na base :/"
        logger.warning(f"Erro ao buscar por lista de cargos. {error_msg}")
        return {"mesage": error_msg}, 400
    else:
        logger.debug(f"Retornando lista de cargos")
        return apresenta_lista_cargo(cargos), 200


@app.delete('/cargo', tags=[cargo_tag],
            responses={"200": CargoDelSchema, "404": ErrorSchema})
def del_cargo(query: CargoBuscaSchema):
    """Deleta um Cargo a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    cargo_id = query.id
    cargo_nome = query.nome

    logger.debug(f"Deletando dados sobre cargo #{cargo_id}")
    session = Session()

    if cargo_id:
        count = session.query(Cargo).filter(Cargo.id == cargo_id).delete()
    else:
        count = session.query(Cargo).filter(Cargo.nome == cargo_nome.upper()).delete()

    session.commit()
    if count:
        logger.debug(f"Deletado cargo #{cargo_id}")
        return {"mesage": "Cargo removido", "id": cargo_id}
    else: 
        error_msg = "Cargo não encontrado na base :/"
        logger.warning(f"Erro ao deletar cargo #'{cargo_id}', {error_msg}")
        return {"mesage": error_msg}, 400
    
@app.post('/cargo_empresa', tags=[cargo_empresa_tag],
          responses={"200": CargoEmpresaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_cargo_empresa(body: CargoEmpresaBodySchema):
    """Adiciona um novo Cargo da empresa à base de dados

    Retorna uma representação do cargo.
    """
    session = Session()

    cargo = None
    empresa = None
    if body.cargo_id and body.empresa_id:
        cargo = session.query(Cargo).filter(Cargo.id == body.cargo_id).first()
        empresa = session.query(Empresa).filter(Empresa.id == body.empresa_id).first()

    
    cargo_empresa = Cargo_empresa(
        empresa=empresa,
        cargo=cargo,
        valor_contrato_diaria=body.valor_contrato_diaria,
        valor_pago_diaria=body.valor_pago_diaria,
        uq_cargo_empresa_id=f"{str(body.cargo_id)}-{str(body.empresa_id)}"
    )

 
    logger.debug(f"Adicionando cargo de nome: '{cargo_empresa.cargo}'")
    try:
        # adicionando cargo
        session.add(cargo_empresa)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado cargo de nome: '{cargo_empresa.cargo.nome}'")
        return apresenta_cargo_empresa(cargo_empresa), 200
    except IntegrityError as e:
        error_msg = "Cargo de mesmo nome já salvo na base para esta empresa:/"
        logger.warning(f"Erro ao adicionar cargo, {error_msg}")
        return {"mesage": error_msg}, 409
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar cargo, {error_msg}")
        return {"mesage": error_msg}, 400

@app.get('/cargo_empresa', tags=[cargo_empresa_tag],
         responses={"200": CargoEmpresaViewSchema, "404": ErrorSchema})
def get_cargo_empresa(query: CargoEmpresaBuscaSchema):
    """Faz a busca por um cargo a partir do id do cargo

    Retorna uma representação dos cargos.
    """
    cargo_id = query.cargo_id
    empresa_id = query.empresa_id

    logger.debug(f"Coletando dados sobre cargo #{cargo_id}")
    session = Session()
    cargo_empresa = session.query(Cargo_empresa).filter(Cargo_empresa.cargo_id == cargo_id, Cargo_empresa.empresa_id == empresa_id).first()
    if not cargo_empresa:
        error_msg = "Cargo não encontrada na base :/"
        logger.warning(f"Erro ao buscar cargo '{cargo_id}', {error_msg}")
        return {"mesage": error_msg}, 400
    else:
        logger.debug(f"Cargo encontrado: '{cargo_empresa.cargo.nome}'")
        return apresenta_cargo_empresa(cargo_empresa), 200


@app.post('/funcionario', tags=[funcionario_tag],
          responses={"200": FuncionarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_funcionario(body: FuncionarioBodySchema):
    """Adiciona um novo Funcionario à base de dados

    Retorna uma representação do Funcionario.
    """
    session = Session()
    
    funcionario = Funcionario(
        nome=body.nome.upper(),
        cpf=body.cpf,
        telefone=body.telefone,
        cidade=body.cidade.upper(),
        bairro=body.bairro.upper(),
        complemento=body.complemento.upper(),
        estado=body.estado.upper(),
        logradouro=body.logradouro.upper(),
        numero=body.numero
    )
     
    logger.debug(f"Adicionando funcionario de nome: '{funcionario.nome}'")
    try:
        # adicionando funcionario
        session.add(funcionario)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado funcionario de nome: '{funcionario.nome}'")
        return apresenta_funcionario(funcionario), 200
    except IntegrityError as e:
        error_msg = "Funcionario de mesmo cpf já salvo na base :/"
        logger.warning(f"Erro ao adicionar funcionario '{funcionario.nome}', {error_msg}")
        return {"mesage": error_msg}, 409
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar funcionario '{funcionario.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/funcionario', tags=[funcionario_tag],
         responses={"200": FuncionarioViewSchema, "404": ErrorSchema})
def get_funcionario(query: FuncionarioBuscaSchema):
    """Faz a busca por um funcionario a partir do id do funcionario.

    Retorna uma representação dos funcionarios.
    """
    funcionario_id = query.id
    logger.debug(f"Coletando dados sobre funcionario #{funcionario_id}")
    session = Session()
    funcionario = session.query(Funcionario).filter(Funcionario.id == funcionario_id).first()
    if not funcionario:
        error_msg = "Funcionario não encontrada na base :/"
        logger.warning(f"Erro ao buscar cargo '{funcionario_id}', {error_msg}")
        return {"mesage": error_msg}, 400
    else:
        logger.debug(f"Funcionario encontrado: '{funcionario.nome}'")
        return apresenta_funcionario(funcionario), 200