# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < "2.14.1":
    raise HTTP(500, "Requires web2py 2.13.3 or newer")

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# app configuration made easy. Look inside private/appconfig.ini
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
myconf = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(myconf.get('db.uri'),
             pool_size=myconf.get('db.pool_size'),
             migrate_enabled=myconf.get('db.migrate'),
             check_reserved=['all'])
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = ['*'] if request.is_local else []
# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------
response.formstyle = myconf.get('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.get('forms.separator') or ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

from gluon.tools import Auth, Service, PluginManager

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db)
service = Service()
plugins = PluginManager()

# -------------------------------------------------------------------------
# create all tables needed by auth if not custom tables
# -------------------------------------------------------------------------
auth.define_tables(username=False, signature=False)

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.get('smtp.server')
mail.settings.sender = myconf.get('smtp.sender')
mail.settings.login = myconf.get('smtp.login')
mail.settings.tls = myconf.get('smtp.tls') or False
mail.settings.ssl = myconf.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------
# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.
#
# More API examples for controllers:
#
# >>> db.mytable.insert(myfield='value')
# >>> rows = db(db.mytable.myfield == 'value').select(db.mytable.ALL)
# >>> for row in rows: print row.id, row.myfield
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# after defining tables, uncomment below to enable auditing
# -------------------------------------------------------------------------
# auth.enable_record_versioning(db)


Clientes = db.define_table('clientes',
    Field('cpf', 'string', label='CPF'),
    Field('nome', 'string', label='Nome'),
    Field('s_nome', 'string', label='Sobrenome'),
    Field('telefone', 'string', label='Telefone'),
    Field('rua', 'string', label='Rua'),
    Field('numero', 'integer', label='Número'),
    Field('cidade', 'string',default = 'Belo Horizonte', label='Cidade'),
    Field('bairro', 'string', label='Bairro'),
    Field('cep', 'string', label='CEP'),
    Field('uf', 'string',default = 'MG', label='Estado'),
    Field('email', 'string', label='E-mail')
)


Carros = db.define_table('carros',
    Field('placa', 'string', label='Placa:'),
    Field('ano', 'integer', label='Ano:'),
    Field('modelo', 'string', label='Modelo:'),
    Field('renavan', 'string', label='Renavan:'),
    Field('chassi', 'string', label='Chassi:'),
    Field('cor', 'string', label='Cor:'),
    Field('ultimo_proprietario', 'reference clientes', label='Ultimo Proprietário:'),
    Field('data_entrada', 'date',default=request.now, label='Data de Entrada:'),
    Field('Financiado', 'boolean', label='Financiado'),
    Field('chave_reserva', 'boolean', label='Chave Reserva'),
    Field('manual_carro', 'boolean', label='Manual'), 
    Field('multa', 'boolean', label='Multa')
    )

CarrosConsig = db.define_table('carros_consig',
    Field('carro', 'reference carros', label='Carro:'),
    Field('data_retirada', 'date', label='Data de Retirada:')
)

CarrosEstoque = db.define_table('carros_estoque',
    Field('carro', 'reference carros', label='Carro:'),
    Field('valor_compra', 'double', label='Valor de Compra R$:'),
    Field('despesa_total', 'double',writable=False, default=0, label='Despesa Total R$:')
)

CarrosVendidos = db.define_table('carros_vendidos',
    Field('carro', 'reference carros', label='Carro:'),
    Field('data_venda', 'date',default=request.now, label='Data de Venda:'),
    Field('comprador', 'reference clientes', label='Comprador:'),
    Field('comissao', 'double', label='Comissão R$:'),
    Field('valor_venda', 'double', label='Valor de venda R$:'),
    Field('forma_pagamento', 'string', label='Forma de pagamento: '),
    Field('vendedor', 'reference auth_user', label='Vendedor:'),
    Field('lucro', 'double', writable=False, default=0.0, label='Lucro R$:')
)

Despesas  = db.define_table('despesas',
    Field('carro', 'reference carros', label='Carro:'),
    Field('despesa', 'string', label='despesa:'),
    Field('valor_despesa', 'double', label='Valor R$:')
)

CarrosFinanciados = db.define_table('carros_financiados',
    Field('carro', 'reference carros', label='Carro:'),
    Field('banco', 'string', label='Banco:'),
    Field('retorno_vendedor', 'double',default = 0.0, label='Retorno do vendedor R$:'),
    Field('retorno', 'double',default =0.0, label='Retorno R$:')
)



