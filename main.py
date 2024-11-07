# main.py

from src.mongo_handler import MongoHandler  # Classe responsável pela consulta
from src.visualization import plot_radar_chart  # Módulo de visualização
import os

# Função principal para rodar o fluxo
def main():
    # Definindo o caminho do arquivo CSV que será gerado
    csv_file = 'data\\query_results.csv'

    # Exemplo de filtro para consulta
    filter_params = {
        "start_date": "2024-01-01T00:00:00.000Z",
        "end_date": "2024-10-31T00:00:00.000Z",
        "lang": "pt"
    }

    # Criação da instância do MongoHandler para a consulta
    # mongo_handler = MongoHandler()

    # Realizando a consulta e gerando o CSV
    #  mongo_handler.query_to_csv(csv_file, filter_params)

    # Gerar o gráfico se o CSV não estiver vazio
    plot_radar_chart(csv_file)

if __name__ == "__main__":
    main()
