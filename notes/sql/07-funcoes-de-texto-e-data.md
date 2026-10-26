# Funções de texto e data

## Para que servem as funções

Funções recebem valores, fazem alguma transformação e devolvem um resultado. Elas aparecem no `SELECT` (para formatar a saída), no `WHERE` (para filtrar) e em qualquer lugar onde caiba uma expressão. Nesta nota ficam as funções de texto e de data, que são as que mais variam entre SGBDs. As funções de agregação (`COUNT`, `SUM`, `AVG`...) estão em [Agregações, GROUP BY e HAVING](/labs/data/sql/08-agregacoes-group-by-e-having/) e o `COALESCE` está em [Consultas com SELECT](/labs/data/sql/06-consultas-com-select/).

Os exemplos usam o esquema e os dados de [Constraints, chaves e relacionamentos](/labs/data/sql/03-constraints-chaves-e-relacionamentos/) e [Inserindo, atualizando e excluindo dados](/labs/data/sql/05-inserindo-atualizando-e-excluindo-dados/). Como nas outras funções, o resultado vale só para a consulta: nada é gravado, a não ser que você use a função dentro de um `UPDATE`.

## Funções de texto

### Juntando textos: CONCAT

```sql
SELECT CONCAT(nome, ' - ', cidade, '/', estado) AS cliente_local
FROM clientes;
-- Ana Souza - Fortaleza/CE
```

`CONCAT` existe nos três SGBDs, mas eles discordam sobre o que fazer com `NULL`, e isso aparece com o cliente Felipe, que não tem cidade nem estado:

|                                     | MySQL                                         | PostgreSQL                                       | SQL Server                                    |
| ----------------------------------- | --------------------------------------------- | ------------------------------------------------ | --------------------------------------------- |
| `CONCAT` com algum argumento `NULL` | Devolve `NULL` (a linha inteira some)         | Ignora o `NULL`                                  | Trata o `NULL` como texto vazio               |
| Operador de concatenação            | Não tem (`\|\|` é "ou" lógico no modo padrão) | `\|\|` (devolve `NULL` se algum lado for `NULL`) | `+` (devolve `NULL` se algum lado for `NULL`) |
| Juntar com separador                | `CONCAT_WS(', ', a, b)`                       | `CONCAT_WS(', ', a, b)`                          | `CONCAT_WS(', ', a, b)` (2017+)               |

Para um resultado igual nos três, trate o nulo antes: `CONCAT(nome, ' - ', COALESCE(cidade, 'sem cidade'))`. O `CONCAT_WS` ("with separator") pula os argumentos `NULL` nos três bancos, o que o torna bem prático para montar endereços.

### Maiúsculas e minúsculas: UPPER e LOWER

```sql
SELECT UPPER(nome) AS nome_maiusculo, LOWER(email) AS email_minusculo
FROM clientes;
```

Iguais nos três SGBDs. Um uso muito comum é comparar textos sem se preocupar com maiúsculas: `WHERE LOWER(email) = 'ana.souza@email.com'`.

### Tamanho do texto: LENGTH x CHAR_LENGTH

Aqui mora uma pegadinha que só aparece com acentos:

|                      | MySQL                | PostgreSQL                              | SQL Server                             |
| -------------------- | -------------------- | --------------------------------------- | -------------------------------------- |
| Número de caracteres | `CHAR_LENGTH(texto)` | `LENGTH(texto)` ou `CHAR_LENGTH(texto)` | `LEN(texto)` (ignora espaços no final) |
| Número de bytes      | `LENGTH(texto)`      | `OCTET_LENGTH(texto)`                   | `DATALENGTH(texto)`                    |

No MySQL, `LENGTH` conta **bytes**, não letras. Em UTF-8, letras sem acento ocupam 1 byte, mas `ã`, `é` e `ç` ocupam 2. Então:

```sql
-- MySQL, com UTF-8
SELECT LENGTH('São Paulo'), CHAR_LENGTH('São Paulo');
-- 10 e 9
```

Exemplos em inglês, como `LENGTH('Hello!')`, dão o mesmo número nas duas funções e escondem o problema. Para validar tamanho de nome ou de campo de formulário em português, use `CHAR_LENGTH` no MySQL.

### Pedaços do texto: SUBSTRING, LEFT e RIGHT

`SUBSTRING(texto, início, quantidade)` recorta um trecho. A contagem começa em 1, não em 0.

