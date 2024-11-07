import streamlit as st
import pandas as pd
from src.visualization import plot_radar_chart, plot_single_app_radar

# Configurações iniciais da página do Streamlit
st.set_page_config(page_title="Análise de Satisfação de Apps", page_icon="data/Logo light mode.png")

# Título e logotipo
st.image("data/Logo light mode.png", width=200)
st.title("Análise de Satisfação de Apps")
st.write("Essa aplicação permite analisar a satisfação de usuários para diferentes aplicativos, com base nas subcategorias e médias de rating dos reviews.")

# # Controle para escolher o CSV de dados
# st.sidebar.header("Configurações de Dados")
# use_default_csv = st.sidebar.radio("Escolha a fonte de dados:", ["Usar CSV padrão", "Carregar novo CSV"])

# # Carregar o CSV com base na opção do usuário
# if use_default_csv == "Usar CSV padrão":
#     csv_file = "data/review_summary.csv"
#     st.sidebar.write("Usando o arquivo de dados padrão.")
# else:
#     uploaded_file = st.sidebar.file_uploader("Carregue um arquivo CSV", type=["csv"])
#     if uploaded_file:
#         csv_file = uploaded_file
#         st.sidebar.write("Novo arquivo de dados carregado.")
#     else:
#         st.warning("Por favor, carregue um arquivo CSV.")
#         st.stop()  # Interrompe a execução até que um arquivo seja carregado

csv_file = "data/review_summary.csv"

# Carregar o DataFrame
df = pd.read_csv(csv_file)

# Exibir uma tabela com o DataFrame processado para o radar
st.subheader("Dados Processados para o Gráfico Radar")
st.write("Tabela mostrando as médias de rating por subcategoria.")
df_radar = df.groupby(['appId', 'subcategory'], as_index=False).agg({'avg(score)': 'mean'}).pivot_table(
    index='appId', columns='subcategory', values='avg(score)').fillna(0)
st.dataframe(df_radar)

# Exibir o gráfico radar geral com o arquivo CSV carregado
st.subheader("Gráfico Radar de Satisfação - Todos os Apps")
plot_radar_chart(csv_file)

# Controle para exibir o gráfico de um único app
st.subheader("Análise Detalhada de um App")
app_id_input = st.text_input("Digite o appId para visualizar o radar específico")

# Verifica se o appId foi inserido e plota o gráfico específico
if app_id_input:
    if app_id_input in df["appId"].unique():
        plot_single_app_radar(app_id_input, csv_file)
    else:
        st.error("O appId informado não foi encontrado no arquivo de dados.")
