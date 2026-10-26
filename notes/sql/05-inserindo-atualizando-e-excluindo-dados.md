# Inserindo, atualizando e excluindo dados

## INSERT: gravando linhas

Com as tabelas criadas (o esquema de exemplo está em [Constraints, chaves e relacionamentos](/labs/data/sql/03-constraints-chaves-e-relacionamentos/)), é hora de colocar dados nelas. Inserir, atualizar e excluir são comandos de DML: mexem no conteúdo, não na estrutura.

A forma básica do `INSERT`:

```sql
INSERT INTO clientes (id, nome, email, cidade, estado, data_cadastro)
VALUES (1, 'Ana Souza', 'ana.souza@email.com', 'Fortaleza', 'CE', '2024-01-15');
```

A lista de colunas depois do nome da tabela diz em que ordem os valores vêm. Ela é opcional (`INSERT INTO clientes VALUES (...)`), mas sempre a escreva: sem ela, o `INSERT` depende da ordem física das colunas e quebra no dia em que alguém adicionar uma coluna nova.

Textos e datas vão entre aspas simples; números, sem aspas. Se o texto tiver um apóstrofo, duplique-o: `'Pingo d''Água'`.

Se for acompanhar no seu banco, não precisa rodar os `INSERT` avulsos desta parte: as linhas da Ana e do Felipe já fazem parte do script de dados de exemplo, mais abaixo, e rodar as duas coisas daria erro de chave duplicada.

### Valores ausentes: NULL e DEFAULT

Quando você não tem um valor, há duas saídas:

```sql
-- Omitir a coluna: ela recebe o DEFAULT ou, sem default, NULL
INSERT INTO produtos (id, nome, categoria, preco)
VALUES (8, 'Marca-texto', 'Papelaria', 6.50);   -- estoque recebe o DEFAULT 0 (linha só ilustrativa)

-- Informar NULL explicitamente
INSERT INTO clientes (id, nome, email, cidade, estado, data_cadastro)
VALUES (6, 'Felipe Araújo', 'felipe.araujo@email.com', NULL, NULL, '2025-01-20');
```

Lembre que `NULL` explícito **não** aciona o `DEFAULT`: se você escrever `NULL` na coluna `estoque`, o banco tenta gravar `NULL` e, como ela é `NOT NULL`, dá erro.

### Várias linhas de uma vez

Um único `INSERT` pode levar várias linhas, separadas por vírgula. É mais rápido do que mandar uma por uma e funciona nos três SGBDs (no SQL Server, até 1000 linhas por `VALUES`).

Este é o script com os dados de exemplo usados nas notas de SQL. Rode depois do script de criação de tabelas:

