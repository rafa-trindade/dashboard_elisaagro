import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime as dt
import numpy as np
from datetime import datetime

import utils.data_utils as data_utils
import utils.string_utils as string_utils
import utils.style_utils as style_utils

st.set_page_config(layout="wide", page_title="B2B Refeições | Elisa Agro", initial_sidebar_state="expanded", page_icon="📊")

style_utils.aplicar_estilo()

sidebar_logo = "https://i.postimg.cc/j5mwCcfV/logo-elisa.png"
main_body_logo = "https://i.postimg.cc/3xkGPmC6/streamlit02.png"
st.logo(sidebar_logo, icon_image=main_body_logo)

# Define a data de início como um Timestamp
data_inicio = pd.Timestamp('2024-03-01')

# Carregar o DataFrame a partir do CSV
csv_url = "data/databaseElisa.csv"
df_elisa = pd.read_csv(csv_url, sep=";", decimal=",", thousands=".", usecols=['data', 'fazenda', 'almoco', 'janta', 'cafe', 'lanche', 'vlrCafe', 'vlrAlmoco', 'total'], index_col=None)

# Convertendo a coluna 'data' para o tipo datetime após carregar o dataframe
df_elisa['data'] = pd.to_datetime(df_elisa['data'], format='%d/%m/%Y', errors='coerce')
df_elisa['fazenda'] = df_elisa['fazenda'].astype('category')


# Opção de seleção no Streamlit
opcao = st.sidebar.selectbox(
    "Selecione:",
    ("Todas as datas", "Contrato Vigente")
)
# Filtrar o DataFrame conforme a opção selecionada
if opcao == "Todas as datas":
    df = df_elisa
    data_menu = df['data'].min()
else:
    df = df_elisa[df_elisa['data'] >= data_inicio]
    data_menu = df['data'].min()

col1_side, col2_side = st.sidebar.columns([2,1])

col1_side.markdown('<h5 style="margin-bottom: -25px;">Início Apurado:', unsafe_allow_html=True)
col2_side.markdown(f'<h5 style="text-align: end; margin-bottom: -25px;">{data_menu.strftime("%d/%m/%Y")}</h5>', unsafe_allow_html=True)

col1_side.markdown('<h5 style="margin-bottom: 15px; color: #053061;">Última Atualização:</h5>', unsafe_allow_html=True)
col2_side.markdown('<h5 style="margin-bottom: 15px; text-align: end; color: #053061;">' + str(df['data'].max().strftime('%d/%m/%Y'))+ '</h5>', unsafe_allow_html=True)

#st.sidebar.write("____")


tab1, tab2 = st.tabs(["📅 Fechamentos Diários", "\t"])

########################################################################################
####### ABA FECHAMENTOS DIÁRIOS ########################################################
########################################################################################
with tab1:

    with st.container(border=True):
        col_data_ini, col_data_fim = st.columns(2)
        col1, col2, col3  = st.columns([1.775,1.7,1])   
        with col1:
            ct1 = st.container()
            ct2 = st.container(border=True )

        with col2:
            ct3 = st.container(border=True )
        with col3:
            ct4 = st.container(border=True )
    with st.container(border=True):

        colradios, col4, col5= st.columns([0.65,1.3,3])
        with colradios:
            colradio1 = st.container(border=True) 
            colradio2 = st.container(border=True)
        with col4:
            ct5 = st.container(border=True )
        with col5:
            ct6 = st.container(border=True )
########################################################################################
####### TABELA FECHAMENTO DIÁRIO #######################################################
########################################################################################

mes_atual = dt.datetime.today().month
ano_atual = dt.datetime.today().year

if df['data'].max().day < 20:
    mes_inicial_padrão = dt.date(ano_atual, mes_atual, 1)
else:
    mes_inicial_padrão = dt.date(ano_atual, mes_atual, 20)

# Suponha que seu dataframe `df` tenha uma coluna de data chamada 'data'
df['data'] = pd.to_datetime(df['data'])  # Certifique-se de que a coluna 'data' esteja no formato datetime

