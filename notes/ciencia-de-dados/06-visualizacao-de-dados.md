# Visualização de Dados

## Por que visualizar

Uma tabela com 344 linhas não mostra padrão nenhum para o olho humano. O mesmo dado num gráfico de dispersão mostra três grupos de pinguins em um segundo. Visualização serve para duas coisas diferentes, e vale saber qual você está fazendo:

- **Explorar** - gráficos rápidos e feios, para você mesmo entender os dados (a [análise exploratória](/labs/data/ciencia-de-dados/05-analise-exploratoria/))
- **Comunicar** - gráficos caprichados, com título, rótulos e uma mensagem clara, para outra pessoa entender sem você do lado

## As bibliotecas

| Biblioteca     | Perfil                                                                                                                                      |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Matplotlib     | A base. Controle total de cada detalhe, mas exige mais código                                                                               |
| seaborn        | Gráficos estatísticos bonitos com uma linha, construído em cima do Matplotlib                                                               |
| Plotly         | Gráficos interativos (zoom, tooltip, filtro pela legenda) que rodam no navegador                                                            |
| pandas `.plot` | Atalho para o Matplotlib direto do DataFrame: `df["body_mass_g"].plot(kind="hist")`                                                         |
| Outras         | Bokeh e Altair (interativos), Dash (dashboards com Plotly, veja [Dashboards com Dash](/labs/data/ciencia-de-dados/07-dashboards-com-dash/)) |

Todos os exemplos usam o dataset de pinguins:

```python
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns

df = sns.load_dataset("penguins").dropna()
```

## Qual gráfico usar

Escolha o gráfico pela pergunta, não pelo que parece mais bonito.

| Pergunta                                    | Gráfico    | Matplotlib     | seaborn                 | Plotly Express |
| ------------------------------------------- | ---------- | -------------- | ----------------------- | -------------- |
| Como algo evolui no tempo?                  | Linha      | `plot`         | `lineplot`              | `px.line`      |
| Duas variáveis numéricas se relacionam?     | Dispersão  | `scatter`      | `scatterplot`           | `px.scatter`   |
| Como comparar quantidades entre categorias? | Barras     | `bar` / `barh` | `barplot`, `countplot`  | `px.bar`       |
| Como os valores se distribuem?              | Histograma | `hist`         | `histplot`              | `px.histogram` |
| Como a distribuição muda entre grupos?      | Box plot   | `boxplot`      | `boxplot`, `violinplot` | `px.box`       |
| Qual a participação de cada parte no todo?  | Pizza      | `pie`          | -                       | `px.pie`       |
| Como várias variáveis se correlacionam?     | Heatmap    | `imshow`       | `heatmap`               | `px.imshow`    |

Sobre pizza: funciona com 2 a 4 fatias bem diferentes. Com mais que isso, o olho não compara ângulos direito e um gráfico de barras ordenado comunica melhor.

## Matplotlib

O Matplotlib tem dois estilos de uso. O mais recomendado pela documentação é o **orientado a objetos**: você cria uma figura (`fig`) com um ou mais eixos (`ax`) e chama os métodos no eixo.

```python
fig, ax = plt.subplots(figsize=(8, 5))

ax.hist(df["body_mass_g"], bins=20, edgecolor="white")
ax.set_title("Distribuição da massa dos pinguins")
ax.set_xlabel("Massa (g)")
ax.set_ylabel("Quantidade")
ax.grid(alpha=0.3)

plt.show()
```

O estilo direto com `plt.plot`, `plt.title`, `plt.xlabel` também funciona e aparece muito em tutoriais. Ele é prático para um gráfico só, mas fica confuso quando há vários gráficos na mesma figura. Com `subplots`, cada eixo é independente:

```python
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].scatter(df["flipper_length_mm"], df["body_mass_g"], alpha=0.6)
axes[0].set_xlabel("Nadadeira (mm)")
axes[0].set_ylabel("Massa (g)")

contagem = df["species"].value_counts()
axes[1].bar(contagem.index, contagem.values)
axes[1].set_title("Pinguins por espécie")

fig.tight_layout()
fig.savefig("graficos.png", dpi=150)   # salva em arquivo
plt.show()
```

Para gráfico de linha você precisa de uma sequência ordenada (tempo, por exemplo). O dataset `flights` do seaborn tem passageiros por mês:

```python
voos = sns.load_dataset("flights")
por_ano = voos.groupby("year")["passengers"].sum()

fig, ax = plt.subplots()
ax.plot(por_ano.index, por_ano.values, marker="o")
ax.set_title("Passageiros por ano")
plt.show()
```

## seaborn

O seaborn recebe o DataFrame e os nomes das colunas, e cuida de cores, legendas e agrupamentos sozinho. O parâmetro `hue` colore por uma categoria, que é exatamente o que você quer na maioria das análises.

```python
sns.scatterplot(data=df, x="flipper_length_mm", y="body_mass_g", hue="species")
plt.show()

sns.histplot(data=df, x="body_mass_g", hue="species", kde=True)   # kde = curva suavizada
plt.show()

sns.countplot(data=df, x="island", hue="species")
plt.show()

sns.barplot(data=df, x="species", y="body_mass_g", errorbar="sd")  # média com barra de desvio
plt.show()
```

O `barplot` do seaborn mostra a **média** de cada grupo, não a soma, e por padrão desenha um intervalo de confiança. O `errorbar="sd"` troca para o desvio-padrão. Já o `countplot` conta linhas.

Como o seaborn devolve eixos do Matplotlib, você ajusta título e rótulos do mesmo jeito:

```python
ax = sns.boxplot(data=df, x="species", y="body_mass_g")
ax.set(title="Massa por espécie", xlabel="Espécie", ylabel="Massa (g)")
plt.show()
```