```sql
SELECT SUBSTRING('Database Systems', 1, 8);   -- Database
SELECT LEFT(nome, 3), RIGHT(email, 9) FROM clientes;
```

`LEFT` e `RIGHT` pegam os primeiros ou últimos caracteres e funcionam nos três. No MySQL e no PostgreSQL o terceiro argumento do `SUBSTRING` é opcional (sem ele, vai até o fim); no SQL Server é obrigatório. O PostgreSQL também aceita a forma do padrão SQL: `SUBSTRING(texto FROM 1 FOR 8)`.

### Procurando um caractere: posição

Para saber onde está um caractere ou trecho dentro do texto:

| MySQL                                            | PostgreSQL                                       | SQL Server              |
| ------------------------------------------------ | ------------------------------------------------ | ----------------------- |
| `LOCATE('@', email)` ou `POSITION('@' IN email)` | `POSITION('@' IN email)` ou `STRPOS(email, '@')` | `CHARINDEX('@', email)` |

Todas devolvem 0 quando não encontram. Combinando com `SUBSTRING`, dá para extrair o domínio do e-mail:

```sql
-- MySQL e PostgreSQL
SELECT email, SUBSTRING(email, POSITION('@' IN email) + 1) AS dominio
FROM clientes;

-- SQL Server
SELECT email, SUBSTRING(email, CHARINDEX('@', email) + 1, LEN(email)) AS dominio
FROM clientes;
```

### Limpando espaços: TRIM

Dados digitados à mão chegam com espaços sobrando, e `'Ana '` é diferente de `'Ana'` numa comparação (pelo menos no PostgreSQL; MySQL e SQL Server ignoram espaços no final ao comparar com `=` na maioria das collations).

```sql
SELECT TRIM('   Ana Souza   ');    -- 'Ana Souza'
SELECT LTRIM('   Ana');            -- tira só da esquerda
SELECT RTRIM('Ana   ');            -- tira só da direita
```

`TRIM` existe no SQL Server a partir da versão 2017; antes disso, use `LTRIM(RTRIM(texto))`. O padrão SQL também permite escolher o caractere a remover, como `TRIM(BOTH '.' FROM texto)` no MySQL e no PostgreSQL.

### Trocando trechos: REPLACE

`REPLACE(texto, procurado, substituto)` troca todas as ocorrências:

```sql
SELECT REPLACE('(85) 99999-0000', '-', '');   -- (85) 999990000
SELECT REPLACE(nome, 'Notebook', 'Laptop') FROM produtos;
```

Funciona igual nos três. No MySQL e no PostgreSQL, a busca do `REPLACE` diferencia maiúsculas; no SQL Server, segue a collation (que por padrão não diferencia).

### Limpeza de dados na prática

As funções de texto brilham na limpeza de dados. Encontrar e-mails duplicados que só diferem por espaço ou maiúscula, por exemplo, exige normalizar antes de comparar:

```sql
SELECT LOWER(TRIM(email)) AS email_normalizado
FROM clientes;
```

Agrupando por esse valor e contando, você acha as duplicatas (veja [Agregações, GROUP BY e HAVING](/labs/data/sql/08-agregacoes-group-by-e-having/)). Para corrigir de vez, use a mesma expressão num `UPDATE`:

```sql
UPDATE clientes SET email = LOWER(TRIM(email));
```

Esse é um dos raros casos em que um `UPDATE` sem `WHERE` é intencional. Mesmo assim, rode dentro de uma transação (veja [Inserindo, atualizando e excluindo dados](/labs/data/sql/05-inserindo-atualizando-e-excluindo-dados/)).

## Funções de data e hora

Datas são onde os dialetos mais se afastam. As ideias são as mesmas em todo lugar (pegar a data de hoje, extrair o mês, somar dias, calcular diferenças), mas quase cada função tem um nome diferente. Vale manter os quadros abaixo por perto.

### Data e hora atuais

| O que você quer | MySQL                          | PostgreSQL                     | SQL Server                                          |
| --------------- | ------------------------------ | ------------------------------ | --------------------------------------------------- |
| Data e hora     | `NOW()` ou `CURRENT_TIMESTAMP` | `NOW()` ou `CURRENT_TIMESTAMP` | `GETDATE()`, `SYSDATETIME()` ou `CURRENT_TIMESTAMP` |
| Só a data       | `CURDATE()` ou `CURRENT_DATE`  | `CURRENT_DATE`                 | `CAST(GETDATE() AS DATE)`                           |
| Só a hora       | `CURTIME()` ou `CURRENT_TIME`  | `CURRENT_TIME`                 | `CAST(GETDATE() AS TIME)`                           |

