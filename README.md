# MongoDB Reviews Aggregator

Este projeto extrai dados de avaliações de aplicativos no MongoDB, calcula estatísticas mensais por subcategoria e gera um relatório em CSV.

## Estrutura do Projeto

- `main.py`: Arquivo principal para executar o script.
- `src/mongo_handler.py`: Classe `MongoHandler` para manipulação e consultas no MongoDB.
- `.env`: Armazena variáveis de ambiente, como URI do MongoDB.

## Configuração

1. Clone o repositório.
2. Crie um ambiente virtual e instale as dependências:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. Configure a string de conexão no arquivo `.env`:

    ```plaintext
    MONGO_URI="sua_uri_mongodb"
    DATABASE_NAME="ReviewsGplay"
    ```

## Uso

Execute o script principal para gerar o arquivo CSV com o resumo das avaliações:

```bash
python main.py
```

## Estrutura do CSV de Saída
O CSV gerado terá as colunas:

- appId: Identificador do aplicativo.
- month: Mês de avaliação.
- subcategory: Subcategoria da avaliação.
- count: Contagem de avaliações.
- avg_score: Média de rating das avaliações.