# Crie um conjunto de todas as datas disponíveis no dataframe
available_dates = set(df['data'].dt.date)

# Defina a data mínima e máxima disponíveis no dataframe
min_date = df['data'].min().date()
max_date = df['data'].max().date()

# Função para validar a data selecionada
def validate_date(selected_date, available_dates):
    if selected_date in available_dates:
        return True
    else:
        st.error(f"A data {selected_date.strftime('%d/%m/%Y')} não está disponível. Por favor, selecione uma data válida.")
        return False

# Usando os componentes date_input
data_inicial = col_data_ini.date_input(
    'Data Início:', 
    max_date, 
    min_value=min_date, 
    max_value=max_date, 
    format="DD/MM/YYYY",  
    key="data_inicio_key"
)

if validate_date(data_inicial, available_dates):
    # Atualize o min_value de data_fim com base na seleção de data_inicial
    data_fim = col_data_fim.date_input(
        'Data Fim:', 
        None,
        min_value=data_inicial, 
        max_value=max_date, 
        format="DD/MM/YYYY", 
        key="data_fim_key",
        #help="Para visualizar um dia em específico selecione o mesmo dia em Data Início e Data Fim"
    )
    
if data_inicial:
    data_inicial = pd.Timestamp(data_inicial)
if data_fim:
    data_fim = pd.Timestamp(data_fim)

df['data'] = pd.to_datetime(df['data'])

filtered_df = df[(df['data'] == data_inicial)]

if data_inicial is not None:
    dia_start = str(data_inicial.day).zfill(2)
    mes_start = str(data_inicial.month).zfill(2)
    ano_start = str(data_inicial.year)
if data_fim is not None:
    dia_end = str(data_fim.day).zfill(2)
    mes_end = str(data_fim.month).zfill(2)
    ano_end = str(data_fim.year)

if data_inicial and data_fim:
    if data_inicial > data_fim:
        st.warning('Data de início é maior que data de término!')
    else:
        filtered_df = df[(df['data'] >= data_inicial) & (df['data'] <= data_fim)] 

        if data_inicial == data_fim:
            periodo = dia_start + "/" + mes_start + "/" + ano_start                
        else:
            periodo = dia_start + "/" + mes_start + "/" + ano_start + " A " + dia_end + "/" + mes_end + "/" + ano_end
elif data_inicial:
    periodo = dia_start + "/" + mes_start + "/" + ano_start
    filtered_df = df[(df['data'] == data_inicial)]
elif data_fim:
    periodo = dia_end + "/" + mes_end + "/" + ano_end
    filtered_df = df[(df['data'] == data_fim)]

lista_fazenda = df['fazenda'].unique().tolist()

qtd_almoco = filtered_df.groupby("fazenda")[["almoco"]].sum(numeric_only=True)
qtd_janta = filtered_df.groupby("fazenda")[["janta"]].sum(numeric_only=True)
qtd_cafe = filtered_df.groupby("fazenda")[["cafe"]].sum(numeric_only=True)
qtd_lanche = filtered_df.groupby("fazenda")[["lanche"]].sum(numeric_only=True)

qtd_almoco = qtd_almoco.reindex(lista_fazenda)
qtd_janta = qtd_janta.reindex(lista_fazenda)
qtd_cafe = qtd_cafe.reindex(lista_fazenda)
qtd_lanche = qtd_lanche.reindex(lista_fazenda)

lista_almoco = qtd_almoco["almoco"].tolist()
lista_janta = qtd_janta["janta"].tolist()
lista_cafe = qtd_cafe["cafe"].tolist()
lista_lanche = qtd_lanche["lanche"].tolist()

# Cria cópias das listas para exibição com "-" no lugar de 0
lista_almoco_display = ['-' if v == 0 else v for v in lista_almoco]
lista_janta_display = ['-' if v == 0 else v for v in lista_janta]
lista_cafe_display = ['-' if v == 0 else v for v in lista_cafe]
lista_lanche_display = ['-' if v == 0 else v for v in lista_lanche]

