# Guia de Contribuição

Obrigado por querer contribuir com este repositório da Caramelo Tech!

## O que pode ser contribuído

- Novas anotações em `src/content/docs/`
- Novos exemplos em `examples/`
- Exercícios adicionais em `examples/exercises.md`
- Projetos práticos em `examples/projects.md`
- Melhorias na configuração do site (Astro/Starlight)

## Processo

1. Crie uma branch a partir de `main` seguindo o padrão:

   ```
   feature/descricao-curta
   fix/descricao-curta
   docs/descricao-curta
   ```

2. Faça commits atômicos com mensagens no padrão de Conventional Commits:

   ```
   feat: adicionar notas sobre loops
   fix: corrigir exemplo de recursão
   docs: melhorar anotação sobre funções
   ```

   Tipos válidos: `feat`, `fix`, `docs`, `style`, `refactor`, `chore`

3. Abra um Pull Request usando o template disponível e aguarde revisão.

4. Após aprovação, o merge será feito por um mantenedor.

## Padrões de conteúdo

### Anotações (`src/content/docs/`)

Cada arquivo `.md` deve ter o seguinte frontmatter:

```yaml
---
title: "Título da nota"
description: "Descrição breve exibida no site e no SEO"
lastUpdated: 2026-01-01
sidebar:
  order: 1 # controla a ordem no sidebar
tags: ["tag1", "tag2"]
---
```

Outras diretrizes:

- Escreva em português
- Use títulos hierárquicos (`##`, `###`) - não repita o `title` como `h1`
- Prefira exemplos curtos e diretos
- Inclua o "por quê", não apenas o "como"
- Para agrupar por tema, use subpastas dentro de `src/content/docs/`

### Exemplos de código (`examples/`)

- Um conceito por arquivo
- Nomeie o arquivo de forma descritiva (`loop-for.js`, não `exemplo1.js`)
- Inclua um comentário no topo explicando o que o exemplo demonstra

### Exercícios (`examples/exercises.md`)

- Descreva claramente o objetivo
- Indique o nível de dificuldade (iniciante / intermediário / avançado)
- Inclua exemplos de entrada e saída esperada quando aplicável

## Rodando o site localmente

```bash
npm install
npm run dev   # localhost:4321
```

## Dúvidas?

Abra uma issue com a tag `question`.
