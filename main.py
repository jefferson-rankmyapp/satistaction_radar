from datetime import datetime
from src.mongo_handler import MongoHandler

def main():
    # Lista de appIds, data inicial, data final e idiomas
    app_ids = ["ws.hanzo.Vrrh", "br.com.santander.benvisavale", "br.com.ifood.benefits"]
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 10, 31)
    langs = ["pt"]

    # Inicializa o manipulador do MongoDB e faz a consulta
    mongo_handler = MongoHandler()
    df = mongo_handler.get_review_summary(app_ids, start_date, end_date, langs)
    
    # Salva o DataFrame em CSV
    df.to_csv("review_summary.csv", index=False, sep=';')
    print("Arquivo CSV gerado: review_summary.csv")
    
    # Fecha a conexão com o MongoDB
    mongo_handler.close_connection()

if __name__ == "__main__":
    main()