`CURRENT_TIMESTAMP` é a forma do padrão SQL e funciona nos três. Todas essas funções usam o relógio e o fuso do servidor (ou da sessão), não do seu computador. Se o servidor estiver em UTC, "hoje" pode virar amanhã às 21h no horário de Brasília.

### Extraindo partes da data

| Parte          | MySQL                      | PostgreSQL                                               | SQL Server              |
| -------------- | -------------------------- | -------------------------------------------------------- | ----------------------- |
| Ano            | `YEAR(data)`               | `EXTRACT(YEAR FROM data)`                                | `YEAR(data)`            |
| Mês            | `MONTH(data)`              | `EXTRACT(MONTH FROM data)`                               | `MONTH(data)`           |
| Dia            | `DAY(data)`                | `EXTRACT(DAY FROM data)`                                 | `DAY(data)`             |
| Forma genérica | `EXTRACT(MONTH FROM data)` | `EXTRACT(MONTH FROM data)` ou `DATE_PART('month', data)` | `DATEPART(month, data)` |

```sql
-- MySQL e SQL Server
SELECT id, data_pedido, YEAR(data_pedido) AS ano, MONTH(data_pedido) AS mes
FROM pedidos;
```

`EXTRACT` é do padrão SQL e funciona no MySQL e no PostgreSQL, mas não no SQL Server.

### Somando e subtraindo tempo

|               | MySQL                                                       | PostgreSQL                                             | SQL Server                 |
| ------------- | ----------------------------------------------------------- | ------------------------------------------------------ | -------------------------- |
| 7 dias depois | `DATE_ADD(data, INTERVAL 7 DAY)` ou `data + INTERVAL 7 DAY` | `data + INTERVAL '7 days'` (ou `data + 7` para `DATE`) | `DATEADD(day, 7, data)`    |
| 1 mês antes   | `DATE_SUB(data, INTERVAL 1 MONTH)`                          | `data - INTERVAL '1 month'`                            | `DATEADD(month, -1, data)` |

```sql
-- MySQL: previsão de entrega 7 dias após o pedido
SELECT id, data_pedido, DATE_ADD(data_pedido, INTERVAL 7 DAY) AS previsao_entrega
FROM pedidos;
-- DATE_ADD('2025-05-15', INTERVAL 7 DAY) = 2025-05-22
```

Somar meses tem um detalhe: 31 de janeiro mais 1 mês dá 28 (ou 29) de fevereiro nos três bancos, porque o dia é ajustado para o último dia válido do mês.

### Diferença entre datas

Aqui está a maior armadilha da nota: a mesma função `DATEDIFF` tem assinaturas diferentes, e o sinal do resultado se inverte.

|                       | MySQL                               | PostgreSQL                                           | SQL Server                     |
| --------------------- | ----------------------------------- | ---------------------------------------------------- | ------------------------------ |
| Dias entre duas datas | `DATEDIFF(fim, inicio)`             | `fim - inicio` (com tipo `DATE`, devolve um inteiro) | `DATEDIFF(day, inicio, fim)`   |
| Em outras unidades    | `TIMESTAMPDIFF(MONTH, inicio, fim)` | `AGE(fim, inicio)` ou `EXTRACT` sobre o intervalo    | `DATEDIFF(month, inicio, fim)` |

```sql
-- Dias desde a admissão de cada funcionário
SELECT nome, DATEDIFF(CURDATE(), data_admissao) AS dias_de_casa FROM funcionarios;              -- MySQL
SELECT nome, CURRENT_DATE - data_admissao AS dias_de_casa FROM funcionarios;                    -- PostgreSQL
SELECT nome, DATEDIFF(day, data_admissao, CAST(GETDATE() AS DATE)) AS dias_de_casa FROM funcionarios;  -- SQL Server
```

Repare: no MySQL a data mais recente vem **primeiro**; no SQL Server, a unidade vem primeiro e a data mais recente vem **por último**. Copiar um `DATEDIFF` de um banco para o outro sem ajustar dá resultado com sinal trocado ou erro.

