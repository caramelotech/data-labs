"""Gera os gráficos de análise bivariada da nota 05 (análise exploratória).

Uso (a partir da raiz do repositório):

    python examples/eda-charts/gerar_graficos_bivariados.py

As figuras são salvas em notes/ciencia-de-dados/assets/.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ROOT_PATH = Path(__file__).resolve().parents[2]
OUTPUT_PATH = ROOT_PATH / "notes" / "ciencia-de-dados" / "assets"

df = sns.load_dataset("penguins")


def save(fig, filename):
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_PATH / filename, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Salvo: {OUTPUT_PATH / filename}")


# numérica x numérica: dispersão colorida por espécie
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=df, x="flipper_length_mm", y="body_mass_g", hue="species", ax=ax)
ax.set_title("Pinguins com nadadeira maior são mais pesados, em três grupos")
ax.set_xlabel("Comprimento da nadadeira (mm)")
ax.set_ylabel("Massa corporal (g)")
ax.legend(title="Espécie")
ax.grid(alpha=0.3)
save(fig, "05-dispersao-nadadeira-massa.png")

# numérica x numérica: paradoxo de Simpson no comprimento x profundidade do bico
fig, (left, right) = plt.subplots(1, 2, figsize=(13, 5), sharey=True)

sns.regplot(data=df, x="bill_length_mm", y="bill_depth_mm", scatter_kws={"alpha": 0.6}, line_kws={"color": "black"}, ax=left)
left.set_title("Todos os pinguins juntos: relação negativa")
left.set_xlabel("Comprimento do bico (mm)")
left.set_ylabel("Profundidade do bico (mm)")
left.grid(alpha=0.3)

sns.scatterplot(data=df, x="bill_length_mm", y="bill_depth_mm", hue="species", alpha=0.7, ax=right)
sns.regplot(data=df, x="bill_length_mm", y="bill_depth_mm", scatter=False, color="gray", ax=right)
for _, group in df.groupby("species"):
    sns.regplot(data=group, x="bill_length_mm", y="bill_depth_mm", scatter=False, ci=None, line_kws={"linewidth": 1.5}, ax=right)
right.set_title("Separado por espécie: relação positiva em cada grupo")
right.set_xlabel("Comprimento do bico (mm)")
right.set_ylabel("Profundidade do bico (mm)")
right.legend(title="Espécie")
right.grid(alpha=0.3)

save(fig, "05-simpson-bico.png")

# categórica x numérica: box plot com pontos individuais
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=df, x="species", y="body_mass_g", color="white", ax=ax)
sns.stripplot(data=df, x="species", y="body_mass_g", hue="species", alpha=0.5, jitter=0.2, legend=False, ax=ax)
ax.set_title("Gentoo é bem mais pesado que Adelie e Chinstrap")
ax.set_xlabel("Espécie")
ax.set_ylabel("Massa corporal (g)")
ax.grid(alpha=0.3, axis="y")
save(fig, "05-box-massa-especie.png")

# categórica x categórica: heatmap da tabela cruzada
crosstab = pd.crosstab(df["species"], df["island"])
fig, ax = plt.subplots(figsize=(7, 4))
sns.heatmap(crosstab, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax)
ax.set_title("Gentoo só aparece em Biscoe, Chinstrap só em Dream")
ax.set_xlabel("Ilha")
ax.set_ylabel("Espécie")
save(fig, "05-heatmap-especie-ilha.png")
