import os
import requests
import json
import pandas as pd
import configGranatum

from datetime import date
from wsgiref import headers

class GranatumAPI:
  def __init__(self):
    print('Iniciando requisições a API da Granatum...')
    self.data = date.today().strftime('%d-%m-%Y')
    self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    self.access_token = (configGranatum.token)
    self.run()

  def cria_diretorio(self, caminho):
    if not os.path.isdir(caminho):
        os.mkdir(caminho)
    print('Diretório Criado!')


  def request_lancamentos(self):
    print('Fazendo requisição dos lançamentos...')
    id_conta_bancaria = 'all'
    urlLancamentos = 'https://api.granatum.com.br/v1/lancamentos?access_token=' + str(self.access_token) +'&conta_id=' + str(id_conta_bancaria) 

    '''curl -i -X GET \
      -H "Content-Type:application/x-www-form-urlencoded" \
      'https://api.granatum.com.br/v1/lancamentos?access_token=token_cliente_granatum&conta_id=[conta_bancaria_id]'''

    #requisição da parte financeira - Listando lançamentos
    rLancamentos = requests.get( urlLancamentos, headers=self.headers )
    dataLancamentos = json.loads(rLancamentos._content.decode('utf-8'))
    self.idsCategoria = []
    for lista in dataLancamentos:
        if lista['categoria_id'] not in self.idsCategoria:
            self.idsCategoria.append(lista['categoria_id'])
            print('adicionando IDs a lista de categorias')

    df = pd.DataFrame(dataLancamentos, columns = ['id','grupo_id','lancamento_transferencia_id','categoria_id','centro_custo_lucro_id','tipo_custo_nivel_producao_id', 'tipo_custo_apropriacao_produto_id','conta_id','forma_pagamento_id','pessoa_id','tipo_lancamento_id','descricao','tipo_documento_id','documento','status', 'infinito',  'data_vencimento',  'data_pagamento',  'data_competencia',  'observacao',  'pagamento_automatico',  'numero_repeticao',  'total_repeticoes',  'periodicidade',  'pedido_id',  'lancamento_composto_id',  'wgi_usuario_id',  'itens_adicionais',  'tags',  'anexos',  'modified',  'valor',  'nfe_id'])    
    df.to_excel(configGranatum.caminho_lancamentos)

    print('Consulta lançamento finalizada, arquivo salvo.')


  def request_fornecedores(self):
    print('Fazendo requisição dos forneceores...')
    #requisição - Listando Fornecedores
    '''curl -i -X GET \
      -H "Content-Type:application/x-www-form-urlencoded" \
      -d 'considerar_inativos=true' \
      'https://api.granatum.com.br/v1/fornecedores?access_token=token_cliente_granatum'''
      
    urlFornecedores = 'https://api.granatum.com.br/v1/fornecedores?access_token=' + str(self.access_token)

    rFornecedores = requests.get( urlFornecedores, headers=self.headers )
    dataFornecedores = json.loads(rFornecedores._content.decode('utf-8'))

    df = pd.DataFrame(dataFornecedores, columns=['id',  'nome',  'nome_fantasia',  'documento',  'inscricao_estadual',  'inscricao_municipal',  'telefone',  'endereco',  'endereco_numero',  'endereco_complemento',  'bairro',  'cep',  'cidade_id',  'estado_id',  'email',  'observacao',  'banco_id',  'agencia',  'numero_conta',  'ativo',  'fornecedor',  'cliente',  'classificacao_cliente_id',  'classificacao_fornecedor_id',  'estado',  'cidade',  'anexos' ])    
    df.to_excel(configGranatum.caminho_fornecedores)

    print('Consulta fornecedores finalizada, arquivo salvo.')


  def requisitando_categotias(self):
    print('Fazendo requisição geral das categorias...')
    #requisição - Listando Categorias

    '''$ curl -i -X GET \
      -H "Content-Type:application/x-www-form-urlencoded" \
      'https://api.granatum.com.br/v1/categorias?access_token=token_cliente_granatum'''

    urlCategorias = 'https://api.granatum.com.br/v1/categorias?access_token=' + str(self.access_token)

    #request categorias geral
    rCategorias = requests.get( urlCategorias, headers=self.headers )
    dataGeralCategorias = json.loads(rCategorias._content.decode('utf-8'))

    #salvando em excel
    df = pd.DataFrame(dataGeralCategorias, columns=['id','descricao', 'cor', 'wgi_usuario_id','ativo','categorias_filhas' ] )
    df.to_excel(configGranatum.caminho_categorias_geral)


    #requisição individual - Categorias

    '''$ curl -i -X GET \
      -H "Content-Type:application/x-www-form-urlencoded" \
      'https://api.granatum.com.br/v1/categorias/43?access_token=token_cliente_granatum'''

    #usando lista de id's
    categoria_id = self.idsCategoria
    categoria = []

    #percorrendo lista
    for id in categoria_id:
      urlCategoriaIndividual = 'https://api.granatum.com.br/v1/categorias/' + str(id) + '?access_token=' + str(self.access_token)
      rCategoriaIndividual = requests.get( urlCategoriaIndividual, headers=self.headers )
      data = json.loads(rCategoriaIndividual._content.decode('utf-8'))
      categoria.append(data)

    #salvando em excel
    df = pd.DataFrame(categoria, columns = ['id','descricao','cor','parent_id', 'ativo','categorias_filhas'])    
    df.to_excel(configGranatum.caminho_categorias_detalhes)

    print('consulta categorias finalizada, arquivos salvos')


  def run(self):
    self.cria_diretorio(configGranatum.caminho)
    self.request_lancamentos()
    self.requisitando_categotias()



if __name__ == "__main__":
  GranatumAPI().__init__()
  #self = GranatumAPI()