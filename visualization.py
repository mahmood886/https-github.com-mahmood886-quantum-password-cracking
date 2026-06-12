
import matplotlib.pyplot as plt
from grovers_password_cracker import GroverPasswordCracker

def plot_histogram(counts, target_password, title="Results"):
    results = list(counts.keys())
    values = list(counts.values())
    sorted_data = sorted(zip(results, values), key=lambda x: x[1], reverse=True)
    results_sorted = [x[0] for x in sorted_data]
    values_sorted = [x[1] for x in sorted_data]
    colors = ["#2ecc71" if r == target_password else "#3498db" for r in results_sorted]
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(results_sorted, values_sorted, color=colors, edgecolor="black")
    ax.set_xlabel("Results")
    ax.set_ylabel("Count")
    ax.set_title(title)
    return fig