```sql
INSERT INTO funcionarios (id, nome, email, departamento, manager_id, salario, data_admissao) VALUES
    (1, 'Marina Costa',    'marina@loja.com',   'TI',         NULL, 12000.00, '2019-03-01'),
    (4, 'Pedro Alves',     'pedro@loja.com',    'Vendas',     NULL,  9000.00, '2018-11-20'),
    (7, 'Fernanda Lima',   'fernanda@loja.com', 'Financeiro', NULL, 10500.00, '2020-05-04'),
    (2, 'Rafael Nunes',    'rafael@loja.com',   'TI',         1,     8500.00, '2021-06-15'),
    (3, 'Juliana Rocha',   'juliana@loja.com',  'TI',         1,     7800.00, '2022-01-10'),
    (5, 'Lucas Martins',   'lucas@loja.com',    'Vendas',     4,     4500.00, '2023-02-01'),
    (6, 'Camila Ferreira', 'camila@loja.com',   'Vendas',     4,     4800.00, '2023-08-14'),
    (8, 'Thiago Ribeiro',  NULL,                'Financeiro', 7,     NULL,    '2025-09-01'),
    (9, 'Beatriz Gomes',   'beatriz@loja.com',  NULL,         NULL,  3900.00, '2024-04-22');

INSERT INTO clientes (id, nome, email, cidade, estado, data_cadastro) VALUES
    (1, 'Ana Souza',     'ana.souza@email.com',     'Fortaleza',      'CE', '2024-01-15'),
    (2, 'Bruno Lima',    'bruno.lima@email.com',    'São Paulo',      'SP', '2024-02-03'),
    (3, 'Carla Dias',    'carla.dias@email.com',    'Recife',         'PE', '2024-03-22'),
    (4, 'Diego Santos',  'diego.santos@email.com',  'Fortaleza',      'CE', '2024-05-10'),
    (5, 'Elisa Moura',   'elisa.moura@email.com',   'Rio de Janeiro', 'RJ', '2024-07-01'),
    (6, 'Felipe Araújo', 'felipe.araujo@email.com', NULL,             NULL, '2025-01-20');

INSERT INTO produtos (id, nome, categoria, preco, estoque) VALUES
    (1, 'Notebook 14',           'Informática', 3899.90,  12),
    (2, 'Mouse sem fio',         'Informática',   89.90, 150),
    (3, 'Teclado mecânico',      'Informática',  349.00,  40),
    (4, 'Monitor 24',            'Informática', 1099.00,   0),
    (5, 'Cadeira ergonômica',    'Móveis',      1499.00,   8),
    (6, 'Mesa de escritório',    'Móveis',       799.00,  15),
    (7, 'Caderno universitário', 'Papelaria',     24.90, 300);

INSERT INTO pedidos (id, cliente_id, data_pedido, status, valor_total) VALUES
    (1, 1,    '2025-01-10', 'enviado',   3989.80),
    (2, 2,    '2025-01-18', 'pago',       698.00),
    (3, 1,    '2025-02-05', 'enviado',    249.00),
    (4, 3,    '2025-02-20', 'cancelado', 1499.00),
    (5, 4,    '2025-03-02', 'pago',       978.80),
    (6, 2,    '2025-03-15', 'pendente',  3799.90),
    (7, 5,    '2025-04-01', 'enviado',   2198.00),
    (8, NULL, '2025-04-05', 'pago',        49.80);

INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES
    (1, 1,  1, 3899.90),
    (1, 2,  1,   89.90),
    (2, 3,  2,  349.00),
    (3, 7, 10,   24.90),
    (4, 5,  1, 1499.00),
    (5, 2,  2,   89.90),
    (5, 6,  1,  799.00),
    (6, 1,  1, 3799.90),
    (7, 4,  2, 1099.00),
    (8, 7,  2,   24.90);
```

Alguns detalhes desses dados foram colocados de propósito, para os exemplos das próximas notas: o funcionário Thiago ainda não tem salário nem e-mail definidos (`NULL`), a Beatriz não tem departamento, o cliente Felipe não fez nenhum pedido, o pedido 8 foi uma venda de balcão sem cliente (`cliente_id` nulo) e o pedido 6 teve desconto no notebook (o `preco_unitario` difere do preço atual do produto). O `valor_total` de cada pedido bate com a soma dos seus itens.

Repare também na ordem dos funcionários: os gerentes (1, 4 e 7) entram antes de quem aponta para eles em `manager_id`.

### A chave estrangeira protege o relacionamento

Tente inserir um pedido para um cliente que não existe:

```sql
INSERT INTO pedidos (id, cliente_id, data_pedido, status)
VALUES (9, 99, '2025-04-10', 'pendente');
```

O banco recusa com um erro de violação de chave estrangeira, porque não há cliente 99. É a integridade referencial em ação. Da mesma forma, inserir um `id` que já existe gera erro de chave primária duplicada.

### INSERT ... SELECT: copiando dados de uma consulta

Em vez de `VALUES`, o `INSERT` pode receber o resultado de um `SELECT`. Útil para arquivar dados, montar tabelas de apoio ou copiar entre tabelas.

