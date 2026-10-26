# Bancos, tabelas e tipos de dados

## Criando e usando um banco de dados

Antes de criar tabelas, você precisa de um banco para guardá-las. Os comandos que criam e removem estruturas fazem parte da DDL (veja as categorias em [Introdução ao SQL](/labs/data/sql/01-introducao-ao-sql/)).

```sql
CREATE DATABASE loja;
```

Pronto, o banco `loja` existe, mas ainda está vazio. Agora é preciso dizer ao SGBD que os próximos comandos são para ele:

|                 | MySQL       | PostgreSQL                                                                                          | SQL Server  |
| --------------- | ----------- | --------------------------------------------------------------------------------------------------- | ----------- |
| Trocar de banco | `USE loja;` | Não existe `USE`: você troca a conexão (`\c loja` no `psql`, ou escolhe o banco no pgAdmin/DBeaver) | `USE loja;` |

No PostgreSQL cada conexão fica presa a um banco, por isso a troca é feita pela ferramenta, não por um comando SQL.

### Removendo um banco

```sql
DROP DATABASE IF EXISTS loja;
```

`DROP DATABASE` apaga o banco inteiro, com todas as tabelas e dados. Não tem lixeira. 🗑️

O `IF EXISTS` evita um erro caso o banco não exista. Isso é útil em scripts que você roda várias vezes: sem ele, a segunda execução pararia com "database doesn't exist". O mesmo vale para `CREATE DATABASE IF NOT EXISTS loja;` (MySQL) e para `DROP TABLE IF EXISTS` (os três SGBDs; no SQL Server a partir da versão 2016).

## Tabelas: a estrutura onde os dados moram

Uma tabela é parecida com uma planilha, mas com regras mais rígidas: cada coluna tem um **nome**, um **tipo de dado** e, opcionalmente, **constraints** (regras como "não pode ficar vazio").

```sql
CREATE TABLE produtos (
    id        INT PRIMARY KEY,
    nome      VARCHAR(100) NOT NULL,
    categoria VARCHAR(50),
    preco     DECIMAL(10, 2) NOT NULL,
    estoque   INT
);
```

Lendo de dentro para fora: a tabela `produtos` tem cinco colunas. `id` é um número inteiro e identifica cada produto (`PRIMARY KEY`); `nome` é um texto de até 100 caracteres e é obrigatório (`NOT NULL`); `preco` é um número decimal exato com duas casas.

A sintaxe geral é:

```sql
CREATE TABLE nome_da_tabela (
    coluna1 TIPO [constraints],
    coluna2 TIPO [constraints],
    ...
    [constraints de tabela]
);
```

As constraints e as chaves têm uma nota própria: [Constraints, chaves e relacionamentos](/labs/data/sql/03-constraints-chaves-e-relacionamentos/). Lá também está o esquema completo de exemplo (`clientes`, `pedidos`, `produtos`, `funcionarios` e companhia) usado nas outras notas.

Pensar bem na estrutura antes de criar a tabela poupa trabalho depois. Uma coluna `preco` guardada como texto, por exemplo, impede somas e ordenações corretas; uma coluna `nome_completo` que mistura nome e sobrenome complica buscas. A nota de [Normalização](/labs/data/sql/12-normalizacao/) trata de como dividir os dados entre tabelas.

## Tipos de dados

O tipo de dado diz o que a coluna aceita. Ele protege os dados (não dá para gravar "abc" numa coluna `INT`), define quanto espaço cada valor ocupa e quais operações fazem sentido (somar números, comparar datas).

### Números inteiros

| Tipo                 | Faixa aproximada           | Uso típico                         |
| -------------------- | -------------------------- | ---------------------------------- |
| `SMALLINT`           | -32 mil a 32 mil           | Quantidades pequenas, códigos      |
| `INT` (ou `INTEGER`) | -2,1 bilhões a 2,1 bilhões | IDs, quantidades, idades           |
| `BIGINT`             | cerca de 9,2 quintilhões   | IDs de tabelas enormes, contadores |

Os três existem com esses nomes em MySQL, PostgreSQL e SQL Server.

### DECIMAL x FLOAT: exato x aproximado

