# main.py

from datetime import datetime
from src.mongo_handler import MongoHandler  # Classe responsável pela consulta
from src.visualization import plot_radar_chart  # Módulo de visualização
import os

# Função principal para rodar o fluxo
def main():
    # Lista de appIds, data inicial, data final e idiomas
    app_ids = ["ws.hanzo.Vrrh", "br.com.santander.benvisavale", "br.com.ifood.benefits", "com.primety.sodexomobile","com.caju.employeeApp","br.com.flashapp", "br.com.mobile.ticket"]
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 10, 31)
    langs = ["pt"]

    # Caminho para o arquivo CSV gerado
    csv_file = "data\\review_summary.csv" 

    # Verifica se o arquivo CSV existe
    if os.path.exists(csv_file):
        os.remove(csv_file)
        print("Arquivo CSV removido: review_summary.csv")

    # Inicializa o manipulador do MongoDB e faz a consulta
    mongo_handler = MongoHandler()
    df = mongo_handler.get_review_summary(app_ids, start_date, end_date, langs)
    
    # Salva o DataFrame em CSV
    df.to_csv(csv_file, index=False, sep=';')
    print(f"Arquivo CSV gerado: {csv_file}")
    
    # Fecha a conexão com o MongoDB
    mongo_handler.close_connection()

    # Verificar se o CSV está vazio
    if os.stat(csv_file).st_size == 0:
        print("O CSV está vazio, nenhum gráfico será gerado.")

    # Gerar o gráfico se o CSV não estiver vazio
    plot_radar_chart(csv_file)

if __name__ == "__main__":
    main()
