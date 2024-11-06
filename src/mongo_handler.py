import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd

# Carregar variáveis de ambiente
load_dotenv()

class MongoHandler:
    def __init__(self):
        # Inicializa a conexão com MongoDB
        self.client = MongoClient(os.getenv("MONGO_URI"))
        self.db = self.client[os.getenv("DATABASE_NAME")]
    
    def get_review_summary(self, app_ids, start_date, end_date, langs=['pt']):
        # Pipeline de agregação com filtros de data e idioma
        pipeline = [
            {"$match": {
                "appId": {"$in": app_ids},
                "date": {"$gte": start_date, "$lte": end_date},
                "lang": {"$in": langs}
            }},
            {"$addFields": {"month": {"$month": "$date"}}},
            {"$group": {
                "_id": {
                    "appId": "$appId",
                    "month": "$month",
                    "subcategory": "$subcategory"
                },
                "count": {"$sum": 1},
                "avgScore": {"$avg": "$score"}
            }},
            {"$sort": {"_id.appId": 1, "_id.month": 1}}
        ]
        
        # Executa a agregação e retorna os resultados como DataFrame
        collection = self.db["reviews"]
        results = list(collection.aggregate(pipeline))
        
        data = [
            {
                "appId": result["_id"]["appId"],
                "month": result["_id"]["month"],
                "subcategory": result["_id"]["subcategory"],
                "count": result["count"],
                "avg_score": result["avgScore"]
            }
            for result in results
        ]
        
        return pd.DataFrame(data)
    
    def close_connection(self):
        # Fecha a conexão com o MongoDB
        self.client.close()
