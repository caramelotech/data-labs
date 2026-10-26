# Métricas de Avaliação de Modelos

## Por que avaliar

Treinar um modelo é fácil: qualquer algoritmo do scikit-learn roda com `fit`. Difícil é saber se ele presta. Uma métrica transforma "parece bom" em um número que dá para comparar entre modelos, acompanhar ao longo do tempo e explicar para quem vai usar a previsão.

Duas regras valem para qualquer métrica:

- **Avalie em dados que o modelo não viu no treino.** Medir no próprio treino mostra o quanto ele decorou, não o quanto generaliza. As técnicas de separação (train/test split, holdout, validação cruzada) estão em [Validação, tuning e regularização](/labs/data/machine-learning/03-validacao-tuning-e-regularizacao/).
- **A métrica certa depende do problema e do custo de cada erro.** Errar o diagnóstico de uma doença grave não tem o mesmo peso que recomendar um filme ruim.

Cada tipo de problema tem sua família de métricas:

| Tipo de problema | Métricas comuns                                                      |
| ---------------- | -------------------------------------------------------------------- |
| Classificação    | matriz de confusão, accuracy, precision, recall, F1, ROC-AUC, PR-AUC |
| Regressão        | MAE, MSE, RMSE, R²                                                   |
| Clustering       | silhouette score, índice Davies-Bouldin                              |

## Métricas de classificação

### Matriz de confusão

Tudo em classificação binária começa por aqui. A matriz cruza o que o modelo previu com o que era verdade. Pense num detector de spam em que "positivo" = spam:

|                    | Previsto: positivo       | Previsto: negativo       |
| ------------------ | ------------------------ | ------------------------ |
| **Real: positivo** | TP (verdadeiro positivo) | FN (falso negativo)      |
| **Real: negativo** | FP (falso positivo)      | TN (verdadeiro negativo) |

- **TP**: era spam e o modelo disse spam. ✅
- **TN**: não era spam e o modelo disse que não era. ✅
- **FP**: não era spam, mas o modelo disse que era. Também chamado de **erro tipo I** (alarme falso). Aquele e-mail importante que foi parar na caixa de spam.
- **FN**: era spam, mas o modelo deixou passar. Também chamado de **erro tipo II**. O spam que chegou na caixa de entrada.

Atenção à ordem no scikit-learn: `confusion_matrix` coloca as classes em ordem crescente, então para rótulos 0 e 1 a primeira linha é a classe 0 (negativos) e a matriz sai como `[[TN, FP], [FN, TP]]`.

### Accuracy, precision, recall e F1

Com os quatro valores da matriz, saem as métricas mais usadas:

```text
accuracy  = (TP + TN) / (TP + TN + FP + FN)
precision = TP / (TP + FP)
recall    = TP / (TP + FN)
F1        = 2 · (precision · recall) / (precision + recall)
```

- **Accuracy** (acurácia): fração de acertos no total. Intuitiva, mas engana quando as classes são desbalanceadas. Se só 1% das transações são fraude, um modelo que diz "nunca é fraude" tem 99% de accuracy e não serve para nada. O assunto é aprofundado em [Dados desbalanceados](/labs/data/machine-learning/04-dados-desbalanceados/).
- **Precision** (precisão): dos que o modelo disse que eram positivos, quantos eram mesmo? Importa quando o falso positivo é caro, como mandar um e-mail legítimo para o spam ou bloquear o cartão de um cliente sem motivo.
- **Recall** (revocação, sensibilidade, taxa de verdadeiros positivos): dos positivos que existiam, quantos o modelo encontrou? Importa quando o falso negativo é caro, como deixar passar uma fraude ou não detectar um tumor.
- **F1-score**: média harmônica entre precision e recall. A média harmônica pune desequilíbrio: com precision 1.0 e recall 0.1, a média simples daria 0.55, mas o F1 dá cerca de 0.18. Útil quando você quer um número só que exija as duas coisas ao mesmo tempo.

Precision e recall puxam em direções opostas. Baixar o limiar de decisão (lembra dele em [Algoritmos de machine learning](/labs/data/machine-learning/01-algoritmos-de-machine-learning/)?) faz o modelo dizer "positivo" mais vezes: o recall sobe e a precision tende a cair. Subir o limiar faz o contrário.

