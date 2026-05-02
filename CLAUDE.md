# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Sobre o lab

Data Labs é o laboratório de ciência e engenharia de dados da Caramelo Tech. O conteúdo cobre SQL, Python (pandas, numpy), pipelines ETL e estatística aplicada. Público-alvo: iniciantes a intermediários.

## Comandos

```bash
npm install
npm run dev      # servidor em localhost:4321
npm run build    # build de produção
npm run preview  # preview do build
```

## Arquitetura

- `src/content/docs/` - anotações publicadas no site via Starlight
- `src/content/docs/fundamentos/` - notas de introdução e conceitos fundamentais
- `examples/` - scripts, queries e projetos práticos (não publicados no site)
- `astro.config.mjs` - configuração do Astro/Starlight, incluindo sidebar e `base: '/data-labs'`
- `src/styles/custom.css` - customizações visuais do tema

## Deployment

O site é publicado via GitHub Actions em `https://caramelotech.com.br/data-labs/`. O `base` em `astro.config.mjs` deve permanecer `/data-labs` para que os links funcionem corretamente no ambiente de produção.

## Convenções de conteúdo

- Idioma: português (pt-BR)
- Frontmatter obrigatório:
  ```yaml
  ---
  title: "Título da nota"
  description: "Descrição breve"
  lastUpdated: 2026-01-01
  sidebar:
    order: 1
  tags: ["sql", "pandas"]
  ---
  ```
- Não repita o `title` como `# h1` - o Starlight renderiza automaticamente
- Use `##` e `###` para seções
- Inclua o "por quê", não apenas o "como"

## Regra de sidebar.order

**`sidebar.order` é sequencial por diretório**, não global. A ordem entre seções é controlada pelo array `sidebar` em `astro.config.mjs`. Dentro de cada pasta, numere os arquivos a partir de 1.

Para adicionar uma nova seção superior (ex: `sql/`):
1. Crie o diretório em `src/content/docs/sql/`
2. Adicione um arquivo `index.md` como página de entrada
3. Adicione uma entrada `autogenerate` em `astro.config.mjs`:
   ```javascript
   {
     label: "SQL",
     autogenerate: { directory: "sql" },
   }
   ```
