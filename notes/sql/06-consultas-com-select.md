# Consultas com SELECT

## A estrutura de um SELECT

O `SELECT` é o comando que você mais vai escrever. Ele só lê: não altera nenhuma linha, então pode testar à vontade. Os exemplos usam o esquema e os dados de exemplo de [Constraints, chaves e relacionamentos](/labs/data/sql/03-constraints-chaves-e-relacionamentos/) e [Inserindo, atualizando e excluindo dados](/labs/data/sql/05-inserindo-atualizando-e-excluindo-dados/).

```sql
SELECT nome, preco          -- quais colunas
FROM produtos               -- de qual tabela
WHERE categoria = 'Móveis'  -- quais linhas
ORDER BY preco DESC;        -- em que ordem
```

Só `SELECT` e `FROM` são obrigatórios. As outras cláusulas entram conforme a pergunta, sempre nesta ordem de escrita: `SELECT`, `FROM`, `WHERE`, `GROUP BY`, `HAVING`, `ORDER BY` e a limitação de linhas. `GROUP BY` e `HAVING` ficam para [Agregações, GROUP BY e HAVING](/labs/data/sql/08-agregacoes-group-by-e-having/).

### Todas as colunas ou só as que você precisa

```sql
SELECT * FROM clientes;              -- todas as colunas
SELECT nome, cidade FROM clientes;   -- só duas
```

O `*` é ótimo para dar uma espiada numa tabela. Em consultas que vão para relatório, aplicação ou pipeline, liste as colunas: você traz menos dados, deixa claro o que está usando e a consulta não muda de comportamento quando alguém adicionar uma coluna na tabela.

### Colunas calculadas

O `SELECT` aceita expressões, não só nomes de colunas:

```sql
SELECT nome, preco, estoque, preco * estoque AS valor_em_estoque
FROM produtos;
```

O cálculo vale só para o resultado; nada é gravado na tabela.

## Aliases: dando apelidos

`AS` dá um nome para a coluna no resultado. Também serve para apelidar tabelas, o que fica indispensável quando há joins (veja [Joins](/labs/data/sql/09-joins/)).

```sql
SELECT c.nome AS cliente, c.cidade AS cidade_cliente
FROM clientes AS c;
```

O `AS` é opcional (`c.nome cliente` funciona), mas escrever deixa a leitura mais fácil. Para tabelas, o Oracle nem aceita o `AS`; nos três SGBDs desta seção ele é permitido.

Se o apelido tiver espaço ou acento, precisa de delimitador, e aí cada banco tem seu jeito:

| Padrão SQL e PostgreSQL | MySQL                                                      | SQL Server                                             |
| ----------------------- | ---------------------------------------------------------- | ------------------------------------------------------ |
| `AS "Nome do cliente"`  | `` AS `Nome do cliente` `` (aspas duplas também funcionam) | `AS [Nome do cliente]` (aspas duplas também funcionam) |

Muito tutorial de MySQL usa aspas simples (`AS 'Nome do cliente'`). O MySQL aceita, mas o PostgreSQL não, e aspas simples no padrão SQL são para textos, não para nomes. O caminho mais tranquilo é usar apelidos sem espaço, em `snake_case`: `AS nome_cliente`.

Um detalhe que pega todo mundo: o apelido criado no `SELECT` **não pode ser usado no `WHERE`**.

```sql
-- Erro: valor_em_estoque ainda não existe quando o WHERE é avaliado
SELECT nome, preco * estoque AS valor_em_estoque
FROM produtos
WHERE valor_em_estoque > 10000;

-- Certo: repita a expressão
SELECT nome, preco * estoque AS valor_em_estoque
FROM produtos
WHERE preco * estoque > 10000;
```

Isso acontece porque o banco não executa a consulta na ordem em que você escreve: o `WHERE` é processado antes do `SELECT`. A ordem lógica completa está em [Agregações, GROUP BY e HAVING](/labs/data/sql/08-agregacoes-group-by-e-having/). O `ORDER BY`, que vem depois do `SELECT`, aceita o apelido normalmente.

