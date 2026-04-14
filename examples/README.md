# Examples

Exemplos, exercícios e projetos práticos de dados.

## Arquivos

| Arquivo          | Descrição                              |
| ---------------- | -------------------------------------- |
| `README.md`      | Este índice                            |
| `exercises.md`   | Exercícios para praticar               |
| `projects.md`    | Mini projetos para aplicar o aprendido |

## Exemplos de código

Exemplos prontos para executar.

### Como usar

1. Escolha um exemplo
2. Leia o código e os comentários
3. Execute
4. Modifique e experimente

### exploração-basica

O ponto de partida para qualquer análise: entender o que tem no dataset.

```python
import pandas as pd

df = pd.read_csv('dados.csv')

print(df.shape)        # linhas e colunas
print(df.dtypes)       # tipos de cada coluna
print(df.isnull().sum()) # valores nulos por coluna
print(df.describe())   # estatísticas descritivas
```

**O que acontece:**

1. O CSV é carregado em um DataFrame
2. `shape` mostra as dimensões
3. `describe()` retorna contagem, média, desvio padrão, mínimo, máximo e quartis

**Variações para praticar:**

- Troque o CSV por outro dataset
- Use `df.sample(10)` para ver linhas aleatórias
- Filtre apenas colunas numéricas com `df.select_dtypes(include='number')`

> Adapte os exemplos para os seus próprios dados.