data = {
    "Fazenda": lista_fazenda,
    "Café": lista_cafe_display,
    "Almoço": lista_almoco_display,
    "Lanche": lista_lanche_display,
    "Janta": lista_janta_display
}

data_frame = pd.DataFrame(data)

# Filtrar o data_frame para incluir apenas linhas onde algum dos valores não é NaN
data_frame = data_frame.dropna(subset=["Café", "Almoço", "Lanche", "Janta"], how='all')

soma_colunas = {
    "Fazenda": "<b>TOTAL</b>",
    "Café": f"<b>{int(qtd_cafe.sum(numeric_only=True).iloc[0]):,}".replace(',', '.') + "</b>",
    "Almoço": f"<b>{int(qtd_almoco.sum(numeric_only=True).iloc[0]):,}".replace(',', '.') + "</b>",
    "Lanche": f"<b>{int(qtd_lanche.sum(numeric_only=True).iloc[0]):,}".replace(',', '.') + "</b>",
    "Janta": f"<b>{int(qtd_janta.sum(numeric_only=True).iloc[0]):,}".replace(',', '.') + "</b>"
}

# Convertendo o dicionário para um DataFrame
soma_colunas_df = pd.DataFrame([soma_colunas])

data_frame = pd.concat([data_frame, soma_colunas_df], ignore_index=True)

# Inicializar listas de cores para as células com as cores padrões
fill_colors = [
    ['#176f87'] * len(data_frame), 
    ['white'] * len(data_frame), 
    ['#e2e7ed'] * len(data_frame), 
    ['white'] * len(data_frame), 
    ['#e2e7ed'] * len(data_frame),
]
font_colors = [
    ['white'] * len(data_frame),
    ['black'] * len(data_frame),
    ['black'] * len(data_frame),
    ['black'] * len(data_frame),
    ['black'] * len(data_frame)
]

# Iterar sobre todas as células e aplicar estilo se contiver <b>
for i, col in enumerate(data_frame.columns):
    for j, cell_value in enumerate(data_frame[col]):
        if '<b>' in str(cell_value):  # Verificar se a string <b> está presente no valor da célula
            fill_colors[i][j] = '#2d5480'  # Cor de fundo
            font_colors[i][j] = 'white'  # Cor da fonte

# Criar a tabela
fig_tabela_dia = go.Figure(data=[go.Table(
    header=dict(
        values=list(data_frame.columns),
        fill_color='#244366',
        line_color="lightgrey",
        font_color="white",
        font=dict(size=14.5),
        align='center',
        height=28  # Ajusta a altura do cabeçalho
    ),
    cells=dict(
        values=[data_frame[col] for col in data_frame.columns],
        fill=dict(color=fill_colors),
        line_color="lightgrey",
        font=dict(color=font_colors, size=13),
        align='center',
        height=29  # Ajusta a altura das células
    ))
])

fig_tabela_dia.update_layout(
                            yaxis=dict(
                                domain=[0.3, 1]  # Ajuste os valores conforme necessário
                            ),
                            #title={ 'text': "-FECHAMENTO DE " + periodo, 'y':0.92, 'x':0.0, 'xanchor': 'left', 'yanchor': 'top'},
                            height=139,
                            margin=dict(r=0, t=20,b=0)
)

# Convertendo colunas relevantes para tipo numérico (se necessário)
data_frame['Café'] = pd.to_numeric(data_frame['Café'], errors='coerce')
data_frame['Almoço'] = pd.to_numeric(data_frame['Almoço'], errors='coerce')
data_frame['Lanche'] = pd.to_numeric(data_frame['Lanche'], errors='coerce')
data_frame['Janta'] = pd.to_numeric(data_frame['Janta'], errors='coerce')

# Dados para o gráfico de barras
categorias = ['Café', 'Almoço', 'Lanche', 'Janta']
valores = [
    data_frame['Café'].sum(numeric_only=True),
    data_frame['Almoço'].sum(numeric_only=True),
    data_frame['Lanche'].sum(numeric_only=True),
    data_frame['Janta'].sum(numeric_only=True)
]