## DISTINCT: removendo repetições

```sql
SELECT DISTINCT categoria FROM produtos;
```

Devolve cada categoria uma vez só: Informática, Móveis e Papelaria. Com mais de uma coluna, o `DISTINCT` olha a combinação:

```sql
SELECT DISTINCT cidade, estado FROM clientes;
```

Fortaleza/CE aparece uma vez, mesmo com duas clientes de lá. Para os bancos, todos os `NULL` contam como iguais no `DISTINCT`, então a linha sem cidade aparece uma única vez.

Se você se pegar usando `DISTINCT` para "consertar" linhas duplicadas que surgiram depois de um join, desconfie: muitas vezes o problema está na condição do join, e o `DISTINCT` só esconde o sintoma.

## WHERE: filtrando linhas

O `WHERE` recebe uma condição e mantém só as linhas em que ela é verdadeira.

### Operadores de comparação

| Operador     | Significado                    | Exemplo                 |
| ------------ | ------------------------------ | ----------------------- |
| `=`          | igual                          | `estado = 'CE'`         |
| `<>` ou `!=` | diferente                      | `status <> 'cancelado'` |
| `>` e `<`    | maior e menor                  | `preco > 1000`          |
| `>=` e `<=`  | maior ou igual, menor ou igual | `estoque <= 10`         |

`<>` é a forma do padrão SQL; `!=` funciona nos três SGBDs. Datas e textos também podem ser comparados: `data_pedido >= '2025-03-01'` traz os pedidos de março em diante.

### AND, OR, NOT e a precedência

```sql
SELECT nome, categoria, preco
FROM produtos
WHERE categoria = 'Informática' AND preco < 500;
```

`AND` exige que as duas condições sejam verdadeiras; `OR`, que pelo menos uma seja; `NOT` inverte.

Quando `AND` e `OR` aparecem juntos, o `AND` é avaliado primeiro, como a multiplicação antes da soma na matemática. Veja a diferença:

```sql
-- Sem parênteses
SELECT nome, preco FROM produtos
WHERE categoria = 'Informática' OR categoria = 'Papelaria' AND preco > 100;

-- Com parênteses
SELECT nome, preco FROM produtos
WHERE (categoria = 'Informática' OR categoria = 'Papelaria') AND preco > 100;
```

A primeira consulta é lida pelo banco como `categoria = 'Informática' OR (categoria = 'Papelaria' AND preco > 100)`: traz **todos** os produtos de informática, inclusive o mouse de R$ 89,90, e nenhum de papelaria. A segunda traz notebook, teclado e monitor, porque o filtro de preço vale para as duas categorias. Regra prática: misturou `AND` com `OR`, coloque parênteses, mesmo quando achar que não precisa.

### IN e NOT IN

`IN` testa se o valor está numa lista. É um jeito mais curto de escrever vários `OR`:

```sql
SELECT nome, estado FROM clientes
WHERE estado IN ('CE', 'PE', 'BA');

SELECT id, status FROM pedidos
WHERE status NOT IN ('cancelado', 'pendente');
```

A lista também pode vir de uma subquery, como em `WHERE cliente_id IN (SELECT id FROM clientes WHERE estado = 'CE')`. Subqueries têm nota própria: [Subqueries e operadores de conjunto](/labs/data/sql/10-subqueries-e-operadores-de-conjunto/).

### BETWEEN

`BETWEEN` testa um intervalo **inclusivo**: os dois extremos entram.

```sql
SELECT id, data_pedido FROM pedidos
WHERE data_pedido BETWEEN '2025-02-01' AND '2025-02-28';
-- equivale a data_pedido >= '2025-02-01' AND data_pedido <= '2025-02-28'
```

Cuidado com colunas de data **e hora**: `BETWEEN '2025-02-01' AND '2025-02-28'` numa coluna `TIMESTAMP` para em `2025-02-28 00:00:00` e deixa de fora quase todo o dia 28. Para datas com hora, prefira um intervalo aberto no fim: `>= '2025-02-01' AND < '2025-03-01'`.

