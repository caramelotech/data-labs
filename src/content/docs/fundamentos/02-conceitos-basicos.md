---
title: "Conceitos Básicos"
description: "Tipos de dados, estruturas fundamentais, SQL básico e manipulação com pandas - os blocos essenciais para trabalhar com dados."
lastUpdated: 2026-04-14
sidebar:
  order: 2
tags: ["fundamentos", "sql", "pandas", "tipos-de-dados"]
---

## Fundamentos

Antes de avançar, é importante dominar os conceitos básicos de dados.
Aqui estão os blocos de construção essenciais.

## Conceitos principais

### Tipos de Dados

Dados existem em diferentes formatos e cada um tem características próprias.

- **Numérico** - inteiros e decimais (idades, preços, contagens)
- **Texto** - strings (nomes, categorias, descrições)
- **Data/Tempo** - timestamps (datas de transação, eventos)
- **Booleano** - verdadeiro/falso (flags, indicadores)

### Estruturas de Dados Fundamentais

As principais formas de organizar dados:

- **Tabela / DataFrame** - dados em linhas e colunas (o formato mais comum)
- **Série / Coluna** - sequência de valores de um mesmo tipo
- **Chave-Valor** - pares associativos, como dicionários Python

### SQL Básico

Linguagem padrão para consultar bancos de dados relacionais.

```sql
-- Selecionar dados
SELECT nome, idade
FROM clientes
WHERE idade > 18
ORDER BY nome;

-- Agregar
SELECT cidade, COUNT(*) AS total
FROM clientes
GROUP BY cidade;
```

### Manipulação com Pandas

A principal biblioteca Python para análise de dados.

```python
import pandas as pd

df = pd.read_csv('dados.csv')

# Explorar
df.head()
df.info()
df.describe()

# Filtrar
adultos = df[df['idade'] > 18]

# Agrupar
df.groupby('cidade')['valor'].sum()
```

## Próximo passo

Veja os exemplos em `/examples` para ver esses conceitos na prática. Depois, pratique com os exercícios em `/examples/exercises.md`.
