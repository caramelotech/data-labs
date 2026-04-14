# Data Labs

Laboratório prático de dados da **Caramelo Tech** com foco em análise de dados, SQL, Python e engenharia de dados.

## O que você vai encontrar

- Anotações sobre SQL, pandas, ETL e estatística aplicada
- Exemplos de queries e scripts prontos para executar
- Exercícios práticos com dados reais
- Mini projetos de análise e pipelines de dados

## Estrutura do repositório

```
src/content/docs/   → Anotações e estudos (publicadas no site)
examples/           → Exemplos de código, exercícios e projetos práticos
```

## Como usar

1. Comece pelas anotações em `src/content/docs/`
2. Explore os exemplos em `examples/`
3. Resolva os exercícios em `examples/exercises.md`
4. Construa os projetos em `examples/projects.md`

## Visualização

As anotações são publicadas via GitHub Pages com o tema Starlight (Astro).

Acesse: https://caramelotech.github.io/data-labs

## Rodando localmente

```bash
npm install
npm run dev     # servidor em localhost:4321
npm run build   # build de produção
npm run preview # preview do build
```

## Adicionando notas

Crie um arquivo `.md` em `src/content/docs/` com o seguinte frontmatter:

```yaml
---
title: "Título da nota"
description: "Descrição breve"
lastUpdated: 2026-01-01
sidebar:
  order: 4
tags: ["sql", "pandas"]
---
```

Subpastas são suportadas - use-as para agrupar notas por tema:

```
src/content/docs/
  sql/
    01-select.md
    02-joins.md
  python/
    01-pandas.md
    02-visualizacao.md
```

## Sobre a Caramelo Tech

A Caramelo Tech é uma iniciativa focada em aprendizado prático de tecnologia.

Aqui você não apenas lê - você constrói.

## Licença

MIT