```python
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_breast_cancer(return_X_y=True)
X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=42
)

modelo = make_pipeline(StandardScaler(), LogisticRegression())
modelo.fit(X_treino, y_treino)
y_pred = modelo.predict(X_teste)

print(confusion_matrix(y_teste, y_pred))  # [[TN, FP], [FN, TP]]
print("accuracy :", round(accuracy_score(y_teste, y_pred), 3))
print("precision:", round(precision_score(y_teste, y_pred), 3))
print("recall   :", round(recall_score(y_teste, y_pred), 3))
print("F1       :", round(f1_score(y_teste, y_pred), 3))

# tudo de uma vez, por classe
print(classification_report(y_teste, y_pred))
```

O `classification_report` também mostra a média _macro_ (média simples entre as classes) e a _weighted_ (ponderada pelo número de amostras de cada classe). Em problemas com mais de duas classes, a macro trata todas as classes como igualmente importantes, o que ajuda a enxergar classes pequenas que o modelo está ignorando.

### Curva ROC e AUC

Precision, recall e F1 dependem de um limiar fixo. A curva ROC mostra o comportamento do modelo em **todos os limiares** de uma vez. Ela cruza duas taxas:

```text
TPR (taxa de verdadeiros positivos) = TP / (TP + FN)   ← é o recall
FPR (taxa de falsos positivos)      = FP / (FP + TN)
```

Para cada limiar possível, calcula-se o par (FPR, TPR) e marca-se um ponto no gráfico. Com limiar 1.0 o modelo nunca diz positivo (ponto 0,0); com limiar 0.0 diz sempre (ponto 1,1). Um bom modelo sobe rápido para o canto superior esquerdo: recall alto com poucos falsos positivos.

A **AUC** (_area under the curve_) resume a curva num número entre 0 e 1. Uma interpretação útil: é a probabilidade de o modelo dar uma pontuação maior a um positivo sorteado do que a um negativo sorteado.

| AUC             | Leitura                                                                     |
| --------------- | --------------------------------------------------------------------------- |
| 1.0             | separação perfeita                                                          |
| entre 0.5 e 1.0 | quanto mais perto de 1, melhor o modelo ordena positivos acima de negativos |
| 0.5             | igual a chutar aleatoriamente (a diagonal do gráfico)                       |
| abaixo de 0.5   | **pior que o acaso**                                                        |

AUC abaixo de 0.5 não quer dizer só "modelo fraco": significa que o modelo ordena sistematicamente ao contrário. Na prática, quase sempre é sinal de bug, como rótulos invertidos na hora de montar o `y` ou uso da coluna de probabilidade errada (`predict_proba(X)[:, 0]` em vez de `[:, 1]`). Inverter as previsões nesse caso daria uma AUC de `1 - AUC`, mas o certo é achar e corrigir o erro.

```python
from sklearn.metrics import RocCurveDisplay, roc_auc_score

# continua do exemplo anterior
probas = modelo.predict_proba(X_teste)[:, 1]  # probabilidade da classe positiva
print("ROC-AUC:", round(roc_auc_score(y_teste, probas), 3))

# desenha a curva (precisa do matplotlib instalado)
RocCurveDisplay.from_predictions(y_teste, probas)
```

Note que `roc_auc_score` recebe **probabilidades ou pontuações**, não as classes previstas. Passar `y_pred` (zeros e uns) funciona sem erro, mas calcula a AUC de um único limiar e dá um número enganoso.

Em problemas muito desbalanceados, a curva ROC pode parecer otimista porque o FPR fica pequeno quando há muitos negativos. Nesses casos a curva precision-recall e a **PR-AUC** (no scikit-learn, `average_precision_score`) costumam ser mais informativas; veja [Dados desbalanceados](/labs/data/machine-learning/04-dados-desbalanceados/).

## Métricas de regressão

Em regressão o erro de cada amostra é a diferença entre o valor real `yᵢ` e o previsto `ŷᵢ`. As métricas variam no jeito de juntar esses erros:

```text
MAE  = (1/n) · Σ |yᵢ - ŷᵢ|
MSE  = (1/n) · Σ (yᵢ - ŷᵢ)²
RMSE = √MSE
R²   = 1 - Σ (yᵢ - ŷᵢ)² / Σ (yᵢ - ȳ)²
```

Onde `n` é o número de amostras e `ȳ` é a média dos valores reais.