### LIKE: buscando padrões em texto

| Curinga | Significa                                           | Exemplo            | Encontra                                      |
| ------- | --------------------------------------------------- | ------------------ | --------------------------------------------- |
| `%`     | qualquer sequência de caracteres, inclusive nenhuma | `nome LIKE 'M%'`   | Mouse sem fio, Monitor 24, Mesa de escritório |
| `_`     | exatamente um caractere                             | `estado LIKE 'C_'` | CE                                            |

```sql
SELECT nome FROM produtos WHERE nome LIKE '%escritório%';  -- contém
SELECT email FROM clientes WHERE email LIKE '%@email.com';  -- termina com
```

Se o `LIKE` diferencia maiúsculas depende do banco:

| MySQL                                  | PostgreSQL                                                                                 | SQL Server                             |
| -------------------------------------- | ------------------------------------------------------------------------------------------ | -------------------------------------- |
| Não diferencia, com a collation padrão | Diferencia; para ignorar, use `ILIKE` (exclusivo do PostgreSQL) ou `LOWER(nome) LIKE 'm%'` | Não diferencia, com a collation padrão |

Um `LIKE` que começa com `%` (`'%escritório'`) obriga o banco a olhar todas as linhas, porque um índice comum não ajuda a buscar pelo fim do texto. Em tabelas pequenas tanto faz; em tabelas com milhões de linhas, pesa. Índices aparecem em [Views, índices e triggers](/labs/data/sql/11-views-indices-e-triggers/).

## NULL: o valor que não é valor

`NULL` representa ausência ou desconhecimento. Ele não é zero nem texto vazio, e isso muda o comportamento das comparações.

### Por que `= NULL` não funciona

O SQL usa uma **lógica de três valores**: uma condição pode ser verdadeira, falsa ou **desconhecida** (UNKNOWN). Qualquer comparação com `NULL` resulta em desconhecido, inclusive `NULL = NULL`. E o `WHERE` só mantém o que é verdadeiro.

```sql
-- Não traz nada, nunca
SELECT nome FROM funcionarios WHERE salario = NULL;

-- Certo
SELECT nome FROM funcionarios WHERE salario IS NULL;      -- Thiago
SELECT nome FROM funcionarios WHERE salario IS NOT NULL;  -- os outros
```

### A armadilha do NOT IN com NULL

Esse é um erro difícil de perceber, porque a consulta roda sem erro e simplesmente volta vazia. Suponha que você queira os funcionários que não são gerentes de ninguém:

```sql
SELECT nome FROM funcionarios
WHERE id NOT IN (SELECT manager_id FROM funcionarios);
```

A subquery devolve `1, 1, 4, 4, 7` e vários `NULL` (de quem não tem gerente). Para cada funcionário, o banco precisa garantir que o `id` é diferente de **todos** os valores da lista, inclusive do `NULL`, e `id <> NULL` é desconhecido. Resultado: nenhuma linha. A correção é tirar os nulos da lista ou usar `NOT EXISTS`:

```sql
SELECT nome FROM funcionarios
WHERE id NOT IN (SELECT manager_id FROM funcionarios WHERE manager_id IS NOT NULL);
```

O mesmo raciocínio explica por que `departamento NOT IN ('TI', 'Vendas')` não traz a Beatriz, que não tem departamento: para ela a condição é desconhecida, não verdadeira.

### COALESCE: trocando NULL por outro valor

`COALESCE` devolve o primeiro argumento que não é `NULL`. Funciona nos três SGBDs e faz parte do padrão SQL.

```sql
SELECT nome,
       COALESCE(salario, 0) AS salario,
       COALESCE(email, 'sem e-mail') AS email
FROM funcionarios;
```

Ele muda só o resultado da consulta, não grava nada na tabela. Outro uso frequente é rotular a venda de balcão, que não tem cliente:

