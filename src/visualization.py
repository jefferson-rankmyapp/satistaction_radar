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
    # Carregar os dados do CSV
    df = pd.read_csv(csv_file)

    # Processar os dados para o gráfico de radar
    df_grouped = df.groupby(['appId', 'subcategory']).agg(
        avg_score=('avg(score)', 'mean'),
        count=('count(id)', 'sum')  # Certifique-se de que 'count(id)' está no CSV
    ).reset_index()

    # Pivotar para a visualização no radar
    df_radar = df_grouped.pivot(index='appId', columns='subcategory', values='avg_score').fillna(0)
    df_count = df_grouped.pivot(index='appId', columns='subcategory', values='count').fillna(0)

    # Lista de subcategorias
    subcategories_list = list(df_radar.columns)

    # Criar o gráfico de radar para todos os apps
    fig = go.Figure()

    for app_id in df_radar.index:
        app_name = app_titles.get(app_id, app_id)
        ratings = df_radar.loc[app_id].values
        counts = df_count.loc[app_id].values

        # Customizar a legenda com o volume e o rating médio
        legend_name = f"{app_name} | Média: {ratings.mean():.3f} | Volume: {counts.sum()}"

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
                range=[0, 5]
            )
        ),
        title="Radar de Satisfação | Subcategorias, Rating Médio e Volume",
        template="plotly",
        showlegend=True
    )

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
