import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly import data
import numpy as np
from pathlib import Path


@st.cache_data
def carregar_dados():
    caminho_relativo = Path.cwd()
    pasta = caminho_relativo / Path('arquivos')
########## PASTA DADOS DE POTÊNCIA ################
    dados_producao = []
# df_prod = pd.read_excel(pasta_prod / Path('prod_AS_2022_1.xlsx'))
    for arquivo in pasta.iterdir():
        df = pd.read_excel(arquivo)
        dados_producao.append(df)
        df = pd.concat(dados_producao)
    return df

base = carregar_dados()

### MENUS ####

st.title("Dados Gerais por aerogerador")

coluna_esquerda, coluna_meio, coluna_direita = st.columns([1,1,1])

filtro_aero = [aero for aero in base['WTG'].unique()]
filtro_aero = sorted(filtro_aero)
aero = coluna_esquerda.selectbox("Aerogerador", filtro_aero)



# Calulando a disponibilidade
base['Disponibilidade'] = np.where(
        base[['Velocidade do vento [m/s]','Potência [kW]']].isna().any(axis=1),  # se vento ou potência for NaN
        np.nan,  # mantém vazio
        np.where((base['Potência [kW]'] <= 1) & (base['Velocidade do vento [m/s]'].between(2.5, 20)),0,1))

# Juntar colunas de tempo e converter para datetime
tempo_td = pd.to_timedelta(base["Tempo"].astype(str), errors="coerce")
base["DataHora"] = base["Data"] + tempo_td

df_tratado = base

df_tratado = df_tratado.set_index('DataHora')
df_tratado = df_tratado.sort_values(by="DataHora")
aerogerador = 'WTG 1'
df_tratado = df_tratado.loc[df_tratado['WTG'] == aero, :]

container = st.container(border = True)

with container:

    
    # grafico_area = px.area(base_disp, x="DataHora", y=aero+'_disp')

    layout = dict(hovermode="x unified", grid=dict(rows=5, columns=1))

    data = [
        go.Scatter(x=df_tratado.index, y=df_tratado['Disponibilidade'], xaxis="x", yaxis="y", name="Disponibilidade",hovertemplate="%{y:.1%}"),
        go.Scatter(x=df_tratado.index, y=df_tratado['Potência [kW]'], xaxis="x", yaxis="y2", name="Potência kW", hovertemplate="%{y:.1f}"),
        go.Scatter(x=df_tratado.index, y=df_tratado['Velocidade do vento [m/s]'], xaxis="x", yaxis="y3", name="Vento (m/s)"),
        go.Scatter(x=df_tratado.index, y=df_tratado['Velocidade do rotor [rpm]'], xaxis="x", yaxis="y4", name="Rotor (rpm)"),
        go.Scatter(x=df_tratado.index, y=df_tratado['Temperatura exterior da nacele [°C]'], xaxis="x", yaxis="y5", name="Temp. Ext. Nacelle (°C)"),
    ]

    fig = go.Figure(data=data, layout=layout,)

    fig.update_xaxes(showspikes=True, spikemode="toaxis", spikesnap="cursor", showline=True, spikecolor="blue",
    spikethickness=2, spikedash="dash")

    for axis in ["yaxis", "yaxis2", "yaxis3", "yaxis4", "yaxis5"]:
        fig.update_layout({
            axis: dict(
                showspikes=True,
                spikemode="toaxis",
                spikesnap="cursor",
                showline=True,
                spikecolor="blue",
                spikethickness=2,
                spikedash="dash"
            )
        })

    fig.update_layout(
        autosize=False,  # Set to False to manually control size
        width=2100,       # Set the desired width in pixels
        height=1000,      # Set the desired height in pixels

        yaxis=dict(title="Disponibilidade"),
        yaxis2=dict(title="Potência [kW]"),
        yaxis3=dict(title="Vento (m/s)"),
        yaxis4=dict(title="Rotor (rpm)"),
        yaxis5=dict(title="Temp. Ext. Nacelle (°C)"),
    )

    st.markdown(
        """
        <style>
        /* reduz padding lateral da área principal */
        .block-container {
            padding-left: 5rem;
            padding-right: 5rem;
            max-width: 100%;
        }
        /* opcional: reduz padding dentro dos elementos de plot */
        .stPlotlyChart > div {
            padding: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )  

    st.plotly_chart(fig, use_container_width=True)
    # st.table(base_disp.head(10))