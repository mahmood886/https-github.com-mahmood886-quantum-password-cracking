import matplotlib.pyplot as plt

def plot_histogram(counts, target_password, title="Results"):
    # إغلاق أي رسمة قديمة لضمان عدم التداخل
    plt.close('all') 
    
    results_sorted = [x[0] for x in sorted(counts.items(), key=lambda x: x[1], reverse=True)]
    values_sorted = [x[1] for x in sorted(counts.items(), key=lambda x: x[1], reverse=True)]
    colors = ["#2ecc71" if r == target_password else "#3498db" for r in results_sorted]
    
    plt.figure("Quantum Simulation Histogram", figsize=(9, 4))
    plt.bar(results_sorted, values_sorted, color=colors, edgecolor="black")
    plt.title(f"Grover Search Results for Password: {target_password}", fontsize=12, fontweight='bold')
    plt.xlabel("States")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show(block=False) # يمنع تجميد البرنامج عند فتح الرسمة

def draw_quantum_circuit(circuit):
    try:
        # رسم الدائرة بستايل ملون واحترافي
        circuit.draw(output='mpl', style='iqp')
        plt.gcf().canvas.manager.set_window_title("Actual Quantum Circuit (Live View)")
        plt.tight_layout()
        plt.show(block=False)
    except Exception as e:
        print("\n📜 ACTUAL QUANTUM CIRCUIT TEXT VIEW:")
        print(circuit)
