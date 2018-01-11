# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Bem Vindo a RAFA veículos!")
    return dict(message=T('Welcome to web2py!'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


##FORM cadastros

@auth.requires_login()
def novo_carro():
    form = SQLFORM(Carros)
    if form.process().accepted:
        session.flash = 'Novo carro cadastrado: %s' % form.vars.placa
        redirect(URL('novo_estoque', vars=dict(carro=form.vars.id)))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)


@auth.requires_login()
def novo_cliente():
    form = SQLFORM(Clientes)
    if form.process().accepted:
        session.flash = 'Novo cliente cadastrado: %s' % form.vars.cpf
        redirect(URL('novo_cliente'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)

def somaDespesa(carro):
    soma = 0.0
    rows = db(db.despesas.carro == carro).select()
    for row in rows:
        soma=soma+row.valor_despesa
    return soma

@auth.requires_login()
def nova_despesa():
    rows = db(request.args(0) == db.carros_estoque.id).select()
    for row in rows:
        db.despesas.carro.default = row.carro
        carro=row.carro

    db.despesas.carro.writable = False
    db.despesas.carro.readable = False

    form = SQLFORM(Despesas)  
    if form.process().accepted:
        
        despesa_total = somaDespesa(carro)
        db(db.carros_estoque.carro == carro).update(despesa_total=despesa_total)

        session.flash = 'Nova despesa cadastrada'
        redirect(URL('nova_despesa', args=request.args(0)))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)

def calculaLucro(carro):
    soma = 0.0
    rows = db(carro == db.carros_estoque.carro).select()
    for row in rows:
        soma = soma+row.despesa_total+row.valor_compra

    rows = db(carro == db.carros_vendidos.carro).select()
    for row in rows:
        soma = soma+row.comissao

    rows = db(carro == db.carros_vendidos.carro).select()
    for row in rows:
        soma = row.valor_venda-soma
    return soma

@auth.requires_login()
def nova_venda():
    form = SQLFORM(CarrosVendidos)
    rows = db(request.args(0) == db.carros_estoque.id).select()
    for row in rows:
        form.vars.carro =row.carro
    carro= form.vars.carro
    if form.process().accepted:   
        lucro = calculaLucro(form.vars.carro)

        db(db.carros_vendidos.carro == carro).update(lucro=lucro)
        db(db.carros_estoque.carro == carro).delete()
        session.flash = 'Nova venda cadastrada!'
        if(form.vars.forma_pagamento == 'Financiamento'):
            redirect(URL('novo_financiamento',vars=dict(carro=form.vars.carro)))
        else:
            redirect(URL('index'))

    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)

@auth.requires_login()
def novo_estoque():
    form = SQLFORM(CarrosEstoque)
    form.vars.carro = request.vars.carro
    if form.process().accepted:
        session.flash = 'Carro cadastrado no estoque'
        redirect(URL('novo_carro'))
    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'

    return dict(form=form)

@auth.requires_login()
def novo_consignado():
    form = SQLFORM(CarrosConsig)
    form.vars.carro = request.vars.carro
    if form.process().accepted:
        session.flash = 'Novo Carro consignado cadastrado: %s' % form.vars.carro
        redirect(URL('novo_carro'))

    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'
    return dict(form=form)


def atualizaLucro(carro, retorno, retorno_vendedor):
    soma = 0.0
    rows = db(carro == db.carros_vendidos.carro).select()
    for row in rows:
        soma=soma+row.lucro
    lucro = soma+retorno-retorno_vendedor
    return lucro

@auth.requires_login()
def novo_financiamento():
    form = SQLFORM(CarrosFinanciados)
    form.vars.carro = request.vars.carro
    if form.process().accepted:
        
        carro = form.vars.carro
        retorno = float(form.vars.retorno)
        retorno_vendedor = float(form.vars.retorno_vendedor)
        lucro = atualizaLucro(carro, retorno, retorno_vendedor)

        db(db.carros_vendidos.carro == carro).update(lucro=lucro)
        session.flash = 'Novo Financiamento cadastrado'
        redirect(URL('ver_estoque'))

    elif form.errors:
        response.flash = 'Erros no formulário!'
    else:
        if not response.flash:
            response.flash = 'Preencha o formulário!'

    return dict(form=form)