```sql
CREATE TABLE pedidos_arquivo (
    id          INT PRIMARY KEY,
    cliente_id  INT,
    data_pedido DATE,
    status      VARCHAR(20)
);

INSERT INTO pedidos_arquivo (id, cliente_id, data_pedido, status)
SELECT id, cliente_id, data_pedido, status
FROM pedidos
WHERE status = 'cancelado';
```

As colunas do `SELECT` precisam bater em quantidade, ordem e tipo com a lista do `INSERT`. Os detalhes do `SELECT` estão em [Consultas com SELECT](/labs/data/sql/06-consultas-com-select/).

### Inserir ou atualizar (upsert)

Às vezes você quer "insira se não existe; se já existe, atualize". Esse padrão tem o apelido de _upsert_ e cada SGBD tem sua sintaxe:

```sql
-- MySQL 8.0.19+
INSERT INTO produtos (id, nome, categoria, preco, estoque)
VALUES (2, 'Mouse sem fio', 'Informática', 89.90, 200) AS novo
ON DUPLICATE KEY UPDATE estoque = novo.estoque;

-- PostgreSQL
INSERT INTO produtos (id, nome, categoria, preco, estoque)
VALUES (2, 'Mouse sem fio', 'Informática', 89.90, 200)
ON CONFLICT (id) DO UPDATE SET estoque = EXCLUDED.estoque;

-- SQL Server (o PostgreSQL 15+ também tem MERGE)
MERGE produtos AS destino
USING (VALUES (2, 'Mouse sem fio', 'Informática', 89.90, 200))
      AS origem (id, nome, categoria, preco, estoque)
ON destino.id = origem.id
WHEN MATCHED THEN
    UPDATE SET estoque = origem.estoque
WHEN NOT MATCHED THEN
    INSERT (id, nome, categoria, preco, estoque)
    VALUES (origem.id, origem.nome, origem.categoria, origem.preco, origem.estoque);
```

### Recuperando o ID gerado

Quando o `id` é gerado pelo banco (`AUTO_INCREMENT`, `IDENTITY`), a aplicação geralmente precisa saber qual número saiu:

| MySQL                                              | PostgreSQL                 | SQL Server                                    |
| -------------------------------------------------- | -------------------------- | --------------------------------------------- |
| `SELECT LAST_INSERT_ID();` logo depois do `INSERT` | `INSERT ... RETURNING id;` | `INSERT ... OUTPUT inserted.id VALUES (...);` |

## UPDATE: alterando linhas

```sql
UPDATE produtos
SET estoque = 20
WHERE id = 4;
```

Leia como "na tabela `produtos`, coloque 20 em `estoque` nas linhas em que `id` é 4". Dá para alterar várias colunas e usar o valor atual no cálculo:

```sql
-- Aumento de 10% para quem é do departamento de TI
UPDATE funcionarios
SET salario = salario * 1.10
WHERE departamento = 'TI';

-- Várias colunas de uma vez
UPDATE clientes
SET cidade = 'Caucaia', estado = 'CE'
WHERE id = 4;
```

No aumento, funcionários com salário `NULL` continuam com `NULL`, porque qualquer conta com `NULL` dá `NULL`. Se a regra de negócio dissesse "quem não tem salário ganha o piso", você precisaria tratar isso com `COALESCE` (veja [Consultas com SELECT](/labs/data/sql/06-consultas-com-select/)).

O `WHERE` do `UPDATE` aceita tudo que o `WHERE` do `SELECT` aceita, inclusive subqueries: `WHERE id IN (SELECT manager_id FROM funcionarios)` dá aumento só para quem é gerente. Subqueries têm nota própria: [Subqueries e operadores de conjunto](/labs/data/sql/10-subqueries-e-operadores-de-conjunto/).

## DELETE: excluindo linhas

```sql
DELETE FROM pedidos
WHERE status = 'cancelado';
```

