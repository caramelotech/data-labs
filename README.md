# Data Labs

Bem-vindo ao **Data Labs**, a trilha aberta do Caramelo Tech sobre **dados**.

Este repositório existe para ajudar pessoas curiosas a aprender, construir e compartilhar conhecimento em comunidade. A ideia é estudar com calma, praticar com exemplos reais e evoluir junto com outras pessoas que também gostam de tecnologia.

As notas deste repositório são publicadas no site do [Caramelo Labs](https://caramelotech.com.br/labs/data/).

## O que você vai encontrar

- Conteúdo didático em português, pensado para estudo progressivo
- Notas em Markdown publicadas no hub do Caramelo Labs
- Exemplos de código e projetos implementados em `examples/`
- Exercícios e ideias de projetos em `notes/pratica/`
- Espaço aberto para contribuições da comunidade

## Conteúdo

| Seção            | Escopo                                                                       |
| ---------------- | ---------------------------------------------------------------------------- |
| Fundamentos      | Introdução, conceitos básicos e tópicos avançados                            |
| SQL              | Linguagem SQL do zero: estrutura, consultas, joins e transações              |
| Power BI         | Business intelligence com Power BI: Power Query, modelagem e DAX             |
| Projetos         | Ideias de projetos práticos para portfólio                                   |
| Prática          | Exercícios, projetos e preparação para entrevistas                           |

## Estrutura do repositório

```text
data-labs/
├── notes/           -> Notas em Markdown puro publicadas no Caramelo Labs
│   └── pratica/     -> Exercícios e projetos propostos
├── examples/        -> Exemplos de código e projetos implementados de dados
├── sidebar.json     -> Ordem das seções no hub
├── .github/         -> Templates e guias de contribuição
└── LICENSE
```

Este repositório contém conteúdo e exemplos. A estrutura web que publica os labs vive no repositório hub [labs](https://github.com/caramelotech/labs), que busca as notas daqui e monta o site.

## Como estudar

1. Comece pelo [site do lab](https://caramelotech.com.br/labs/data/) ou pelas notas em `notes/`
2. Siga a ordem sugerida em `sidebar.json`
3. Use `examples/` para ver implementações prontas
4. Pratique com os [exercícios](notes/pratica/01-exercicios.md)
5. Aplique os aprendizados nos [projetos](notes/pratica/02-projetos.md)

## Escrevendo notas

As notas em `notes/` são Markdown puro, sem frontmatter:

- A primeira linha da nota deve ser o título: `# Título da Nota`
- Use prefixo numérico no nome do arquivo para controlar a ordem: `01-introducao.md`, `02-conceitos.md`
- Agrupe conteúdos por tema em subpastas
- Imagens ficam junto das notas e usam caminho relativo
- Links internos publicados no hub usam o caminho completo: `/labs/data/<secao>/<arquivo-com-prefixo>/`

Ao criar uma nova subpasta de tema, adicione a seção correspondente em `sidebar.json`.
