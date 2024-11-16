import streamlit as st
import requests as rq
import pandas as pd
import plotly.express as pl

def formata_numero(valor, prefixo = ''):
    for unidade in ['', 'mil']:
        if valor <1000:
            return f'{prefixo} {valor:.2f} {unidade}'
        valor /= 1000
    return f'{prefixo} {valor:.2f} milhões'

st.title("Dashboard de Vendas :shopping_trolley:")


url = 'https://labdados.com/produtos'
response = rq.get(url)
dados = pd.DataFrame.from_dict(response.json())

## Tabelas
receita_estados = dados.groupby('Local da compra')[['Preço']].sum()

receita_categorias = dados.groupby('Categoria do Produto')[['Preço']].sum().sort_values('Preço', ascending=False)

receita_estados = dados.drop_duplicates(subset = 'Local da compra')[['Local da compra', 'lat', 'lon']].merge(receita_estados, left_on = 'Local da compra', right_index = True).sort_values('Preço', ascending = False)

## Gráficos
fig_mapa_receita = pl.scatter_geo(receita_estados,
                                   lat = 'lat',
                                   lon = 'lon',
                                   scope = 'south america',
                                   size = 'Preço',
                                   template = 'seaborn',
                                   hover_name = 'Local da compra',
                                   hover_data = {'lat':False,'lon':False},
                                   title = 'Receita por Estado')

fig_receita_estados = pl.bar(receita_estados.head(),
                                            x = 'Local da compra',
                                            y = 'Preço',
                                            text_auto = True,
                                            title = 'Top estados')

fig_receita_estados.update_layout(yaxis_title = 'Receita')

fig_receita_categorias = pl.bar(receita_categorias, text_auto = True, title = 'Receita por categoria')

fig_receita_categorias.update_layout(yaxis_title = 'Receita')


coluna1, coluna2 = st.columns(2)
with coluna1:
    st.metric('Receita', formata_numero(dados['Preço'].sum(), 'R$'))
    st.plotly_chart(fig_mapa_receita, use_container_width = True)
    st.plotly_chart(fig_receita_estados, use_container_width = True)
with coluna2:
    st.metric('Quantidade de vendas', formata_numero(dados.shape[0]))
    #st.plotly_chart(fig_receita_mensal, use_container_width = True)
    st.plotly_chart(fig_receita_categorias, use_container_width = True)

#st.metric('Receita: ', dados['Preço'].sum())
#st.metric('Quantidade de vendas', dados.shape[0])

st.dataframe(dados)