```sql
SELECT id, COALESCE(CAST(cliente_id AS VARCHAR(10)), 'balcão') AS cliente, valor_total
FROM pedidos;
```

O `CAST` está ali porque todos os argumentos do `COALESCE` precisam ter tipos compatíveis: `cliente_id` é número e `'balcão'` é texto. (No MySQL, use `CAST(cliente_id AS CHAR)`.) Também aceita vários argumentos: `COALESCE(celular, telefone_fixo, 'sem contato')`.

Cada SGBD tem ainda uma versão própria de dois argumentos: `IFNULL(salario, 0)` no MySQL e `ISNULL(salario, 0)` no SQL Server. Prefira `COALESCE`, que funciona em todos.

O caminho inverso também existe: `NULLIF(a, b)` devolve `NULL` quando `a = b`. O uso clássico é evitar divisão por zero: `vendas / NULLIF(visitas, 0)`.

## CASE: lógica condicional

O `CASE` é o "se... então..." do SQL. Ele cria valores novos a partir de condições e pode aparecer no `SELECT`, no `WHERE`, no `ORDER BY` e dentro de agregações.

```sql
SELECT nome, preco,
       CASE
           WHEN preco >= 1000 THEN 'alto'
           WHEN preco >= 100  THEN 'médio'
           ELSE 'baixo'
       END AS faixa_preco
FROM produtos;
```

As condições são testadas em ordem e vale a primeira verdadeira. Por isso o notebook (R$ 3.899,90) cai em "alto" e não em "médio", embora também seja maior que 100. Sem `ELSE`, as linhas que não casam com nenhum `WHEN` recebem `NULL`.

Quando todas as condições comparam a mesma coluna com valores fixos, existe a forma simples:

```sql
SELECT id,
       CASE status
           WHEN 'pendente'  THEN 'Aguardando pagamento'
           WHEN 'pago'      THEN 'Em separação'
           WHEN 'enviado'   THEN 'A caminho'
           WHEN 'cancelado' THEN 'Cancelado'
       END AS situacao
FROM pedidos;
```

O `CASE` também resolve classificações de valor, como o porte de cada pedido:

```sql
SELECT id, valor_total,
       CASE WHEN valor_total >= 2000 THEN 'grande' ELSE 'pequeno' END AS porte
FROM pedidos;
```

Combinado com `SUM` ou `COUNT`, o `CASE` permite contagens condicionais ("quantos pedidos pagos e quantos cancelados por cliente"), assunto de [Agregações, GROUP BY e HAVING](/labs/data/sql/08-agregacoes-group-by-e-having/).

## ORDER BY: ordenando o resultado

Sem `ORDER BY`, o banco devolve as linhas na ordem que for mais conveniente para ele, e essa ordem pode mudar de uma execução para outra. Se a ordem importa, peça.

```sql
SELECT nome, categoria, preco
FROM produtos
ORDER BY categoria ASC, preco DESC;
```

`ASC` (crescente) é o padrão; `DESC` inverte. Com várias colunas, a segunda só desempata a primeira: aqui os produtos ficam agrupados por categoria e, dentro de cada uma, do mais caro para o mais barato.

Dá para ordenar por apelido (`ORDER BY valor_em_estoque`) e por expressões (`ORDER BY preco * estoque DESC`).

### Onde ficam os NULL

|                              | MySQL                                       | PostgreSQL                                     | SQL Server                                                              |
| ---------------------------- | ------------------------------------------- | ---------------------------------------------- | ----------------------------------------------------------------------- |
| Em `ASC`, os `NULL` aparecem | Primeiro                                    | Por último                                     | Primeiro                                                                |
| Escolher explicitamente      | Truque: `ORDER BY salario IS NULL, salario` | `ORDER BY salario NULLS FIRST` ou `NULLS LAST` | Truque: `ORDER BY CASE WHEN salario IS NULL THEN 1 ELSE 0 END, salario` |

## Limitando o número de linhas

