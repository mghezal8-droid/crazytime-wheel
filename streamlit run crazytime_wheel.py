import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
import time

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Crazy Time RNG", page_icon="🎡", layout="centered")

st.title("🎡 Crazy Time RNG - Simulation interactive")
st.write("Roue vectorielle fluide avec pondérations ajustables (inspirée du jeu Crazy Time).")

# --- Segments réels de la roue ---
segments = (
    ["1"] * 21
    + ["2"] * 13
    + ["5"] * 7
    + ["10"] * 4
    + ["Coin Flip"] * 4
    + ["Cash Hunt"] * 2
    + ["Pachinko"] * 2
    + ["Crazy Time"] * 1
)
assert len(segments) == 52, "Erreur : la roue doit avoir 52 segments."

# --- Couleurs par type ---
colors = {
    "1": "#f6d743",
    "2": "#4eb1d4",
    "5": "#ec6f3c",
    "10": "#9467bd",
    "Coin Flip": "#00bcd4",
    "Cash Hunt": "#a0cf4f",
    "Pachinko": "#ffb347",
    "Crazy Time": "#d62828",
}

# ------------------ INTERFACE DES PONDÉRATIONS ------------------
st.sidebar.header("⚙️ Pondération personnalisée")
st.sidebar.write("Ajuste la probabilité de chaque type de segment :")

weight_1 = st.sidebar.slider("Poids du 1", 0.1, 3.0, 1.0, 0.1)
weight_2 = st.sidebar.slider("Poids du 2", 0.1, 3.0, 1.0, 0.1)
weight_5 = st.sidebar.slider("Poids du 5", 0.1, 3.0, 1.0, 0.1)
weight_10 = st.sidebar.slider("Poids du 10", 0.1, 3.0, 1.0, 0.1)
weight_coinflip = st.sidebar.slider("Poids Coin Flip", 0.1, 3.0, 1.0, 0.1)
weight_cashhunt = st.sidebar.slider("Poids Cash Hunt", 0.1, 3.0, 1.0, 0.1)
weight_pachinko = st.sidebar.slider("Poids Pachinko", 0.1, 3.0, 1.0, 0.1)
weight_crazytime = st.sidebar.slider("Poids Crazy Time", 0.1, 3.0, 1.0, 0.1)

weights_map = {
    "1": weight_1,
    "2": weight_2,
    "5": weight_5,
    "10": weight_10,
    "Coin Flip": weight_coinflip,
    "Cash Hunt": weight_cashhunt,
    "Pachinko": weight_pachinko,
    "Crazy Time": weight_crazytime,
}

# ------------------ RNG AVEC PONDÉRATION ------------------
weighted_segments = []
for seg in segments:
    # multiplie les occurrences selon le poids choisi
    count = int(10 * weights_map[seg])
    weighted_segments.extend([seg] * count)

# ------------------ FONCTION D’AFFICHAGE ------------------
def draw_wheel(angle=0, highlight=None):
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(aspect="equal"))
    wedges, texts = ax.pie(
        [1] * len(segments),
        labels=segments,
        startangle=90 + angle,
        colors=[colors[s] for s in segments],
        textprops={"fontsize": 6},
    )
    ax.text(0, 1.15, "▼", ha="center", va="center", fontsize=25, color="black")
    if highlight:
        for i, s in enumerate(segments):
            if s == highlight:
                wedges[i].set_edgecolor("red")
                wedges[i].set_linewidth(2)
    return fig

# ------------------ LANCEMENT DU SPIN ------------------
if st.button("🎰 Lancer la roue !"):
    result = random.choice(weighted_segments)
    result_index = segments.index(result)

    # Animation fluide
    total_rotation = random.randint(1080, 2880) + (360 / len(segments)) * result_index
    steps = 60
    for i in range(steps):
        fig = draw_wheel(angle=(total_rotation * (i + 1) / steps))
        st.pyplot(fig)
        time.sleep(0.03 + i * 0.01)

    # Résultat final
    fig = draw_wheel(angle=total_rotation, highlight=result)
    st.pyplot(fig)
    st.success(f"🎯 Résultat : **{result}**")

else:
    st.info("Appuie sur **Lancer la roue !** pour faire tourner la roue 🎡")
