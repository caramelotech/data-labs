# Exercícios

Pratique o que aprendeu nas anotações e exemplos.

## Como usar

1. Leia o enunciado do exercício
2. Tente resolver por conta própria
3. Consulte as notas se precisar de ajuda
4. Compare sua solução com a dos colegas

## Exercício 01 - Exploração de Dataset

**Objetivo:** Carregar e explorar um dataset com pandas.

**Instrução:**
Carregue um arquivo CSV de sua escolha e responda:

1. Quantas linhas e colunas tem o dataset?
2. Quais colunas possuem valores nulos?
3. Quais são os tipos de dados de cada coluna?

**Critérios de sucesso:**

- [ ] O dataset é carregado sem erros
- [ ] `df.shape`, `df.info()` e `df.isnull().sum()` são usados corretamente
- [ ] Os resultados são interpretados e descritos

## Exercício 02 - Filtros e Agregações com SQL

**Objetivo:** Praticar SELECT, WHERE, GROUP BY e ORDER BY.

**Instrução:**
Dado uma tabela `vendas` com as colunas `produto`, `categoria`, `valor` e `data`:

1. Liste os 5 produtos com maior valor total vendido
2. Calcule o total vendido por categoria
3. Filtre apenas as vendas do último mês

**Critérios de sucesso:**

- [ ] As queries retornam os resultados corretos
- [ ] GROUP BY e ORDER BY são usados corretamente
- [ ] A filtragem por data funciona

## Exercício 03 - Limpeza de Dados

**Objetivo:** Identificar e tratar problemas comuns em um dataset.

**Instrução:**
Dado um DataFrame com dados "sujos":

1. Remova linhas completamente duplicadas
2. Preencha valores nulos em colunas numéricas com a mediana
3. Normalize a coluna de texto (remova espaços, converta para minúsculas)

**Critérios de sucesso:**

- [ ] Duplicatas são removidas com `drop_duplicates()`
- [ ] Nulos são tratados com `fillna()`
- [ ] A coluna de texto é normalizada com `str.strip()` e `str.lower()`