Outros que valem conhecer: `sns.heatmap` (matriz de correlação), `sns.pairplot` (todos os pares de colunas) e `sns.violinplot` (box plot com a forma da distribuição). O seaborn também traz datasets de exemplo: `sns.load_dataset("tips")`, `"titanic"`, `"flights"`, entre outros.

## Plotly Express

O Plotly gera gráficos em HTML com interatividade pronta: passe o mouse para ver o valor, arraste para dar zoom, clique na legenda para esconder uma série. No Jupyter o gráfico aparece direto na célula.

```python
fig = px.scatter(
    df,
    x="flipper_length_mm",
    y="body_mass_g",
    color="species",            # cor por categoria
    size="bill_length_mm",      # tamanho do ponto por uma coluna numérica
    hover_data=["island"],      # informação extra no tooltip
    labels={"flipper_length_mm": "Nadadeira (mm)", "body_mass_g": "Massa (g)"},
)
fig.update_layout(title="Nadadeira x massa", template="plotly_white")
fig.show()
```

Barras agrupadas, com uma agregação feita no pandas antes:

```python
media = df.groupby(["island", "species"], as_index=False)["body_mass_g"].mean()

fig = px.bar(media, x="island", y="body_mass_g", color="species", barmode="group")
fig.show()
```

Sem `barmode="group"`, as barras ficam empilhadas. O Plotly também tem datasets de exemplo, como `px.data.iris()`, `px.data.tips()` e `px.data.gapminder()`.

### Recursos avançados

```python
# 3D
px.scatter_3d(df, x="bill_length_mm", y="bill_depth_mm", z="flipper_length_mm", color="species")

# um gráfico por categoria (small multiples)
px.scatter(df, x="flipper_length_mm", y="body_mass_g", color="species", facet_col="island")

# animação ao longo do tempo
gap = px.data.gapminder()
px.scatter(gap, x="gdpPercap", y="lifeExp", size="pop", color="continent",
           animation_frame="year", log_x=True, size_max=55)

# mapa coroplético (países coloridos por um valor)
px.choropleth(gap.query("year == 2007"), locations="iso_alpha", color="lifeExp")
```

Para controle fino existe o módulo `plotly.graph_objects` (`go.Scatter3d`, `go.Surface`, `go.Mesh3d`) e `make_subplots` para combinar gráficos de tipos diferentes. Temas mudam com `template` (`"plotly_white"`, `"plotly_dark"`, `"simple_white"`).

Para salvar:

```python
fig.write_html("grafico.html")   # interativo, abre em qualquer navegador
fig.write_image("grafico.png")   # estático
```

O `write_image` precisa do pacote **Kaleido** (`pip install kaleido`), e a partir do Kaleido 1.0 ele usa um Chrome ou Chromium instalado na máquina. Se não tiver, rode `plotly_get_chrome` no terminal.

## Matplotlib x seaborn x Plotly

| Aspecto        | Matplotlib                                                  | seaborn                               | Plotly                                           |
| -------------- | ----------------------------------------------------------- | ------------------------------------- | ------------------------------------------------ |
| Interatividade | Zoom e pan em janelas interativas; na imagem salva, nenhuma | Igual ao Matplotlib                   | Tooltip, zoom, filtro na legenda, por padrão     |
| 3D             | Sim, via `mplot3d` (`projection="3d"`)                      | Não                                   | Sim, interativo                                  |
| Web            | Gera imagem (PNG, SVG, PDF)                                 | Gera imagem                           | Gera HTML, base do Dash                          |
| Facilidade     | Mais código, mais controle                                  | Mais fácil para gráficos estatísticos | Fácil com Plotly Express                         |
| Melhor uso     | Artigos, relatórios, ajuste fino                            | EDA rápida e bonita                   | Dashboards, apresentações, exploração interativa |

É comum ver a afirmação de que o Matplotlib "não é interativo" e "não faz 3D". Não é bem assim: rodando como script ou com `%matplotlib widget` no Jupyter, ele abre janelas com zoom e pan, e o `mplot3d` faz gráficos 3D. A diferença real é que o Plotly entrega interatividade na web por padrão, sem configurar nada.

Na prática muita gente usa seaborn para explorar e Plotly para mostrar.

## Boas práticas

- **Comece pela pergunta.** "Qual espécie é mais pesada?" pede box plot ou barras, não pizza
- **Título que diz algo.** "Gentoo pesa cerca de 1,3 kg a mais que as outras espécies" comunica mais que "Massa por espécie"
- **Rótulos com unidade.** "Massa (g)" e não `body_mass_g`
- **Eixo de barras começa no zero.** Cortar o eixo exagera diferenças pequenas. Em gráfico de linha e dispersão isso é menos crítico
- **Ordene as barras** pelo valor, a não ser que a categoria tenha ordem natural (meses, faixas etárias)
- **Cor com propósito.** Use cor para diferenciar grupos ou destacar um ponto, não para enfeitar. Paletas como `viridis` e as padrão do seaborn funcionam para daltônicos
- **Menos é mais.** Tire grade pesada, bordas, efeito 3D em gráfico 2D e legendas desnecessárias
- **Cuidado com sobreposição.** Com muitos pontos, use `alpha` (transparência) ou um gráfico de densidade

## Referências

- [Matplotlib - Quick start guide](https://matplotlib.org/stable/users/explain/quick_start.html) - Matplotlib, en
- [seaborn tutorial](https://seaborn.pydata.org/tutorial.html) - seaborn, en
- [Plotly Express in Python](https://plotly.com/python/plotly-express/) - Plotly, en
- [Static image export in Python](https://plotly.com/python/static-image-export/) - Plotly, en
