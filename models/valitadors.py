# -*- coding: utf-8 -*-
## Validadores de Carros
Carros.placa.requires = [IS_MATCH('^(.+)(-\d{4})?$', error_message='AAA-0000'),
IS_NOT_IN_DB(db, 'carros.placa')]
Carros.chassi.requires = [IS_NOT_EMPTY(),
IS_NOT_IN_DB(db, 'carros.chassi')]
Carros.data_entrada.requires = IS_DATE(format='%d-%m-%Y')
Carros.ano.requires = IS_MATCH('^\d{4}?$', error_message='YYYY')
Carros.modelo.requires = IS_NOT_EMPTY()
Carros.renavan.requires = [ IS_MATCH('^\d{11}?$', error_message='renavan possui 11 dígitos númericos'),
IS_NOT_IN_DB(db, 'carros.renavan')]
Carros.cor.requires = IS_NOT_EMPTY()
Carros.ultimo_proprietario.requires =  IS_IN_DB(db, 'clientes.id', '%(nome)s %(s_nome)s  %(cpf)s')

## Validadores de venda
CarrosVendidos.carro.requires = IS_IN_DB(db, 'carros.id', '%(placa)s')
CarrosVendidos.data_venda.requires = IS_DATE(format='%d-%m-%Y')
CarrosVendidos.comprador.requires = IS_IN_DB(db, 'clientes.id', '%(nome)s %(s_nome)s %(cpf)s')
CarrosVendidos.vendedor.requires = IS_IN_DB(db, 'auth_user.id', '%(first_name)s %(last_name)s')
CarrosVendidos.forma_pagamento.requires = IS_IN_SET(['Cheque', 'Ted', 'Financiamento', 'Promissória'])
CarrosVendidos.valor_venda.requires = IS_NOT_EMPTY()
CarrosVendidos.comissao.requires = IS_NOT_EMPTY()

##Validadores de Estoque
CarrosEstoque.carro.requires = IS_IN_DB(db, 'carros.id', '%(placa)s')
CarrosEstoque.despesa_total.requires = IS_NOT_EMPTY()
CarrosEstoque.valor_compra.requires = IS_NOT_EMPTY()


##Validadores de Consignados
CarrosConsig.carro.requires = IS_IN_DB(db, 'carros.id', '%(placa)s')

## Validadores de financiamento
CarrosFinanciados.carro.requires = IS_IN_DB(db, 'carros.id', '%(placa)s')
CarrosFinanciados.banco.requires = IS_NOT_EMPTY()

## Validadores de Cliente
Clientes.cpf.requires = [IS_MATCH('^\d{3}(.\d{3})(.\d{3})(-\d{2})?$', error_message='000.000.000-00'),
IS_NOT_IN_DB(db, 'clientes.cpf')]
Clientes.nome.requires = IS_NOT_EMPTY()
Clientes.s_nome.requires = IS_NOT_EMPTY()
Clientes.telefone.requires = IS_MATCH('^\d{2}(-\d{9})?$', error_message='00-000000000')
Clientes.rua.requires = IS_NOT_EMPTY()
Clientes.numero.requires = IS_NOT_EMPTY()
Clientes.cidade.requires = IS_NOT_EMPTY()
Clientes.bairro.requires = IS_NOT_EMPTY()
Clientes.cep.requires = requires = IS_MATCH('^\d{5}(-\d{3})?$', error_message='00000-000')
Clientes.uf.requires = IS_IN_SET(['AC','AL','AP','AM','BA','CE','DF','ES','GO', 'MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO'])
Clientes.email.requires = IS_EMAIL(error_message='invalid email!')

##Validadores de Despesas
Despesas.carro.requires = IS_IN_DB(db, 'carros.id', '%(placa)s')
Despesas.despesa.requires = IS_NOT_EMPTY()
Despesas.valor_despesa.requires = IS_NOT_EMPTY()
