# Projeto 01 — Stack Overflow Developer Survey: Perfil e Tendências da Comunidade de Desenvolvedores

## Objetivo

Utilizar a base de dados da Stack Overflow Developer Survey para realizar análises estatísticas e responder a perguntas que vão além do artigo base de referência: [2024 Developer Survey](https://stackoverflow.blog/2025/01/01/developers-want-more-more-more-the-2024-results-from-stack-overflow-s-annual-developer-survey/).


O entregável é um Jupyter Notebook executável contendo os resultados das análises e as discussões associadas a cada uma.

## Dataset

- **Fonte:** [Stack Overflow Developer Survey](https://survey.stackoverflow.co/)
- **Anos disponíveis:** 2011–2024 (formato CSV)
- **Recomendado:** utilizar o ano mais recente disponível; anos anteriores podem ser incluídos para análises de tendência



## Perguntas de Análise

| # | Pergunta | Tipo |
| --- | ---------- | ------ |
| 1 | Qual é a distribuição de salários entre os desenvolvedores? | Distribuição |
| 2 | Quais são as linguagens de programação mais populares? | Ranking |
| 3 | Existe correlação entre anos de experiência e salário? | Correlação |
| 4 | Quais são as tendências de adoção de tecnologias ao longo do tempo? | Série temporal |
| 5 | Quais são as diferenças de perfil entre desenvolvedores de diferentes regiões? | Comparação |
| 6 | Quais são as principais motivações para escolha de linguagem? | Categórica |
| 7 | Quais são as principais barreiras na carreira dos desenvolvedores? | Categórica |

## Estrutura do Projeto

```text
01-stackoverflow-survey/
  README.md          ← este arquivo
  analysis.ipynb     ← notebook principal (entregável)
  data/              ← dataset local (não versionado)
```

## Requisitos

- [ ] Notebook executável do início ao fim sem erros
- [ ] Cada análise acompanhada de discussão/interpretação
- [ ] Visualizações claras e com títulos/rótulos adequados
- [ ] Outros conjuntos de dados podem ser incluídos se necessário

## Dica

Comece pela exploração. Só transforme os dados depois de entender o que tem.
