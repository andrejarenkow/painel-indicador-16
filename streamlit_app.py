import pandas as pd
import streamlit as st

@st.cache_data
def buscar_dados(persist=True):
  dados = pd.read_excel('cadastro_pop_sac_rs.xlsx')
  dados['Tipo da Forma de Abastecimento'] = dados['Tipo da Forma de Abastecimento'].str.strip()

  return dados

dados = pd.read_excel('cadastro_pop_sac_rs.xlsx')
dados['Tipo da Forma de Abastecimento'] = dados['Tipo da Forma de Abastecimento'].str.strip()
cadastro_populacao_abastecida = dados.copy()

ano = st.selectbox(label='Selecione o ano', options = sorted(cadastro_populacao_abastecida['Ano de referência'].unique()))

filtro_rs_sac = (cadastro_populacao_abastecida['Ano de referência']==ano)

cadastro_populacao_abastecida_sac = cadastro_populacao_abastecida[filtro_rs_sac].reset_index(drop=True)
cadastro_populacao_abastecida_sac['Número de economias residenciais (domicílios permanentes)'] = pd.to_numeric(cadastro_populacao_abastecida_sac['Número de economias residenciais (domicílios permanentes)'])
cadastro_populacao_abastecida_sac['Número de economias residenciais (de uso ocasional)'] = pd.to_numeric(cadastro_populacao_abastecida_sac['Número de economias residenciais (de uso ocasional)']).fillna(0)
cadastro_populacao_abastecida_sac['Razão habitantes/domicílio'] = pd.to_numeric(cadastro_populacao_abastecida_sac['Razão habitantes/domicílio'])
cadastro_populacao_abastecida_sac['populacao_abastecida'] = (cadastro_populacao_abastecida_sac['Número de economias residenciais (domicílios permanentes)'])*cadastro_populacao_abastecida_sac['Razão habitantes/domicílio']

municipios = pd.read_csv('https://raw.githubusercontent.com/andrejarenkow/csv/master/Munic%C3%ADpios%20RS%20IBGE6%20Popula%C3%A7%C3%A3o%20CRS%20Regional%20-%20P%C3%A1gina1.csv', sep=',')

tabela_pop = pd.pivot_table(cadastro_populacao_abastecida_sac, index='Código IBGE',
                            columns='Desinfecção', values='populacao_abastecida',
                            aggfunc='sum').fillna(0)
tabela_pop['porcentagem_tratado'] = (tabela_pop['Sim']/(tabela_pop['Sim']+tabela_pop['Não'])*100).round(2)
tabela_pop.reset_index(inplace=True)

tabela_regioes_pop = pd.merge(municipios, tabela_pop, left_on='IBGE6', right_on='Código IBGE')[['Município', 'Região_saude','CRS', 'Não',	'Sim']]
tabela_regioes_pop['total'] = tabela_regioes_pop['Sim']+tabela_regioes_pop['Não']
tabela_regioes_dinamica_pop = pd.pivot_table(tabela_regioes_pop, index='Região_saude', values=['Não',	'Sim',	'total'], aggfunc='sum')
tabela_regioes_dinamica_pop['porcentagem_tratada'] = (tabela_regioes_dinamica_pop['Sim']/tabela_regioes_dinamica_pop['total']*100).round(2)

tabela_regioes_dinamica_pop