# Criando o gráfico de barras
fig_barras = go.Figure(data=go.Bar(
    x=categorias,
    y=valores,
    text=valores,
    textposition='auto',
    texttemplate='%{y:.0f}',  # Formato do texto (inteiro sem casas decimais)
    marker_color=["#2d5480", "#176f87", "#2d5480", "#176f87"],  # Cor das barras
    textangle = 0

))

fig_barras.update_layout(
    #title='Consumo Diário por Refeição',
    height=301,
    margin=dict(l=0, r=0, t=23, b=0),
    yaxis=dict(showticklabels=False),
    title_text=f'-QUANTIDADE TOTAL DE REFEIÇÕES ({periodo})',
    title_x=0,
    title_y=0.98,
    title_font_color="rgb(98,83,119)",
    title_font_size=15,
)
fig_barras.update_yaxes(showline=True, linecolor="Grey", linewidth=0.1, gridcolor='lightgrey')
fig_barras.update_xaxes(showline=True, linecolor="Grey", linewidth=0.1, gridcolor='lightgrey')

# Mostrando a tabela ao lado do gráfico de barras
ct1.plotly_chart(fig_tabela_dia, use_container_width=True, automargin=True)
ct3.plotly_chart(fig_barras, use_container_width=True)

########################################################################################
####### GRÁFICO PIZZA FECHAMENTO DIÁRIO ################################################
########################################################################################
# Cálculo dos totais
fazenda_total = filtered_df.groupby("fazenda")[["total"]].sum(numeric_only=True).reset_index()

# Filtrar as fazendas com valor maior que 0
fazenda_total = fazenda_total[fazenda_total['total'] > 0]

# Calcular a porcentagem relativa ao total
total_geral = fazenda_total['total'].sum(numeric_only=True)
fazenda_total['porcentagem'] = fazenda_total['total'] / total_geral * 100

# Adicionando uma coluna com os valores formatados em porcentagem
fazenda_total['porcentagem_formatada'] = fazenda_total['porcentagem'].apply(lambda x: f"{x:.2f}%")

# Criando o gráfico de rosca
fig_venda_fazenda = px.pie(fazenda_total, names='fazenda', values='porcentagem', 
                        color='fazenda', 
                        color_discrete_sequence= [style_utils.barra_vermelha, style_utils.barra_azul, style_utils.barra_verde_escuro],
                        hover_data=['porcentagem_formatada'])

# Configurações adicionais
fig_venda_fazenda.update_traces(
    texttemplate='%{label}<br>%{value:.2f}%', 
    textposition='inside'
)

fig_venda_fazenda.update_layout(
    #width=200, 
    height=301, 
    margin=dict(l=0, t=35, b=0, r=0), 
    legend=dict(
        orientation="h",
        yanchor="top",
        y=0,
        xanchor="center",
        x=0.5,
        font=dict(size=12),
        itemsizing='constant',
        itemwidth=30,
        entrywidthmode='pixels'
    ),
    title={
        'text': f"-DISTRIBUIÇÃO ({periodo})",
        'y': 0.965,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {
            'color': "rgb(98,83,119)",
            'size': 15
        }
    },
    #showlegend = False
)

ct4.plotly_chart(fig_venda_fazenda, use_container_width=True)


########################################################################################
####### GRAFICO BOX PLOT MENSAL ########################################################
########################################################################################
df_filtrado = df[(pd.to_datetime(df['data']).dt.month == data_inicial.month) &
                (pd.to_datetime(df['data']).dt.year == data_inicial.year)]

# Agrupar e somar os valores por data e fazenda
df_agrupado = df_filtrado.groupby(['data', 'fazenda']).sum(numeric_only=True).reset_index()

# Renomear as colunas
df_agrupado = df_agrupado.rename(columns={'cafe': 'Café', 'almoco': 'Almoço', 'lanche': 'Lanche', 'janta': 'Janta'})  