Para pegar só as primeiras linhas (os 3 produtos mais caros, os 10 últimos pedidos), cada SGBD tem sua sintaxe:

| MySQL                              | PostgreSQL                                                      | SQL Server                                                    |
| ---------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------- |
| `... ORDER BY preco DESC LIMIT 3;` | `... ORDER BY preco DESC LIMIT 3;` ou `FETCH FIRST 3 ROWS ONLY` | `SELECT TOP 3 nome, preco FROM produtos ORDER BY preco DESC;` |

```sql
-- MySQL e PostgreSQL
SELECT nome, preco
FROM produtos
ORDER BY preco DESC
LIMIT 3;
```

`FETCH FIRST n ROWS ONLY` é a forma do padrão SQL. O PostgreSQL aceita as duas; o SQL Server aceita uma variação com `OFFSET` (abaixo); o MySQL só aceita `LIMIT`.

Sem `ORDER BY`, "as 3 primeiras linhas" não significa nada em particular: você recebe 3 linhas quaisquer.

### Paginação com OFFSET

Para mostrar a "página 2" de uma lista com 3 itens por página, pule as 3 primeiras linhas:

| MySQL e PostgreSQL                | SQL Server (e PostgreSQL)                             |
| --------------------------------- | ----------------------------------------------------- |
| `ORDER BY nome LIMIT 3 OFFSET 3;` | `ORDER BY nome OFFSET 3 ROWS FETCH NEXT 3 ROWS ONLY;` |

No SQL Server, `OFFSET ... FETCH` exige `ORDER BY`.

### O maior salário (e o problema dos empates)

"Encontre o funcionário com o maior salário" é pergunta clássica de entrevista. A resposta com `LIMIT`/`TOP` funciona, mas tem uma pegadinha:

```sql
-- MySQL e PostgreSQL (o NULLS LAST é só do PostgreSQL)
SELECT nome, salario FROM funcionarios
ORDER BY salario DESC NULLS LAST
LIMIT 1;
```

O `NULLS LAST` está ali porque, no PostgreSQL, `NULL` conta como maior que tudo e o Thiago (sem salário) apareceria no topo de um `ORDER BY salario DESC`. No MySQL e no SQL Server, os `NULL` já vão para o fim em `DESC`.

Se dois funcionários empatarem no maior salário, `LIMIT 1` devolve só um deles, escolhido sem critério. Para trazer todos os empatados:

```sql
-- Funciona nos três SGBDs
SELECT nome, salario FROM funcionarios
WHERE salario = (SELECT MAX(salario) FROM funcionarios);
```

O SQL Server também tem `SELECT TOP 1 WITH TIES ... ORDER BY salario DESC`, e o PostgreSQL 13+ tem `FETCH FIRST 1 ROW WITH TIES`. A versão com `MAX` usa uma subquery (veja [Subqueries e operadores de conjunto](/labs/data/sql/10-subqueries-e-operadores-de-conjunto/)); as variações como "segundo maior salário" estão em [Entrevista de SQL](/labs/data/pratica/03-entrevista-de-sql/).

## Referências

- [SELECT (Transact-SQL)](https://learn.microsoft.com/pt-br/sql/t-sql/queries/select-transact-sql) - Microsoft Learn, pt-BR
- [LIKE (Transact-SQL)](https://learn.microsoft.com/pt-br/sql/t-sql/language-elements/like-transact-sql) - Microsoft Learn, pt-BR
- [COALESCE (Transact-SQL)](https://learn.microsoft.com/pt-br/sql/t-sql/language-elements/coalesce-transact-sql) - Microsoft Learn, pt-BR
- [LIMIT e OFFSET (documentação do PostgreSQL)](https://halleyoliv.gitlab.io/pgdocptbr/queries-limit.html) - tradução de Halley Pacheco de Oliveira da documentação oficial, pt-BR
- [Operator Precedence](https://dev.mysql.com/doc/refman/8.4/en/operator-precedence.html) - Oracle/MySQL, en
