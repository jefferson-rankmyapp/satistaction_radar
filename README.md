# Projeto de Análise de Satisfação dos Usuários

Este projeto realiza a análise de satisfação dos usuários de diferentes aplicativos, com foco nas avaliações de subcategorias, ratings médios, e volumes de feedback por app. A aplicação é implementada em Python e utiliza o MongoDB para consultas de dados e Plotly para visualizações interativas.

## Estrutura do Projeto

- `main.py`: Arquivo principal para execução do projeto.
- `src/`: Pasta de módulos com funcionalidades organizadas.
  - `mongo_handler.py`: Gerencia a conexão e consultas ao MongoDB.
  - `data_processing.py`: Processa e organiza os dados para análise.
  - `visualization.py`: Gera os gráficos de radar interativos, incluindo gráficos por app específico.
- `data/`: Contém arquivos de dados, incluindo o logotipo da organização.
- `README.md`: Instruções e informações sobre o projeto.
- `.env`: Arquivo com configurações de ambiente, incluindo a string de conexão ao MongoDB.
- `.gitignore`: Define arquivos e diretórios a serem ignorados pelo Git.

## Funcionalidades

### Coleta e Processamento de Dados

1. **Consulta ao MongoDB**: Extrai avaliações de apps com base em filtros, incluindo período e idioma.
2. **Processamento de Dados**: Agrupa os dados para cada `appId` por subcategoria, calcula a média de rating e o volume total.

### Visualizações Interativas

O projeto oferece visualizações no formato de gráfico de radar interativo, permitindo explorar as avaliações e comparar subcategorias de forma intuitiva.

- **Gráfico de Radar Geral**: Apresenta a média de rating e volume de feedback para cada appId, permitindo uma visão geral de múltiplos apps.
- **Gráfico de Radar por App**: Fornece uma visão específica para um `appId`, detalhando as subcategorias com a média de rating e o volume de feedback.

### Interface Streamlit

A interface Streamlit foi desenvolvida para facilitar a visualização e manipulação dos dados, com as seguintes funcionalidades:

- **Título e Logotipo**: Exibe o nome da organização e logotipo.
- **Tabela de Dados**: Mostra uma tabela com os dados agrupados por subcategoria e appId.
- **Gráfico Interativo**: Renderiza o gráfico de radar diretamente na interface.
- **Seleção de App**: Permite ao usuário selecionar um `appId` específico para visualizar o gráfico de radar por app.

## Requisitos e Instalação

1. Clone o repositório e entre no diretório do projeto.
2. Crie um ambiente virtual e ative-o:
```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
```

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
    MONGO_GPLAY_URI="sua_uri_mongodb"
    DATABASE_NAME="nome_do_database"
    ```

Para executar a aplicação Streamlit, use:
```bash
streamlit run main.py
```

## Exemplo de Uso
* Interface Geral: A interface exibe o título, logotipo, e uma breve explicação do projeto.
* Visualização dos Dados: A tabela apresenta os dados processados, incluindo o appId, subcategoria, rating médio, e volume.
* Gráfico de Radar: Interaja com o gráfico de radar para explorar ratings médios e volumes por subcategoria para cada appId.
* Filtro de AppId: Selecione um appId específico para visualizar o gráfico de radar exclusivo. Use a tabela de dados como referência.

Projeto criado com Python, MongoDB, e Streamlit. Agradecemos pelo uso e contribuições.