# Transformar o DataFrame para o formato longo
df_long = df_agrupado.melt(id_vars=['data', 'fazenda'], value_vars=['Café', 'Almoço', 'Lanche', 'Janta'], 
                        var_name='Refeição', value_name='Valor')

# Filtrar as opções de fazendas com valor maior que 0
fazendas_com_valor = df_long[df_long['Valor'] > 0]['fazenda'].unique()
opcoes_fazenda = np.append(['Todas'], fazendas_com_valor)

with colradio1:
    # Configurar o radio com as opções de fazendas únicas
    fazenda_selecionada = st.radio("FAZENDA:", options=opcoes_fazenda, index=0, key="fazenda_selecionada")

# Filtrar o DataFrame para a fazenda selecionada (ou todas)
if fazenda_selecionada != 'Todas':
    df_filtrado_fazenda = df_long[(df_long['fazenda'] == fazenda_selecionada) & (df_long['Valor'] >= 0)]
else:
    df_filtrado_fazenda = df_long[df_long['Valor'] >= 0]


# Filtrar os valores onde a coluna 'valor' é maior que 0
df_filtrado_valor_radio = df_filtrado_fazenda[df_filtrado_fazenda['Valor'] > 0]

# Obter os valores únicos da coluna 'Refeição'
tipos_com_valor = df_filtrado_valor_radio['Refeição'].unique()

with colradio2:
    # Configurar o radio com as opções de refeições únicas
    tipo_refeicao = st.radio("TIPO REFEIÇÃO:", options=tipos_com_valor, index=list(tipos_com_valor).index("Almoço") if "Almoço" in tipos_com_valor else 0, key="tipo_selecionado")

# Filtrar pelo tipo de refeição selecionado
df_selecionado = df_filtrado_fazenda[df_filtrado_fazenda['Refeição'] == tipo_refeicao]

# Filtrar pelo fazenda selecionada
if fazenda_selecionada == 'Todas':
    # Agrupar por data para obter a soma de todas as fazendas
    df_selecionado = df_selecionado.groupby('data').sum(numeric_only=True).reset_index()

# Criando a figura com go.Box
fig_box = go.Figure()

# Adicionando caixa para a refeição selecionada
colors = {"Café": "#2d5480", "Almoço": "#2d5480", "Lanche": "#2d5480", "Janta": "#2d5480"}
color = colors.get(tipo_refeicao, "#b3112e")  # Cor padrão

fig_box.add_trace(go.Box(
    y=df_selecionado['Valor'],
    name=tipo_refeicao,
    marker=dict(color="#2d5480"),  # Cor personalizada para cada refeição
    line=dict(color=color),  # Cor da linha
    boxpoints="all",  # Mostrar todos os pontos
    hovertext=df_selecionado['data'].dt.strftime('%d/%m/%y')   
))

fig_box.update_layout(
    height=284,
    margin=dict(l=0, r=0, t=30, b=0),
    title_text=f'-BOX PLOT QTD. DE REFEIÇÕES ({data_utils.mapa_meses[data_inicial.month].upper()}/{data_inicial.year})',
    title_font_color="rgb(98,83,119)",
    title_font_size=15,
    showlegend=False,
    title_x=0,
    title_y=1,
)

fig_box.update_yaxes(
    zerolinecolor='lightgrey',
    autorange=True,
    autorangeoptions=dict(maxallowed = df_selecionado['Valor'].max() + 10, minallowed = df_selecionado['Valor'].min() - 10 ),
    dtick=5,
    showline=False, 
    linecolor="Grey", 
    linewidth=0.1, 
    gridcolor='lightgrey', 
    showticklabels=True, 
    title_text='Quantidade',
)

fig_box.update_xaxes(showline=True, linecolor="Grey", linewidth=0.1, gridcolor='lightgrey', title_text=f'{fazenda_selecionada}')
fig_box.update_traces(marker=dict(size=4.5),
                    boxmean='sd',)

