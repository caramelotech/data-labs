# Caramelo Labs

Laboratório prático da **Caramelo Tech** com foco em aprendizado hands-on através de exemplos, exercícios e projetos.

## O que você vai encontrar

- Anotações em Markdown
- Exemplos de código
- Exercícios práticos
- Mini projetos

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

Acesse: https://caramelotech.github.io/caramelo-labs

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
tags: ["tag1", "tag2"]
---
```

Subpastas são suportadas - use-as para agrupar notas por tema:

```
src/content/docs/
  javascript/
    01-variaveis.md
    02-funcoes.md
  python/
    01-introducao.md
```

## Sobre a Caramelo Tech

A Caramelo Tech é uma iniciativa focada em aprendizado prático de tecnologia.

Aqui você não apenas lê - você constrói.

## Licença

MIT