Aqui mora uma das armadilhas mais comuns.

- `DECIMAL(p, s)` (ou `NUMERIC`) guarda o número **exato**. `p` é a precisão (total de dígitos) e `s` a escala (dígitos depois da vírgula). `DECIMAL(10, 2)` aceita até `99999999.99`.
- `FLOAT`, `DOUBLE` e `REAL` são de **ponto flutuante**: guardam uma aproximação em binário. São rápidos e ótimos para medições científicas, mas números como `0.1` não têm representação binária exata, então pequenos erros de arredondamento aparecem em somas e comparações.

Regra prática: **dinheiro, preço e salário sempre em `DECIMAL`**. Uma coluna `salario FLOAT`, comum em exemplos de tutorial, pode fazer `WHERE salario = 3500.10` não encontrar a linha que você acabou de gravar.

| Tipo aproximado  | MySQL    | PostgreSQL         | SQL Server |
| ---------------- | -------- | ------------------ | ---------- |
| Precisão simples | `FLOAT`  | `REAL`             | `REAL`     |
| Precisão dupla   | `DOUBLE` | `DOUBLE PRECISION` | `FLOAT`    |

Repare que `FLOAT` significa coisas diferentes no MySQL e no SQL Server. Mais um motivo para usar `DECIMAL` quando o valor precisa ser exato.

### Texto: CHAR x VARCHAR

- `CHAR(n)` tem **tamanho fixo**: sempre ocupa `n` caracteres, completando com espaços à direita. `'CE'` num `CHAR(5)` vira `'CE   '`.
- `VARCHAR(n)` tem **tamanho variável**: ocupa só o necessário, até o limite `n`.

Quando usar cada um:

- `CHAR` para valores que têm sempre o mesmo tamanho: sigla de estado (`CHAR(2)`), código de país no padrão ISO 3166 (`'BR'`, `'US'`), indicador de uma letra.
- `VARCHAR` para o resto: nomes, e-mails, descrições curtas.

É comum ler que "`CHAR` é mais rápido". Isso já foi verdade em alguns bancos antigos, mas não é regra: a documentação do PostgreSQL afirma que não há diferença de desempenho e que `char(n)` costuma ser o mais lento dos três tipos de texto, por causa do preenchimento com espaços. Escolha pelo significado do dado, não pela suposta velocidade.

Para textos longos (descrições, comentários), use `TEXT` (MySQL e PostgreSQL) ou `VARCHAR(MAX)` (SQL Server).

Um cuidado no SQL Server: declarar `VARCHAR` sem tamanho numa coluna ou variável equivale a `VARCHAR(1)`. Sempre informe o tamanho.

#### Telefone é texto, não número

Telefone, CEP e CPF parecem números, mas não são: você nunca vai somar dois telefones, eles podem ter zeros à esquerda (`01310-100`) e podem levar `+`, parênteses e hífen. Guarde em `VARCHAR`. Para telefones internacionais, o padrão E.164 (`+5585999990000`) tem no máximo 15 dígitos, então um `VARCHAR(20)` sobra.

### Datas e horas

| Necessidade          | MySQL                           | PostgreSQL                                 | SQL Server                           |
| -------------------- | ------------------------------- | ------------------------------------------ | ------------------------------------ |
| Só a data            | `DATE`                          | `DATE`                                     | `DATE`                               |
| Só a hora            | `TIME`                          | `TIME`                                     | `TIME`                               |
| Data e hora          | `DATETIME` ou `TIMESTAMP`       | `TIMESTAMP`                                | `DATETIME2` (ou o antigo `DATETIME`) |
| Data e hora com fuso | `TIMESTAMP` (converte para UTC) | `TIMESTAMPTZ` (`TIMESTAMP WITH TIME ZONE`) | `DATETIMEOFFSET`                     |
| Só o ano             | `YEAR`                          | não tem (use `INT` ou `DATE`)              | não tem                              |

Os literais de data seguem o formato ISO 8601, `'AAAA-MM-DD'`: `'2025-05-15'`. Esse é o formato que você escreve e o que os bancos aceitam sem ambiguidade; internamente, cada SGBD guarda a data do seu jeito. Evite `'15/05/2025'`, que depende de configuração regional e pode ser lido errado.

