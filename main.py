import tkinter as tk
from grovers_password_cracker import GroverPasswordCracker
import matplotlib.pyplot as plt

def run_simulation():
    password = entry.get()

    cracker = GroverPasswordCracker(password)

    circuit, counts = cracker.run()

    total = sum(counts.values())
    success = counts.get(password, 0)
    prob = (success / total) * 100 if total > 0 else 0

    best = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]

    text = f"""
Target: {password}
Success Rate: {prob:.2f}%
Hits: {success}/{total}

Top Results:
"""

    for b in best:
        text += f"{b[0]} -> {b[1]}\n"

    output.config(text=text)

    labels = [b[0] for b in best]
    values = [b[1] for b in best]

    plt.figure(figsize=(8,4))
    plt.bar(labels, values)
    plt.title("Quantum Results Histogram")
    plt.xlabel("States")
    plt.ylabel("Frequency")
    plt.show()

window = tk.Tk()
window.title("Quantum Password Cracking")
window.geometry("550x400")

tk.Label(window, text="🔐 Enter Binary Password").pack(pady=10)

entry = tk.Entry(window, font=("Arial", 12))
entry.pack(pady=5)

tk.Button(
    window,
    text="Run Quantum Simulation",
    command=run_simulation,
    bg="green",
    fg="white"
).pack(pady=10)

output = tk.Label(window, text="", justify="left")
output.pack(pady=20)

window.mainloop()
