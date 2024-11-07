# src/visualization.py

import plotly.graph_objects as go
import pandas as pd

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

    # Criar uma lista de subcategorias
    subcategories = df_grouped['subcategory'].unique()

    # Para um gráfico de radar, precisamos organizar os dados de forma que cada appId tenha um valor para cada subcategoria
    df_radar = df_grouped.pivot_table(index='appId', columns='subcategory', values='avg(score)', aggfunc='mean')
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
            name=app_id
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