#### DATETIME x TIMESTAMP no MySQL

Os dois guardam data e hora, mas se comportam de forma diferente:

|              | `DATETIME`                                        | `TIMESTAMP`                                                         |
| ------------ | ------------------------------------------------- | ------------------------------------------------------------------- |
| Faixa        | de `1000-01-01` a `9999-12-31`                    | de `1970-01-01` a `2038-01-19` (UTC)                                |
| Fuso horário | Grava exatamente o que você mandou                | Converte para UTC ao gravar e de volta para o fuso da sessão ao ler |
| Uso típico   | Datas de negócio (data de nascimento, vencimento) | Registro de quando algo aconteceu (`criado_em`)                     |

O limite de 2038 do `TIMESTAMP` é real: uma data de vencimento de contrato em 2040 não cabe ali.

#### Cuidado: `timestamp` no SQL Server não é data

No SQL Server, `timestamp` é um nome antigo (e obsoleto) para `rowversion`, um contador binário que muda toda vez que a linha é alterada. Ele **não guarda data nem hora**. Para data e hora no SQL Server, use `DATETIME2`.

### Verdadeiro ou falso

| MySQL                                                             | PostgreSQL                            | SQL Server    |
| ----------------------------------------------------------------- | ------------------------------------- | ------------- |
| `BOOLEAN` (na verdade um apelido para `TINYINT(1)`, guarda 0 e 1) | `BOOLEAN` (`true`/`false` de verdade) | `BIT` (0 e 1) |

### Guia rápido: qual tipo usar

| Dado                                 | Tipo sugerido                                              |
| ------------------------------------ | ---------------------------------------------------------- |
| ID numérico                          | `INT` ou `BIGINT`                                          |
| Nome de pessoa ou produto            | `VARCHAR(100)`                                             |
| E-mail                               | `VARCHAR(150)`                                             |
| Sigla do estado                      | `CHAR(2)`                                                  |
| Telefone, CEP, CPF                   | `VARCHAR`                                                  |
| Idade, quantidade em estoque         | `INT`                                                      |
| Preço, salário                       | `DECIMAL(10, 2)`                                           |
| Data do pedido                       | `DATE`                                                     |
| Momento em que o registro foi criado | `TIMESTAMP` (MySQL/PostgreSQL) ou `DATETIME2` (SQL Server) |
| Ativo/inativo                        | `BOOLEAN` (ou `BIT` no SQL Server)                         |

## Conferindo a estrutura de uma tabela

Depois de criar uma tabela, é bom conferir se ficou como você queria.

| MySQL                                      | PostgreSQL                | SQL Server                 |
| ------------------------------------------ | ------------------------- | -------------------------- |
| `DESCRIBE produtos;` (ou `DESC produtos;`) | `\d produtos` (no `psql`) | `EXEC sp_help 'produtos';` |

O resultado mostra cada coluna, seu tipo, se aceita nulos, se é chave e o valor padrão. Se quiser um comando que funcione nos três, consulte os metadados pelo `information_schema`:

```sql
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'produtos';
```

Para mudar a estrutura de uma tabela que já existe (adicionar coluna, mudar tipo, renomear), veja [Alterando a estrutura](/labs/data/sql/04-alterando-a-estrutura/).

## Referências

- [Tipos de dados (Transact-SQL)](https://learn.microsoft.com/pt-br/sql/t-sql/data-types/data-types-transact-sql) - Microsoft Learn, pt-BR
- [Capítulo 8. Tipos de dados (documentação do PostgreSQL)](https://halleyoliv.gitlab.io/pgdocptbr/datatype.html) - tradução de Halley Pacheco de Oliveira da documentação oficial, pt-BR
- [Data Types](https://dev.mysql.com/doc/refman/8.4/en/data-types.html) - Oracle/MySQL, en
- [The DATE, DATETIME, and TIMESTAMP Types](https://dev.mysql.com/doc/refman/8.4/en/datetime.html) - Oracle/MySQL, en
- [Character Types](https://www.postgresql.org/docs/current/datatype-character.html) - PostgreSQL Global Development Group, en
