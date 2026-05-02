---
title: "Avançando"
description: "Joins, agregações avançadas, limpeza de dados, pipelines ETL e boas práticas para trabalhar com dados em produção."
lastUpdated: 2026-04-14
sidebar:
  order: 3
tags: ["joins", "etl", "limpeza", "boas-práticas"]
---

## Indo além do básico

Com os fundamentos dominados, é hora de avançar.
Este arquivo cobre padrões e práticas para trabalhar com dados de forma mais robusta.

## Tópicos

### Joins e Relacionamentos

Combinar dados de múltiplas tabelas é essencial no dia a dia.

```sql
-- Pedidos com dados do cliente
SELECT p.id, c.nome, p.valor
FROM pedidos p
JOIN clientes c ON p.cliente_id = c.id;

-- LEFT JOIN para incluir registros sem correspondência
SELECT c.nome, COUNT(p.id) AS total_pedidos
FROM clientes c
LEFT JOIN pedidos p ON c.id = p.cliente_id
GROUP BY c.nome;
```

### Limpeza de Dados

Dados reais são sujos. Tratar isso é parte fundamental do trabalho.

```python
# Verificar valores nulos
df.isnull().sum()

# Preencher ou remover
df['coluna'].fillna(0)
df.dropna(subset=['coluna_critica'])

# Remover duplicatas
df.drop_duplicates()

# Normalizar texto
df['nome'] = df['nome'].str.strip().str.lower()
```

### Pipelines ETL

Estruture o fluxo de dados de forma reproduzível.

- **Extract** - leia os dados da fonte (CSV, banco, API)
- **Transform** - limpe, filtre e enriqueça
- **Load** - salve no destino (banco, arquivo, dashboard)

### Boas Práticas

- Sempre explore os dados antes de transformar (`head()`, `describe()`, `info()`)
- Documente as transformações aplicadas
- Versione os datasets e os scripts juntos
- Prefira operações vetorizadas a loops em pandas
- Teste seus pipelines com amostras pequenas antes de rodar no dataset completo

## Próximo passo

Aplique esses conceitos nos projetos em `/examples/projects.md`.
É construindo que o aprendizado se consolida.