Outro detalhe do SQL Server: `DATEDIFF` conta quantas **fronteiras** da unidade foram cruzadas, não períodos completos. `DATEDIFF(year, '2024-12-31', '2025-01-01')` dá 1, embora tenha passado só um dia. Para calcular idade ou tempo de casa em anos, compare também mês e dia, ou use `TIMESTAMPDIFF(YEAR, ...)` no MySQL e `AGE` no PostgreSQL, que contam anos completos.

### Formatando datas para exibição

| Exibir como 15/05/2025 | Função                                                            |
| ---------------------- | ----------------------------------------------------------------- |
| MySQL                  | `DATE_FORMAT(data, '%d/%m/%Y')`                                   |
| PostgreSQL             | `TO_CHAR(data, 'DD/MM/YYYY')`                                     |
| SQL Server             | `FORMAT(data, 'dd/MM/yyyy')` ou `CONVERT(VARCHAR(10), data, 103)` |

O resultado dessas funções é **texto**, não data. Use-as só na saída final: ordenar ou comparar pela versão formatada dá resultados errados (`'02/03/2025'` vem antes de `'15/01/2025'` em ordem alfabética).

### Agrupando por mês

Para relatórios mensais, é comum "arredondar" cada data para o primeiro dia do mês:

| MySQL                           | PostgreSQL                  | SQL Server                                                                      |
| ------------------------------- | --------------------------- | ------------------------------------------------------------------------------- |
| `DATE_FORMAT(data, '%Y-%m-01')` | `DATE_TRUNC('month', data)` | `DATETRUNC(month, data)` (2022+) ou `DATEFROMPARTS(YEAR(data), MONTH(data), 1)` |

Esse valor vira a chave de um `GROUP BY` em consultas como "faturamento por mês":

```sql
-- PostgreSQL
SELECT DATE_TRUNC('month', data_pedido) AS mes, SUM(valor_total) AS faturamento
FROM pedidos
WHERE status <> 'cancelado'
GROUP BY DATE_TRUNC('month', data_pedido)
ORDER BY mes;
```

O funcionamento do `GROUP BY` e do `SUM` está em [Agregações, GROUP BY e HAVING](/labs/data/sql/08-agregacoes-group-by-e-having/).

### Convertendo texto em data

`CAST('2025-05-15' AS DATE)` funciona nos três SGBDs. Para textos em outros formatos, cada banco tem sua função: `STR_TO_DATE('15/05/2025', '%d/%m/%Y')` no MySQL, `TO_DATE('15/05/2025', 'DD/MM/YYYY')` no PostgreSQL e `CONVERT(DATE, '15/05/2025', 103)` no SQL Server.

### Funções na coluna do WHERE deixam a consulta lenta

Esta consulta está correta, mas tem um problema de desempenho:

```sql
SELECT id FROM pedidos WHERE YEAR(data_pedido) = 2025;
```

Como a função é aplicada à coluna, o banco precisa calcular `YEAR()` para cada linha antes de comparar, e um índice em `data_pedido` deixa de ser aproveitado. Escrevendo como intervalo, o índice volta a funcionar e o resultado é o mesmo:

```sql
SELECT id FROM pedidos
WHERE data_pedido >= '2025-01-01' AND data_pedido < '2026-01-01';
```

O mesmo vale para funções de texto: `WHERE LOWER(email) = '...'` também impede o uso de um índice comum em `email`. Em tabelas pequenas a diferença é invisível; em tabelas grandes, pode ser a diferença entre milissegundos e minutos. Índices estão em [Views, índices e triggers](/labs/data/sql/11-views-indices-e-triggers/).

## Referências

- [Funções de cadeia de caracteres (Transact-SQL)](https://learn.microsoft.com/pt-br/sql/t-sql/functions/string-functions-transact-sql) - Microsoft Learn, pt-BR
- [Tipos de dados e funções de data e hora (Transact-SQL)](https://learn.microsoft.com/pt-br/sql/t-sql/functions/date-and-time-data-types-and-functions-transact-sql) - Microsoft Learn, pt-BR
- [Funções e operadores de cadeia de caracteres (documentação do PostgreSQL)](https://halleyoliv.gitlab.io/pgdocptbr/functions-string.html) - tradução de Halley Pacheco de Oliveira da documentação oficial, pt-BR
- [String Functions and Operators](https://dev.mysql.com/doc/refman/8.4/en/string-functions.html) - Oracle/MySQL, en
- [Date and Time Functions](https://dev.mysql.com/doc/refman/8.4/en/date-and-time-functions.html) - Oracle/MySQL, en