##FORM consulta
@auth.requires_login()
def ver_carros():
    db.carros.id.writable = False
    db.carros.id.readable = False
    
    fields=[db.carros.placa, db.carros.ano, db.carros.modelo, db.carros.renavan, db.carros.chassi,
            db.carros.cor, db.carros.data_entrada, db.carros.chave_reserva,
            db.carros.manual_carro, db.carros.multa, db.clientes.nome, db.clientes.s_nome,
            db.clientes.cpf]
    
    grid = SQLFORM.grid(Carros,
                        fields = fields,
                        left=db.clientes.on(db.carros.ultimo_proprietario == db.clientes.id),
                        headers = {'clientes.nome' : 'Último Proprietário',
                                    'clientes.s_nome': ''},
                        create = False,
                        editable = False)

    return dict(grid=grid)

@auth.requires_login()
def ver_clientes():
    db.clientes.id.writable = False
    db.clientes.id.readable = False

    grid = SQLFORM.grid(Clientes, 
                        create = False,
                        editable = False,
                        deletable = False)
    
    return dict(grid=grid)

@auth.requires_login()
def ver_vendas():
    db.carros_vendidos.id.writable = False
    db.carros_vendidos.id.readable = False

    fields = [db.carros.placa, db.carros.modelo, db.carros_vendidos.data_venda, 
              db.carros_vendidos.comissao, db.carros_vendidos.valor_venda, 
              db.carros_vendidos.forma_pagamento, db.carros_vendidos.lucro, 
              db.clientes.nome, db.clientes.s_nome, db.auth_user.first_name, 
              db.auth_user.last_name]
    
    grid = SQLFORM.grid(CarrosVendidos,
                        left=[db.carros.on(db.carros_vendidos.carro == db.carros.id), 
                                db.clientes.on(db.carros_vendidos.comprador == db.clientes.id),
                                db.auth_user.on(db.carros_vendidos.vendedor == db.auth_user.id)],
                        fields = fields,
                        create = False,
                        editable = False,
                        deletable = False)

    return dict(grid=grid)

@auth.requires_login()
def ver_estoque():
    db.carros_estoque.id.writable = False
    db.carros_estoque.id.readable = False

    links= [ lambda row:A(T('VENDER'),
                            _class="button btn btn-default",
                            _href=URL('default','nova_venda',user_signature=True,args=row.get('carros_estoque', row).id)),
             lambda row:A(T('DESPESAS'),
                            _class="button btn btn-default",
                            _href=URL('default','ver_despesas',user_signature=False,args=row.get('carros_estoque', row).id)),
             lambda row:A(T('ADICIONAR DESPESA'),
                            _class="button btn btn-default",
                            _href=URL('default','nova_despesa',user_signature=True,args=row.get('carros_estoque', row).id))]

    fields = [db.carros.placa, db.carros.data_entrada,
                db.carros_estoque.valor_compra, db.carros_estoque.despesa_total]
    grid = SQLFORM.grid(db.carros_estoque,
                        left = db.carros.on(db.carros_estoque.carro == db.carros.id),
                        fields = fields,
                        create = False,
                        deletable = False,
                        editable = False,
                        links=links)

    return dict(grid=grid)

@auth.requires_login()
def ver_consig():
    grid = SQLFORM.grid(CarrosConsig,
                        left=db.carros.on(db.carros_consig.carro == db.carros.id),
                        create = False,
                        editable = False,
                        deletable = False)

    return dict(grid=grid)

@auth.requires_login()
def ver_despesas():
    rows = db(request.args(0) == db.carros_estoque.id).select()
    for row in rows:
            carro = row.carro
    query = ((db.despesas.carro == carro))

    fields = [db.carros.placa, db.carros.modelo, db.despesas.despesa,
                db.despesas.valor_despesa]
    grid = SQLFORM.grid(query,
                        left=db.carros.on(db.despesas.carro == db.carros.id),
                        create = False,
                        fields = fields,
                        deletable = False,
                        editable = False,
                        user_signature=False)

    return dict(grid=grid)

@auth.requires_login()
def ver_financiados():
    grid = SQLFORM.grid(CarrosFinanciados)
    return dict(grid=grid)