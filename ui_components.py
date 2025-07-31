import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

def plot_radar_chart(category_scores):
    categories = list(category_scores.keys())
    values = list(category_scores.values())
    N = len(categories)

    if N == 0:
        st.warning("Not enough category data to plot a radar chart.")
        return

    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2, linestyle='solid', color="blue")
    ax.fill(angles, values, alpha=0.3, color="blue")

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"])
    ax.set_ylim(0, 1)

    st.pyplot(fig)
