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
