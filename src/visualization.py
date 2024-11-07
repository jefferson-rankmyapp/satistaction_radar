# src/visualization.py

import plotly.graph_objects as go
import pandas as pd

 # Mapeamento de appIds para títulos dos apps
app_titles = {
    "ws.hanzo.Vrrh": "SuperApp VR",
    "br.com.santander.benvisavale": "Ben Visa Vale",
    "br.com.ifood.benefits": "iFood Benefícios",
    "com.primety.sodexomobile": "Pluxee Brasil",
    "com.caju.employeeApp": "Caju - Benefícios por inteiro",
    "br.com.flashapp": "Flash App Benefícios",
    "br.com.mobile.ticket": "Ticket"
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
    fig.show()

def plot_single_app_radar(app_id, csv_file):
    # Verificar se o app_id existe no mapeamento e obter o título correspondente
    app_title = app_titles.get(app_id, app_id)

    # Carregar o arquivo CSV gerado
    df = pd.read_csv(csv_file)

    # Filtrar os dados para o appId selecionado
    df_app = df[df['appId'] == app_id]

    # Agrupar os dados por subcategoria e calcular o rating médio
    df_grouped = df_app.groupby('subcategory', as_index=False).agg({'avg(score)': 'mean'})
    
    # Formatar o 'avg(score)' para 3 casas decimais
    df_grouped['avg(score)'] = df_grouped['avg(score)'].round(3)

    # Garantir que todas as subcategorias estejam no índice, substituindo NaNs por 0 para eixos ausentes
    df_radar = df_grouped.set_index('subcategory').reindex(columns=['avg(score)']).fillna(0)

    # Criar o gráfico de radar para o app específico
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=df_radar['avg(score)'].values,
        theta=df_radar.index,
        fill='toself',
        name=app_title
    ))

    # Configurar layout do gráfico
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]  # A média de score está entre 0 e 5
            )
        ),
        title=f"Radar de Satisfação | {app_title}",
        template="plotly_dark",
        showlegend=False  # Remover legenda para gráfico de app único
    )

    # Exibir o gráfico
    fig.show()