Como `itens_pedido` foi criada com `ON DELETE CASCADE`, os itens do pedido cancelado são apagados junto. Já tentar apagar um cliente que tem pedidos falha, porque a chave estrangeira de `pedidos` não tem cascata:

```sql
DELETE FROM clientes WHERE id = 1;   -- erro: o cliente 1 tem pedidos
DELETE FROM clientes WHERE id = 6;   -- funciona: o Felipe não tem pedidos
```

Para esvaziar uma tabela inteira ou removê-la, compare `DELETE` com `TRUNCATE` e `DROP` em [Alterando a estrutura](/labs/data/sql/04-alterando-a-estrutura/).

### Soft delete: marcar em vez de apagar

Muitos sistemas não apagam registros de verdade. Em vez disso, adicionam uma coluna como `excluido_em` e fazem um `UPDATE` preenchendo a data. As consultas passam a filtrar `WHERE excluido_em IS NULL`. Dá mais trabalho, mas permite desfazer exclusões e mantém o histórico para auditoria.

## O perigo do UPDATE e do DELETE sem WHERE ⚠️

Sem `WHERE`, `UPDATE` e `DELETE` afetam **todas as linhas da tabela**:

```sql
UPDATE produtos SET preco = 0;   -- todos os produtos passam a custar zero
DELETE FROM clientes;            -- todos os clientes somem (ou dá erro de FK, se tiver sorte)
```

Não existe "Ctrl+Z" depois que a alteração é confirmada. Alguns hábitos que evitam o desastre:

1. **Escreva o `SELECT` antes.** Rode `SELECT * FROM produtos WHERE id = 4;`, confira se vieram só as linhas certas e só então troque `SELECT *` por `UPDATE ... SET` ou `DELETE`, mantendo o mesmo `WHERE`.
2. **Filtre pela chave primária** sempre que estiver mexendo em linhas específicas.
3. **Use uma transação como rede de segurança.** Abra a transação, rode o comando, confira o resultado e só então confirme:

```sql
START TRANSACTION;          -- PostgreSQL: BEGIN;  SQL Server: BEGIN TRANSACTION;

UPDATE funcionarios
SET salario = salario * 1.10
WHERE departamento = 'TI';

SELECT nome, salario FROM funcionarios WHERE departamento = 'TI';

-- Ficou certo?  COMMIT;
-- Deu errado?   ROLLBACK;
```

Enquanto não houver `COMMIT`, o `ROLLBACK` desfaz tudo. Depois do `COMMIT`, só um backup salva. Como as transações funcionam está em [Transações e ACID](/labs/data/sql/13-transacoes-e-acid/).

### Safe updates no MySQL Workbench

O MySQL Workbench vem com o modo **Safe Updates** ligado. Nele, `UPDATE` e `DELETE` sem `WHERE` usando uma coluna de chave (e sem `LIMIT`) são bloqueados com o erro 1175. É chato quando você realmente quer alterar tudo, mas já salvou muita gente. Se precisar desligar só na sessão atual:

```sql
SET SQL_SAFE_UPDATES = 0;
-- comando que precisava
SET SQL_SAFE_UPDATES = 1;
```

A opção permanente fica em Edit > Preferences > SQL Editor.

## Referências

- [INSERT (Transact-SQL)](https://learn.microsoft.com/pt-br/sql/t-sql/statements/insert-transact-sql) - Microsoft Learn, pt-BR
- [Manipulação de dados (documentação do PostgreSQL)](https://halleyoliv.gitlab.io/pgdocptbr/dml.html) - tradução de Halley Pacheco de Oliveira da documentação oficial, pt-BR
- [INSERT ... ON DUPLICATE KEY UPDATE Statement](https://dev.mysql.com/doc/refman/8.4/en/insert-on-duplicate.html) - Oracle/MySQL, en
- [Data Manipulation](https://www.postgresql.org/docs/current/dml.html) - PostgreSQL Global Development Group, en
