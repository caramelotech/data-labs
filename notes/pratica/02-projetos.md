# Projetos

Mini projetos para aplicar o que foi aprendido.

## Como usar

1. Leia o enunciado do projeto
2. Planeje antes de codificar
3. Implemente incrementalmente
4. Teste cada parte antes de avançar

## Projeto 01 - Estudo de Caso: Stack Overflow Developer Survey: Perfil e Tendências da Comunidade de Desenvolvedores

**Objetivo:** Ler o Artigo Base e buscar construir análises que respondam questões que não foram contempladas no trabalho original.

O entregável será um relatório, em jupyter notebook (ou Google Colab), contendo todas os resultados das análises estatísticas e as discussões associadas a cada uma: o arquivo entregue deverá ser executável!

**Descrição:**
Utilize a base de dados da Stack Overflow Developer Survey para realizar análises estatísticas e responder a perguntas como:

- Qual é a distribuição de salários entre os desenvolvedores?
- Quais são as linguagens de programação mais populares?
- Existe alguma correlação entre anos de experiência e salário?
- Quais são as tendências de adoção de tecnologias ao longo do tempo?
- Quais são as diferenças de perfil entre desenvolvedores de diferentes regiões?
- Quais são as principais motivações para os desenvolvedores escolherem suas linguagens
- Quais são as principais barreiras enfrentadas pelos desenvolvedores em suas carreiras?

**Requisitos:**

- [ ] O produto será um relatório, em jupyter notebook (ou Google Colab), contendo todas os resultados das análises estatísticas e as discussões associadas a cada uma;
- [ ] Caso necessário,será incluído nas análises outros conjuntos de dados;

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

## Projeto 03 - Dashboard de vendas no Power BI

**Objetivo:** Construir um relatório de vendas ponta a ponta no Power BI, da preparação dos dados até a publicação, aplicando o conteúdo da seção [Power BI](/labs/data/power-bi/01-introducao-e-licencas/).

**Dataset sugerido:**
A [pasta de trabalho de Exemplo Financeiro](https://learn.microsoft.com/pt-br/power-bi/create-reports/sample-financial-download) da Microsoft, pública e gratuita (também disponível no Power BI Desktop em **Usar dados de exemplo**). Ela traz uma única tabela de vendas com colunas como `Segment`, `Country`, `Product`, `Units Sold`, `Sales`, `COGS`, `Profit` e `Date`. Parte do desafio é transformar essa tabela plana num modelo estrela. Se preferir outro dataset público de vendas, mantenha as mesmas etapas.

**Descrição:**
Monte um relatório que responda perguntas como:

- Quanto vendemos e qual foi a margem no período?
- Como as vendas evoluíram mês a mês e em relação ao ano anterior?
- Quais produtos, segmentos e países mais contribuem para o resultado?
- Onde a margem está abaixo do esperado?

**Etapas:**

1. **Power Query:** importe o arquivo, ajuste os tipos de dados, renomeie colunas para pt-BR, remova o que não for usado e crie as consultas de dimensão (produto, segmento, país) a partir da tabela original, usando consultas de referência e remoção de duplicatas. Veja [Power Query](/labs/data/power-bi/04-power-query/).
2. **Modelo estrela:** deixe a tabela de vendas como fato (`fVendas`), relacione as dimensões em um para muitos com filtro de direção única, crie uma `dCalendario` contínua, marque como tabela de datas e desative a data/hora automática. Veja [Modelagem de dados](/labs/data/power-bi/05-modelagem-de-dados/).
3. **Medidas DAX:** crie medidas explícitas para Total Vendas, Custo, Lucro, Margem %, Unidades, Vendas do ano anterior, Variação % AA e Vendas acumuladas no ano, usando `DIVIDE` e variáveis. Veja [DAX: fundamentos](/labs/data/power-bi/06-dax-fundamentos/) e [DAX: contexto, CALCULATE e inteligência de tempo](/labs/data/power-bi/07-dax-contexto-calculate-e-inteligencia-de-tempo/).
4. **Visuais:** monte ao menos duas páginas (visão geral e detalhe por produto) com cartões, linha de tendência, barras ordenadas, mapa ou matriz com formatação condicional e um tema consistente. Veja [Visualizações e formatação](/labs/data/power-bi/08-visualizacoes-e-formatacao/).
5. **Interatividade:** adicione segmentações de período e segmento sincronizadas entre páginas, um drill-through para o detalhe do produto e um navegador de páginas. Veja [Filtros, segmentações e interatividade](/labs/data/power-bi/09-filtros-segmentacoes-e-interatividade/).
6. **Publicação:** publique num workspace, crie um dashboard com os principais blocos e configure a atualização. Se tiver acesso a um ambiente com licença, crie uma função de RLS por país e teste. Veja [Serviço do Power BI](/labs/data/power-bi/10-servico-publicacao-e-dashboards/).

**Critérios de sucesso:**

- [ ] O modelo está em esquema estrela, sem relacionamentos bidirecionais desnecessários
- [ ] Nenhum visual usa agregação implícita: todos os números vêm de medidas formatadas
- [ ] Total Vendas, Lucro e Margem % batem com a soma conferida na tabela original
- [ ] A comparação com o ano anterior funciona ao filtrar qualquer mês
- [ ] Segmentações, drill-through e navegação funcionam como esperado para quem só lê o relatório
- [ ] O relatório publicado abre no serviço e o dashboard leva aos relatórios de origem
- [ ] Se for compartilhar publicamente (portfólio), usar apenas dados públicos como os do dataset sugerido

**Desafio extra:**

- Criar um layout móvel para a página de visão geral
- Adicionar uma medida de cor para formatação condicional da margem
- Usar cálculos visuais para uma média móvel de 3 meses e comparar com a medida equivalente

**Dica:**
Valide as medidas numa tabela simples antes de montar os gráficos. Um número errado bem formatado continua errado.
