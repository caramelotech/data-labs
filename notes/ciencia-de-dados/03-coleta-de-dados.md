# Coleta de Dados

## O que é coleta de dados

Coletar dados é reunir, de uma ou mais fontes, as informações necessárias para responder a pergunta do projeto. Parece a parte fácil, mas é onde muita coisa se decide: se o dado chega incompleto, enviesado ou mal documentado, nenhuma técnica depois conserta. É o famoso "garbage in, garbage out" (entra lixo, sai lixo).

Antes de sair baixando tudo, vale responder:

- Que pergunta eu quero responder e que colunas preciso para isso?
- Quem é o dono do dado e eu tenho permissão para usar? (se tiver dado pessoal, a LGPD se aplica)
- Com que frequência o dado é atualizado?
- O que cada coluna significa? Existe dicionário de dados?

## Tipos de dados

| Tipo            | Como é                                      | Exemplos                                          |
| --------------- | ------------------------------------------- | ------------------------------------------------- |
| Estruturado     | Linhas e colunas com esquema fixo           | CSV, planilhas Excel, tabelas de banco relacional |
| Semiestruturado | Tem marcação ou chaves, mas o formato varia | JSON, XML, logs, e-mails (cabeçalho + corpo)      |
| Não estruturado | Sem esquema definido                        | Texto livre, imagens, vídeo, áudio, PDF           |

O pandas trabalha com dados estruturados. Semiestruturados geralmente são "achatados" para tabela (você vai ver isso com JSON mais abaixo). Não estruturados precisam de técnicas próprias, como processamento de linguagem natural para texto ([NLP](/labs/data/machine-learning/06-processamento-de-linguagem-natural/)).

## De onde vêm os dados