ct5.plotly_chart(fig_box, use_container_width=True)

########################################################################################
####### HISTOGRAMA MES HISTORICO QUANTIDADES ###########################################
########################################################################################

# Conversão de colunas e criação de novas
df["data"] = pd.to_datetime(df["data"], errors='coerce')
df["Almoço | Janta"] = df["almoco"] + df["janta"]
df["Café | Lanche"] = df["cafe"] + df["lanche"]
df["ano"] = df["data"].dt.year
df["mes"] = df["data"].dt.month
df["dia"] = df["data"].dt.day

# Identificar o mês selecionado em data_inicial
data_inicial = pd.Timestamp(data_inicial)  # Supondo que esta é a data selecionada
data_selecionada = data_inicial

# Filtrar os dados para o mês selecionado
df_filtrado = df[(df["ano"] == data_selecionada.year) & (df["mes"] == data_selecionada.month)]

# Filtrar o DataFrame para a fazenda selecionada (ou todas)
if fazenda_selecionada != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['fazenda'] == fazenda_selecionada]

# Agrupar os dados por dia
df_grouped = df_filtrado.groupby(["ano", "mes", "dia"]).sum(numeric_only=True).reset_index()

# Criar uma nova coluna com o formato "Dia/Mês"
df_grouped["Dia/Mês"] = df_grouped.apply(lambda row: f"{str(int(row['dia'])).zfill(2)}/{str(int(row['mes'])).zfill(2)}", axis=1)

# Identificar o dia selecionado no mês
dia_selecionado = data_selecionada.day

# Adicionar linhas verticais a cada 7 dias para trás e para frente a partir do dia selecionado
linhas_verticais = []
# Para trás
for day in range(dia_selecionado, df_grouped['dia'].min() - 1, -7):
    if day in df_grouped['dia'].values:
        day_label = df_grouped[df_grouped['dia'] == day]["Dia/Mês"].values[0]
        linhas_verticais.append(day_label)
        
# Para frente
for day in range(dia_selecionado + 7, df_grouped['dia'].max() + 1, 7):
    if day in df_grouped['dia'].values:
        day_label = df_grouped[df_grouped['dia'] == day]["Dia/Mês"].values[0]
        linhas_verticais.append(day_label)

# Criar o histograma
fig = go.Figure()

# Função para determinar se o valor deve ser exibido
def should_show_text(x_value):
    return x_value in linhas_verticais

# Adicionar barras para Almoço | Janta
fig.add_trace(go.Bar(
    x=df_grouped["Dia/Mês"],
    y=df_grouped["Almoço | Janta"],
    name="Almoço | Janta",
    marker_color="#81a8b4",
    showlegend=True,  # Remover legenda das cores
    text=df_grouped.apply(lambda row: f"<b>{int(row['Almoço | Janta'])}</b>" if row["Dia/Mês"] in linhas_verticais else "", axis=1),
    textposition='outside',
    textangle=-45,
    textfont=dict(
        color=style_utils.barra_verde_escuro,
    )    
))

# Adicionar barras para Café | Lanche
fig.add_trace(go.Bar(
    x=df_grouped["Dia/Mês"],
    y=df_grouped["Café | Lanche"],
    name="Café | Lanche",
    marker_color="#6882a0",
    showlegend=True,  # Remover legenda das cores
    text=df_grouped.apply(lambda row: f"<b>{int(row['Café | Lanche'])}</b>" if row["Dia/Mês"] in linhas_verticais else "", axis=1),
    textposition='outside',
    textangle=-45,
    textfont=dict(
        color=style_utils.barra_azul_escuro,
    )   
))


# Adicionar linhas verticais ao gráfico
for day_label in linhas_verticais:
    fig.add_shape(
        type="line",
        x0=day_label,
        x1=day_label,
        y0=0,
        y1=df_grouped[["Almoço | Janta", "Café | Lanche"]].max().max(),
        line=dict(color="#b3112e", width=1, dash="dot")
    )