- **MAE** (erro absoluto médio): a média do tamanho dos erros, na mesma unidade do alvo. "Em média, o modelo erra o preço em R$ 30 mil." Fácil de explicar e menos sensível a erros extremos.
- **MSE** (erro quadrático médio): eleva os erros ao quadrado antes da média, então pune muito mais os erros grandes. A unidade fica ao quadrado (reais²), o que dificulta a leitura. É a função de custo da regressão linear.
- **RMSE** (raiz do erro quadrático médio): a raiz do MSE, de volta à unidade original. Como herda o quadrado, um RMSE bem maior que o MAE indica que existem alguns erros muito grandes.
- **R²** (coeficiente de determinação): compara o modelo com um "modelo bobo" que sempre prevê a média `ȳ`. R² = 1 é perfeito, R² = 0 é tão bom quanto prever a média, e **R² pode ser negativo** quando o modelo é pior que prever a média. Isso acontece de verdade, por exemplo com um modelo muito overfitado avaliado no teste ou com um bug no pré-processamento. O nome "R ao quadrado" engana: nada impede que ele fique abaixo de zero.

```python
import numpy as np
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    root_mean_squared_error,
)

y_real = np.array([300, 410, 500, 620, 700])
y_prev = np.array([310, 400, 520, 590, 720])

print("MAE :", mean_absolute_error(y_real, y_prev))
print("MSE :", mean_squared_error(y_real, y_prev))
print("RMSE:", round(root_mean_squared_error(y_real, y_prev), 2))
print("R²  :", round(r2_score(y_real, y_prev), 3))

# um "modelo" pior que prever a média: R² negativo
y_ruim = np.array([700, 620, 500, 410, 300])
print("R² do modelo ruim:", round(r2_score(y_real, y_ruim), 3))
```

A função `root_mean_squared_error` existe desde o scikit-learn 1.4. Em código antigo você vai ver `mean_squared_error(..., squared=False)`, parâmetro que foi removido nas versões recentes.

Qual escolher? MAE quando todos os erros pesam igual e você quer explicar para gente de negócio; RMSE quando errar muito em poucos casos é bem pior que errar pouco em muitos; R² para comparar com a linha de base "prever a média". Reportar MAE e RMSE juntos costuma contar a história melhor que qualquer um sozinho.

Séries temporais usam as mesmas métricas e mais o MAPE (erro percentual), com uma pegadinha quando o valor real é zero; isso fica em [Séries temporais](/labs/data/machine-learning/05-series-temporais/).

## Métricas de clustering

Em clustering não há resposta certa para comparar, então as métricas internas medem o quanto os grupos são compactos e separados:

- **Silhouette score**: para cada ponto, compara a distância média aos pontos do próprio grupo (`a`) com a distância média aos pontos do grupo vizinho mais próximo (`b`): `s = (b - a) / max(a, b)`. Vai de -1 a 1. Perto de 1, o ponto está bem encaixado; perto de 0, está na fronteira; negativo, provavelmente está no grupo errado. O score final é a média de todos os pontos.
- **Índice Davies-Bouldin**: para cada grupo, olha o grupo mais parecido com ele, comparando o espalhamento interno com a distância entre os centróides. Aqui **quanto menor, melhor**, com 0 como mínimo.

```python
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from sklearn.metrics import davies_bouldin_score, silhouette_score

X, _ = make_blobs(n_samples=500, centers=3, random_state=42)
rotulos = KMeans(n_clusters=3, n_init="auto", random_state=42).fit_predict(X)

print("silhouette    :", round(silhouette_score(X, rotulos), 3))
print("Davies-Bouldin:", round(davies_bouldin_score(X, rotulos), 3))
```

As duas métricas favorecem grupos "redondos" e bem separados, então podem subestimar algoritmos como o DBSCAN, que encontra grupos de formato irregular. Use-as para comparar configurações, junto com uma olhada nos grupos e no que eles significam para o negócio. A escolha de K pelo silhouette aparece em [Algoritmos de machine learning](/labs/data/machine-learning/01-algoritmos-de-machine-learning/).

## Referências

- [Classificação: acurácia, recall, precisão e métricas relacionadas](https://developers.google.com/machine-learning/crash-course/classification/accuracy-precision-recall?hl=pt-br) - Google for Developers, pt-BR
- [Classificação: ROC e AUC](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc?hl=pt-br) - Google for Developers, pt-BR
- [Metrics and scoring: quantifying the quality of predictions](https://scikit-learn.org/stable/modules/model_evaluation.html) - scikit-learn, en
- [Clustering performance evaluation](https://scikit-learn.org/stable/modules/clustering.html#clustering-performance-evaluation) - scikit-learn, en
