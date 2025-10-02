import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


############## ABAS DO EXCEL ####################################################################################################################
@st.cache_data
def carregar_base1():
    base = pd.read_excel('Teste Prático - Dados para Tarefa 2 .xlsx')
    base = base.set_index("sample_time")
    return base
@st.cache_data
def carregar_base2():
    base = pd.read_excel('Teste Prático - Dados para Tarefa 2 .xlsx', sheet_name=1)
    base = base.set_index("sample_time")
    return base
@st.cache_data
def carregar_base3():
    base = pd.read_excel('Teste Prático - Dados para Tarefa 2 .xlsx', sheet_name=2)
    base = base.set_index("sample_time")
    return base

base = carregar_base1()
base2 = carregar_base2()
base3 = carregar_base3()


############# Layout ############################################################################################################################

st.title("Relatório de Performance - Usina Solar 2")
st.title("Performance Report - Solar Plant 2")

############## POTENCIA ##############################################################################################################################
potencia = base.loc[:, [coluna for coluna in base.columns if 'PowerActive' in coluna]]
potencia = potencia.drop(potencia.index[-1])
fig = go.Figure()
for coluna in potencia.columns:
    fig.add_trace(go.Scatter(
        x=potencia.index,
        y=potencia[coluna],
        name=coluna,              
        line_shape='linear',
        hovertemplate="<b>%{x}</b><br>Potência: %{y} kW<br>Coluna: " + coluna + "<extra></extra>"
    ))

fig.update_traces(hoverinfo='text+name', mode='lines')
st.plotly_chart(fig)

st.write('')
st.write('**[PT]**')
st.write('INV02 apresentou queda de 50% na performance nos dois dias.')
st.write('INV05 apresentou queda de performance durante perídos de baixa-média irradiância.')

st.write('**[EN]**')
st.write('Inverter INV02 showed a 50% performance drop on both days.')
st.write('Inverter INV05 showed a performance drop during periods of low to medium irradiance.')
########### TEMPERATURA ##############################################################################################################################
temperatura = base.loc[:, [coluna for coluna in base.columns if 'Temperature' in coluna]]
temperatura = temperatura.drop(temperatura.index[-1])
fig = go.Figure()
for coluna in temperatura.columns:
    fig.add_trace(go.Scatter(
        x=temperatura.index,
        y=temperatura[coluna],
        name=coluna,             
        line_shape='linear',
        hovertemplate="<b>%{x}</b><br>Temperatura (°C): %{y} °C<br>Coluna: " + coluna + "<extra></extra>"
    ))

fig.update_traces(hoverinfo='text+name', mode='lines')
# fig.show()
st.plotly_chart(fig)
st.write('**[PT]**')
st.write('INV07 apresentou temperatura maior em todo o período de análise, mesmo quando não havia produção. Recomenda-se analisar a calibração do sensor')
st.write('**[EN]**')
st.write('INV07 showed a higher temperature throughout the entire analysis period, even when there was no production. It is recommended to check the sensor calibration')

########### TENSÃO ###################################################################################################################################
tensao = base.loc[:, [coluna for coluna in base.columns if 'Voltage' in coluna]]
tensao = tensao.drop(tensao.index[-1])
fig = go.Figure()
for coluna in tensao.columns:
    fig.add_trace(go.Scatter(
        x=tensao.index,
        y=tensao[coluna],
        name=coluna,             
        line_shape='linear',
        hovertemplate="<b>%{x}</b><br>Tensão (V): %{y} V<br>Coluna: " + coluna + "<extra></extra>"
    ))

fig.update_traces(hoverinfo='text+name', mode='lines')
# fig.show()
st.plotly_chart(fig)
st.write('**[PT]**')
st.write('Tensões sem anomalias. as quedas pontuais observáveis não indicam riscos')
st.write('**[EN]**')
st.write('Voltages show no anomalies. The occasional drops observed do not indicate any risks')

######### CORRENTE CC #################################################################################################################################
corrente_CC = base2.loc[:, [coluna for coluna in base2.columns]]
corrente_CC = corrente_CC.drop(corrente_CC.index[-1])
fig = go.Figure()
for coluna in corrente_CC.columns:
    fig.add_trace(go.Scatter(
        x=corrente_CC.index,
        y=corrente_CC[coluna],
        name=coluna,             
        line_shape='linear',
        hovertemplate="<b>%{x}</b><br>Corrente CC normalizada: %{y} %<br>Coluna: " + coluna + "<extra></extra>"
    ))

fig.update_traces(hoverinfo='text+name', mode='lines')
# fig.show()
st.plotly_chart(fig)
lista = ['INV08 - MPPT2_STR01',
        'INV08 - MPPT1_STR01',
        'INV08 - MPPT1_STR02',
        'INV08 - MPPT2_STR02',
        'INV05 - MPPT3_STR01',
        'INV05 - MPPT3_STR02',
        'INV05 - MPPT4_STR01',
        'INV05 - MPPT4_STR02', 
        'INV02 - MPPT5_STR01',
        'INV02 - MPPT5_STR02']
st.write('**[PT]**')
st.write('Strings com baixa performance nos dois dias (inversor 02 tem strings desligadas):')
st.write('**[EN]**')
st.write('Strings with low performance on both days (Inverter 02 has disconnected strings):')

for item in lista:
    st.write(f"- {item}")

######## TRACKERS #####################################################################################################################################
tracker = base3.loc[:, [coluna for coluna in base3.columns]]
tracker = tracker.drop(tracker.index[-1])
fig = go.Figure()
for coluna in tracker.columns:
    fig.add_trace(go.Scatter(
        x=tracker.index,
        y=tracker[coluna],
        name=coluna,             
        line_shape='linear',
        hovertemplate="<b>%{x}</b><br>Inclinação (°): %{y} °<br>Coluna: " + coluna + "<extra></extra>"
    ))

fig.update_traces(hoverinfo='text+name', mode='lines')
# fig.show()
st.plotly_chart(fig)
lista_trackers = ['TK_04-03','TK_05-03']
st.write('**[PT]**')
st.write('Trackers inoperantes:')
st.write('**[EN]**')
st.write('inoperative trackers:')
for item in lista_trackers:
    st.write(f"- {item}")

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