# Pegar os valores de Almoço | Janta e Café | Lanche do último dia do mês selecionado
ultimo_dia_almoco_janta = df_grouped["Almoço | Janta"].iloc[-1]
ultimo_dia_cafe_lanche = df_grouped["Café | Lanche"].iloc[-1]

# Adicionar a linha horizontal para Almoço | Janta do último dia
fig.add_shape(
    type="line",
    x0=df_grouped["Dia/Mês"].iloc[0],
    x1=df_grouped["Dia/Mês"].iloc[-1],
    y0=ultimo_dia_almoco_janta,
    y1=ultimo_dia_almoco_janta,
    line=dict(color="#176f87", width=1.5, dash="dashdot") 
)

# Adicionar a linha horizontal para Café | Lanche do último dia
fig.add_shape(
    type="line",
    x0=df_grouped["Dia/Mês"].iloc[0],
    x1=df_grouped["Dia/Mês"].iloc[-1],
    y0=ultimo_dia_cafe_lanche,
    y1=ultimo_dia_cafe_lanche,
    line=dict(color="#2d5480", width=1.5, dash="dashdot")
)

# Configurar as datas do eixo x
if len(df_grouped) < 21:
    tickvals = df_grouped["Dia/Mês"].tolist()
else:
    tickvals = linhas_verticais

# Configuração do gráfico
fig.update_yaxes(showline=True, linecolor="Grey", linewidth=0.1, gridcolor='lightgrey', dtick=10, range=[0, df_grouped["Almoço | Janta"].max() + 40])
fig.update_xaxes(
    showline=True, 
    linecolor="Grey", 
    linewidth=0.1, 
    gridcolor='lightgrey',
    tickmode='array',
    tickvals=tickvals,
    tickformat="%d/%m"
)
fig.update_layout(
    margin=dict(l=0, r=0, t=30, b=0),
    height=284,
    title=" ",
    title_text=f'-HISTOGRAMA QUANTIDADE REFEIÇÕES AGRUPADAS ({data_utils.mapa_meses[data_inicial.month].upper()}/{data_inicial.year})',
    title_x=0,
    title_y=1,
    title_font_color="rgb(98,83,119)",
    title_font_size=15,
    barmode='group',  # Configurar as barras para serem agrupadas lado a lado
    yaxis=dict(showticklabels=False),
    xaxis_title="Período",
    legend=dict(x=0.7315, y=1.115, orientation='h')  # Configurar a posição da legenda
)

# Exibir o gráfico no Streamlit
ct6.plotly_chart(fig, use_container_width=True, automargin=True)

########################################################################################
####### GRAFICO AREA HISTORICO QUANTIDADES #############################################
########################################################################################

# Conversão de colunas e criação de novas
df["data"] = pd.to_datetime(df["data"], errors='coerce')
df["Almoço | Janta"] = df["almoco"] + df["janta"]
df["Café | Lanche"] = df["cafe"] + df["lanche"]
df["ano"] = df["data"].dt.year
df["mes"] = df["data"].dt.month

# Agrupar os dados por ano e mês
df_grouped = df.groupby(["ano", "mes"]).sum(numeric_only=True).reset_index()

# Criar uma nova coluna com o formato "Mês/Ano" utilizando o mapa de meses
df_grouped["Mês/Ano"] = df_grouped.apply(lambda row: f"{data_utils.mapa_meses[int(row['mes'])]}/{int(row['ano'])}", axis=1)

# Identificar o mês e ano atual
current_month = pd.Timestamp.now().month
current_year = pd.Timestamp.now().year

# Calculando o mês anterior
previous_month = current_month - 1 if current_month != 1 else 12
previous_year = current_year if current_month != 1 else current_year - 1

# Identificar o valor de 'Almoço | Janta' e 'Café | Lanche' para o mês anterior
previous_almoco_janta_value = df_grouped[(df_grouped["ano"] == previous_year) & (df_grouped["mes"] == previous_month)]["Almoço | Janta"].values[0]
previous_cafe_lanche_value = df_grouped[(df_grouped["ano"] == previous_year) & (df_grouped["mes"] == previous_month)]["Café | Lanche"].values[0]