- **Arquivos** - CSV e Excel exportados de sistemas, planilhas da equipe
- **Bancos de dados** - MySQL, PostgreSQL, SQL Server, SQLite; data warehouses como BigQuery, Redshift e Snowflake; bancos NoSQL como MongoDB
- **APIs** - serviços que devolvem dados sob demanda, normalmente em JSON (REST ou GraphQL)
- **Web scraping** - extrair dados de páginas HTML quando não existe API
- **Datasets públicos** - Kaggle, UCI Machine Learning Repository, portais de dados abertos como [dados.gov.br](https://dados.gov.br) e o IBGE
- **Sensores e IoT** - leituras de máquinas, GPS, medidores
- **Redes sociais** - via API oficial de cada plataforma, com regras de uso bem restritas

## O fluxo de coleta

```mermaid
flowchart LR
    A[Definir o problema] --> B[Identificar fontes]
    B --> C[Coletar]
    C --> D[Armazenar cópia bruta]
    D --> E[Validar]
    E --> F[Usar na análise]
    E -. dado com problema .-> B
```

Um hábito que poupa dor de cabeça: **guarde a versão bruta** do que coletou, sem nenhuma alteração, e faça a limpeza em cima de uma cópia. Se você errar algo na limpeza, volta para o bruto em vez de coletar de novo (e a API ou a página podem nem ter mais aquele dado).

## Lendo CSV com pandas

O caso mais comum. Para os exemplos, gere um CSV a partir do dataset de pinguins:

```python
import pandas as pd
import seaborn as sns

sns.load_dataset("penguins").to_csv("pinguins.csv", index=False)

df = pd.read_csv("pinguins.csv")
df.head()
```

Na vida real o arquivo raramente vem tão bonitinho. Os parâmetros que você mais vai usar:

| Parâmetro     | Para que serve                                                  | Exemplo                              |
| ------------- | --------------------------------------------------------------- | ------------------------------------ |
| `sep`         | Separador de colunas                                            | `sep=";"`                            |
| `decimal`     | Separador decimal                                               | `decimal=","`                        |
| `encoding`    | Codificação de caracteres                                       | `encoding="latin-1"`                 |
| `header`      | Linha do cabeçalho (`None` se não houver)                       | `header=None`                        |
| `usecols`     | Ler só algumas colunas                                          | `usecols=["species", "body_mass_g"]` |
| `nrows`       | Ler só as primeiras N linhas (bom para espiar arquivos grandes) | `nrows=1000`                         |
| `parse_dates` | Converter colunas para data                                     | `parse_dates=["data_pedido"]`        |
| `dtype`       | Forçar o tipo de colunas                                        | `dtype={"cep": "str"}`               |

O tropeço clássico no Brasil: CSV exportado do Excel em português vem com `;` como separador e `,` como decimal. Sem avisar o pandas, tudo vira uma coluna só, ou os números viram texto:

```python
df_br = pd.read_csv(
    "vendas.csv",
    sep=";",
    decimal=",",
    encoding="latin-1",       # arquivos antigos do Windows; tente "utf-8" primeiro
    usecols=["data", "produto", "valor"],
    parse_dates=["data"],
)
```

Outro: colunas como CEP, CPF ou código de produto com zero à esquerda. O pandas lê como número e o zero some. Use `dtype={"cep": "str"}`.

## Lendo Excel

```python
df = pd.read_excel("pinguins.xlsx", sheet_name="dados")
```

- Precisa do pacote `openpyxl` instalado (`pip install openpyxl`) para arquivos `.xlsx`
- `sheet_name` aceita o nome ou o índice da aba; `sheet_name=None` devolve um dicionário com todas as abas
- `skiprows` e `usecols` ajudam com planilhas que têm título, logotipo ou células mescladas no topo

## Lendo de bancos de dados com SQL

Para buscar dados num banco você escreve uma consulta SQL e o pandas transforma o resultado num DataFrame. Se SQL ainda é novidade, veja [Consultas com SELECT](/labs/data/sql/06-consultas-com-select/).

A ponte entre Python e o banco é o **SQLAlchemy**: ele cria uma conexão (`engine`) a partir de uma URL, e o `pd.read_sql` executa a consulta. O exemplo usa SQLite, que é um banco num arquivo e não precisa de servidor, então roda em qualquer máquina:

```python
import pandas as pd
import seaborn as sns
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///pinguins.db")

# só para o exemplo: grava o dataset numa tabela
sns.load_dataset("penguins").to_sql("pinguins", engine, if_exists="replace", index=False)

consulta = text("""
    SELECT species, island, body_mass_g
    FROM pinguins
    WHERE body_mass_g > :massa
""")

pesados = pd.read_sql(consulta, engine, params={"massa": 5000})
pesados.head()
```

Repare no `:massa` com `params`. Passar valores por parâmetro, em vez de montar a string com f-string, evita SQL injection e problemas com aspas.

Para outros bancos, só muda a URL (e o driver, que você instala com pip):

| Banco      | URL de conexão                                                                 | Driver              |
| ---------- | ------------------------------------------------------------------------------ | ------------------- |
| PostgreSQL | `postgresql+psycopg://usuario:senha@host:5432/banco`                           | `psycopg`           |
| MySQL      | `mysql+pymysql://usuario:senha@host:3306/banco`                                | `pymysql`           |
| SQL Server | `mssql+pyodbc://usuario:senha@host/banco?driver=ODBC+Driver+18+for+SQL+Server` | `pyodbc`            |
| SQLite     | `sqlite:///caminho/arquivo.db`                                                 | já vem com o Python |

BigQuery, Snowflake e Redshift têm conectores próprios com suporte a SQLAlchemy. MongoDB não é SQL: você usa o `pymongo` e converte a lista de documentos com `pd.DataFrame(...)`.

### Não deixe senha no código

Uma URL com usuário e senha escrita no notebook acaba no Git, num print, num e-mail. Leia de variáveis de ambiente:

```python
import os
from sqlalchemy import create_engine

engine = create_engine(os.environ["DATABASE_URL"])
```

No terminal você define `DATABASE_URL` antes de rodar, ou usa um arquivo `.env` (lido com a biblioteca `python-dotenv`) que **fica fora do Git** via `.gitignore`.

Uma dica de desempenho: filtre e agregue no banco, não no pandas. Trazer 50 milhões de linhas para depois fazer `groupby` na sua máquina é bem mais lento que um `GROUP BY` no servidor.

## Coletando de APIs

Uma API REST é um endereço na web que devolve dados (geralmente JSON) quando você faz uma requisição HTTP. Em Python, a biblioteca `requests` faz o trabalho. Exemplo com a [BrasilAPI](https://brasilapi.com.br), pública e sem chave, listando os feriados nacionais de 2026:

```python
import pandas as pd
import requests

resposta = requests.get("https://brasilapi.com.br/api/feriados/v1/2026", timeout=10)
resposta.raise_for_status()      # gera erro se o status não for 2xx

feriados = pd.json_normalize(resposta.json())
feriados.head()
```

O `pd.json_normalize` transforma JSON (inclusive aninhado) em tabela, criando colunas como `endereco.cidade` para campos dentro de campos.

Cuidados ao consumir APIs:

- **Sempre use `timeout`**, senão o script pode ficar parado para sempre esperando resposta
- **Chaves de API** vão em variável de ambiente, como as senhas de banco
- **Limite de requisições (rate limit)**: respeite. Se for buscar muitas páginas, coloque pausas e trate o status `429 Too Many Requests`
- **Paginação**: APIs costumam devolver os resultados em páginas; leia a documentação para saber como pedir a próxima

## Web scraping (noções)

Quando não há API, dá para extrair dados do HTML de uma página com `requests` + `BeautifulSoup` (`pip install beautifulsoup4`):

```python
import requests
from bs4 import BeautifulSoup

html = requests.get("https://exemplo.com/produtos", timeout=10).text
sopa = BeautifulSoup(html, "html.parser")

nomes = [item.get_text(strip=True) for item in sopa.select("h2.nome-produto")]
```

O seletor (`h2.nome-produto`) depende de como a página foi construída, por isso scraper quebra sempre que o site muda o layout. Se a página tem uma tabela HTML simples, `pd.read_html(url)` às vezes resolve sem BeautifulSoup.

Antes de fazer scraping:

- Leia os **termos de uso** do site; muitos proíbem coleta automatizada
- Respeite o arquivo `robots.txt` (`https://site.com/robots.txt`), que diz o que robôs podem acessar
- Não sobrecarregue o servidor: uma requisição por vez, com intervalo
- Cuidado com dados pessoais: coletar não dá direito de usar, a LGPD continua valendo

## Validando o que chegou

Logo depois de carregar, antes de qualquer análise:

```python
df.shape           # quantas linhas e colunas vieram (bate com o esperado?)
df.dtypes          # os tipos estão certos? número não veio como texto?
df.isna().sum()    # quanto falta em cada coluna
df.duplicated().sum()
```

Se algo estranhar, investigue na fonte antes de seguir. Como tratar o que estiver errado é assunto de [Limpeza e pré-processamento](/labs/data/ciencia-de-dados/04-limpeza-e-pre-processamento/).

## Referências

- [IO tools (text, CSV, HDF5, …)](https://pandas.pydata.org/docs/user_guide/io.html) - pandas, en
- [pandas.read_sql](https://pandas.pydata.org/docs/reference/api/pandas.read_sql.html) - pandas, en
- [SQLAlchemy - Engine Configuration](https://docs.sqlalchemy.org/en/20/core/engines.html) - SQLAlchemy, en
- [Requests - Quickstart](https://requests.readthedocs.io/en/latest/user/quickstart/) - Requests, en
