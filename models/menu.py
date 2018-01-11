# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# Customize your APP title, subtitle and menus here
# ----------------------------------------------------------------------------------------------------------------------

response.logo = A(B(SPAN('RAFA '), 'automóveis'),
                  _class="navbar-brand", _href=URL("default","index"), _id="web2py-logo")
response.title = request.application.replace('_', ' ').title()
response.subtitle = ''

# ----------------------------------------------------------------------------------------------------------------------
# read more at http://dev.w3.org/html5/markup/meta.name.html
# ----------------------------------------------------------------------------------------------------------------------
response.meta.author = myconf.get('app.author')
response.meta.description = myconf.get('app.description')
response.meta.keywords = myconf.get('app.keywords')
response.meta.generator = myconf.get('app.generator')

# ----------------------------------------------------------------------------------------------------------------------
# your http://google.com/analytics id
# ----------------------------------------------------------------------------------------------------------------------

DEVELOPMENT_MENU = True

def _():
    # ------------------------------------------------------------------------------------------------------------------
    # shortcuts
    # ------------------------------------------------------------------------------------------------------------------
    
    response.menu += [
        ('Cadastros', False, '#', [
            (T('Cadastrar novo carro'), False,
             URL('default','novo_carro'), []),
            (T('Cadastrar novo cliente'), False,
             URL('default','novo_cliente'), []),
            (T('Cadastrar nova consignação'), False, 
             URL('default','novo_consignado'), []),           
        ]),
        (T('Carros'), False, '#', [
            (T('Todos os carros'), False, 
             URL('default','ver_carros'), []),
            LI(_class="divider"),
            (T('Estoque'), False,
             URL('default','ver_estoque'), []),
            (T('consignados'), False,
             URL('default','ver_consig'), []),
            (T('Vendidos'), False,
             URL('default','ver_vendas'),[]), 
             LI(_class="divider"),
            (T('financiados'), False, 
             URL('default','ver_financiados'), []),
        ]),
        (T('clientes'), False, URL('default','ver_clientes'), []),
    ]


if DEVELOPMENT_MENU:
    _()

if "auth" in locals():
    auth.wikimenu()