# Criar o gráfico de área
fig = go.Figure()

# Adicionar a área para Almoço | Janta
fig.add_trace(go.Scatter(
    x=df_grouped["Mês/Ano"],
    y=df_grouped["Almoço | Janta"],
    mode='lines+markers+text',
    name="Almoço | Janta",
    fill='tozeroy',
    marker=dict(
        color=style_utils.barra_verde,
        size=5  
    ),    
    marker_color=style_utils.barra_verde,
))

# Adicionar a área para Café | Lanche
fig.add_trace(go.Scatter(
    x=df_grouped["Mês/Ano"],
    y=df_grouped["Café | Lanche"],
    mode='lines+markers+text',
    name="Café | Lanche",
    fill='tozeroy',
    marker=dict(
        color=style_utils.barra_azul,
        size=5  
    ),    
    marker_color=style_utils.barra_azul,
    fillcolor="#6c87a6"
))

# Adicionar a linha horizontal para Almoço | Janta do mês anterior
fig.add_shape(
    type="line",
    x0=df_grouped["Mês/Ano"].iloc[0],
    x1=df_grouped["Mês/Ano"].iloc[-1],
    y0=previous_almoco_janta_value,
    y1=previous_almoco_janta_value,
    line=dict(color="#0e7089", width=1.5, dash="dashdot")
)

# Adicionar a linha horizontal para Café | Lanche do mês anterior
fig.add_shape(
    type="line",
    x0=df_grouped["Mês/Ano"].iloc[0],
    x1=df_grouped["Mês/Ano"].iloc[-1],
    y0=previous_cafe_lanche_value,
    y1=previous_cafe_lanche_value,
    line=dict(color="#145073", width=1.5, dash="dashdot")
)

# Buscar os anos para os quais temos dados do mês anterior
previous_month_years = df_grouped[df_grouped["mes"] == previous_month]["ano"].values

# Adicionar linhas verticais para cada "Mês/Ano" do mês anterior em todos os anos disponíveis
linhas_verticais = []
for year in previous_month_years:
    month_year_label = f"{data_utils.mapa_meses[previous_month]}/{year}"
    linhas_verticais.append(month_year_label)
    fig.add_shape(
        type="line",
        x0=month_year_label,
        x1=month_year_label,
        y0=0,
        y1=df_grouped["Almoço | Janta"].max(),
        line=dict(color="#b3112e", width=1, dash="dot")
    )

# Configurar as datas do eixo x para mostrar somente as datas com linhas verticais
tickvals = linhas_verticais

# Período do gráfico
data_inicial_area = pd.Timestamp(df['data'].min())
data_fim_area = pd.Timestamp(df['data'].max())
periodo_area = f"{data_utils.mapa_meses[data_inicial_area.month].upper()}/{data_inicial_area.year} A {data_utils.mapa_meses[data_fim_area.month].upper()}/{data_fim_area.year}"

# Configuração do gráfico
fig.update_yaxes(showline=True, linecolor="Grey", linewidth=0.1, gridcolor='lightgrey', dtick=2000)
fig.update_xaxes(
    showline=True, 
    linecolor="Grey", 
    linewidth=0.1, 
    gridcolor='lightgrey',
    tickmode='array',
    tickvals=tickvals,
)
fig.update_layout(
    margin=dict(l=5, r=0, t=28, b=0),
    height=145.5,
    title=f"-HISTÓRICO REFEIÇÕES AGRUPADAS ({periodo_area})",
    title_font_color="rgb(98,83,119)",
    title_font_size=15,
    legend=dict(x=0.722, y=1.09, orientation='h'),
    title_x=0,
    title_y=1,
    yaxis=dict(showticklabels=False),
    showlegend=False
)

# Exibir o gráfico no Streamlit
ct2.plotly_chart(fig, use_container_width=True, automargin=True)