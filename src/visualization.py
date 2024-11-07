# src/visualization.py

import plotly.graph_objects as go
import pandas as pd
import streamlit as st

 # Mapeamento de appIds para títulos dos apps
app_titles = {
    "ws.hanzo.Vrrh": "SuperApp VR",
    "br.com.santander.benvisavale": "Ben Visa Vale",
    "br.com.ifood.benefits": "iFood Benefícios",
    "com.primety.sodexomobile": "Pluxee Brasil",
    "com.caju.employeeApp": "Caju - Benefícios por inteiro",
    "br.com.flashapp": "Flash App Benefícios",
    "br.com.mobile.ticket": "Ticket",
    "br.com.gabba.Caixa": "Caixa",
    "com.shopee.br": "Shopee",
    "com.nu.production": "Nubank: conta, cartão e mais",
    "com.ubercab": "Uber: Peça viagem de carro",
    "br.gov.meugovbr": "Gov.br",
    "br.gov.caixa.tem": "Caixa Tem",
    "com.taxis99": "99: Vá de Carro, Moto ou Taxi",
    "br.gov.caixa.fgts.trabalhador": "FGTS",
    "br.com.vivo": "Vivo",
    "com.mercadopago.wallet": "Mercado Pago: banco digital",
}

def plot_radar_chart(csv_file):
    """
    Recebe um CSV de resultados e plota um gráfico radar interativo.
    """
    # Carregar o arquivo CSV gerado
    df = pd.read_csv(csv_file)

    # Verificar se o CSV está vazio
    if df.empty:
        print("O CSV está vazio, nenhum gráfico será gerado.")
        return
    
    # Agrupar os dados por appId, subcategoria e calcular o rating médio
    df_grouped = df.groupby(['appId', 'subcategory'], as_index=False).agg({'avg(score)': 'mean'})

    # Formatando o 'avg(score)' para 3 casas decimais
    df_grouped['avg(score)'] = df_grouped['avg(score)'].round(3)

    # Substituir valores NaN por 0
    df_grouped = df_grouped.fillna(0)

    # Criar uma lista de subcategorias
    subcategories = df_grouped['subcategory'].unique()

    # Para um gráfico de radar, precisamos organizar os dados de forma que cada appId tenha um valor para cada subcategoria
    df_radar = df_grouped.pivot_table(index='appId', columns='subcategory', values='avg(score)', aggfunc='mean')
    
    # Substituir valores NaN por 0
    df_radar = df_radar.fillna(0)
    print(df_radar)

    # Definir a lista de subcategorias
    subcategories_list = list(df_radar.columns)

    # Criar o gráfico de radar
    fig = go.Figure()

    # Adicionar cada appId como uma linha no gráfico de radar
    for app_id in df_radar.index:
        fig.add_trace(go.Scatterpolar(
            r=df_radar.loc[app_id].values,
            theta=subcategories_list,
            fill='toself',
            name=app_titles.get(app_id, app_id)
        ))

    # Atualizar o layout do gráfico
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]  # A média de score está entre 0 e 5
            )
        ),
        title="Radar de Satisfação | Subcategorias e Rating Médio",
        template="plotly",
        showlegend=True
    )

    # Exibir o gráfico
    #  fig.show()

    # Exibir o gráfico diretamente na página do Streamlit
    st.plotly_chart(fig)

def plot_single_app_radar(app_id, csv_file):
    # Carregar os dados do CSV
    df = pd.read_csv(csv_file)
    
    # Filtrar os dados para o appId específico
    df_app = df[df['appId'] == app_id]

    # Agrupar e calcular a média do rating e o volume para cada subcategoria
    df_grouped = df_app.groupby('subcategory').agg(
        avg_score=('avg(score)', 'mean'),
        count=('count(id)', 'sum')
    ).reset_index()

    # Lista de subcategorias
    subcategories_list = df_grouped['subcategory'].tolist()
    ratings = df_grouped['avg_score'].tolist()
    counts = df_grouped['count'].tolist()

    # Obter o título do app pelo appId
    app_name = app_titles.get(app_id, app_id)

    # Criar o gráfico de radar para o app específico
    fig = go.Figure()

    # Customizar a legenda com o volume e o rating médio por subcategoria
    legend_name = f"{app_name} | Média: {sum(ratings) / len(ratings):.3f} | Volume total: {sum(counts)}"

    fig.add_trace(go.Scatterpolar(
        r=ratings,
        theta=subcategories_list,
        fill='toself',
        name=legend_name,
        hovertemplate='<b>Subcategoria: %{theta}</b><br>Média: %{r:.2f}<br>Volume: %{customdata}',
        customdata=counts  # Exibe o volume de cada subcategoria ao passar o mouse
    ))

    # Configurações do layout do gráfico
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]  # Define a escala de 0 a 5
            )
        ),
        title=f"Radar de Satisfação | {app_name}",
        template="seaborn",
        showlegend=False
    )

    # Exibir o gráfico diretamente na página do Streamlit
    st.plotly_chart(fig)
