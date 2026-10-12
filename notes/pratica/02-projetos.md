# Projetos

Mini projetos para aplicar o que foi aprendido.

## Como usar

1. Leia o enunciado do projeto
2. Planeje antes de codificar
3. Implemente incrementalmente
4. Teste cada parte antes de avançar

## Projeto 01 - Análise de Vendas

**Objetivo:** Analisar um dataset de vendas e extrair insights.

**Descrição:**
Dado um CSV com colunas `data`, `produto`, `categoria`, `quantidade` e `valor_unitario`, construa uma análise completa.

**Requisitos:**

- [ ] Carregar e explorar o dataset (shape, tipos, nulos)
- [ ] Criar a coluna `valor_total = quantidade * valor_unitario`
- [ ] Calcular o faturamento total por mês
- [ ] Identificar o produto mais vendido por categoria
- [ ] Gerar um gráfico de faturamento mensal

**Desafio extra:**

- Identificar meses com queda de vendas em relação ao mês anterior
- Calcular o ticket médio por categoria

**Dica:**
Comece pela exploração. Só transforme os dados depois de entender o que tem.

## Projeto 02 - Pipeline ETL Simples

**Objetivo:** Construir um pipeline que extrai, transforma e carrega dados.

**Descrição:**
Crie um script Python que lê dados de uma fonte (CSV ou API pública), aplica transformações e salva o resultado processado.

**Requisitos:**

- [ ] Extrair dados de um arquivo CSV ou endpoint público
- [ ] Remover duplicatas e tratar valores nulos
- [ ] Adicionar colunas derivadas (ex: mês a partir de uma data)
- [ ] Salvar o resultado em um novo CSV limpo

**Desafio extra:**

- Adicionar logs de execução com o número de linhas em cada etapa
- Criar uma função para cada etapa (extract, transform, load)

**Dica:**
Estruture o código em funções desde o início. Pipelines viram um emaranhado rápido sem organização.
