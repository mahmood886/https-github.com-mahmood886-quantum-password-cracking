import customtkinter as ctk
from grovers_password_cracker import GroverPasswordCracker
from comparison import compare_classical_vs_quantum
from visualization import plot_histogram, draw_quantum_circuit

# إعداد الثيم المظلم والمستقبلي للوحة التحكم
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

def run_simulation():
    password = entry.get()
    user_shots = int(shots_slider.get())
    selected_iter_mode = iter_dropdown.get()
    
    custom_iter = None
    if selected_iter_mode != "Auto (Theoretical)":
        custom_iter = int(selected_iter_mode.split()[0])
        
    cracker = GroverPasswordCracker(password)
    circuit, counts = cracker.run(shots=user_shots, custom_iter=custom_iter)

    total = sum(counts.values())
    success = counts.get(password, 0)
    prob = (success / total) * 100 if total > 0 else 0
    best = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]

    text = f"🎯 Target Password: {password}\n"
    text += f"⚡ Quantum Success Rate: {prob:.2f}%\n"
    text += f"🎯 Hits Found: {success}/{total}\n\n"
    text += "🏆 Top States Frequencies:\n"
    text += "--------------------------------------\n"
    for b in best:
        text += f"  State [ {b[0]} ]   --->   {b[1]} hits\n"
    output.configure(text=text)

    # استدعاء المقارنة وطباعتها في الـ Prompt
    compare_classical_vs_quantum(password, custom_iter=custom_iter)
    
    # فتح نوافذ المخطط البياني ودائرة الكيومبيوتر الكمية حية
    plot_histogram(counts, password)
    draw_quantum_circuit(circuit)

def update_slider_label(value):
    slider_val_label.configure(text=f"{int(value)} Shots")

# بناء لوحة التحكم الرسومية المودرن
window = ctk.CTk()
window.title("Advanced Quantum Control Center")
window.geometry("620x650")

title_label = ctk.CTkLabel(window, text="⚛️ Quantum Grover Control Panel", font=("Arial", 22, "bold"), text_color="#2ecc71")
title_label.pack(pady=15)

input_frame = ctk.CTkFrame(window, corner_radius=10)
input_frame.pack(pady=10, padx=20, fill="x")
ctk.CTkLabel(input_frame, text="Enter 4-Bit Password:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=15, pady=15)
entry = ctk.CTkEntry(input_frame, placeholder_text="1010", width=120, height=30, font=("Arial", 14), justify="center")
entry.grid(row=0, column=1, padx=15, pady=15)
entry.insert(0, "1010")

controls_frame = ctk.CTkFrame(window, corner_radius=10)
controls_frame.pack(pady=10, padx=20, fill="x")
ctk.CTkLabel(controls_frame, text="Quantum Engine Parameters", font=("Arial", 14, "bold"), text_color="#3498db").pack(pady=5)

shots_label_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
shots_label_frame.pack(fill="x", padx=20)
ctk.CTkLabel(shots_label_frame, text="Simulation Shots:", font=("Arial", 12)).pack(side="left")
slider_val_label = ctk.CTkLabel(shots_label_frame, text="1000 Shots", font=("Arial", 12, "bold"), text_color="#2ecc71")
slider_val_label.pack(side="right")

shots_slider = ctk.CTkSlider(controls_frame, from_=100, to=5000, number_of_steps=49, command=update_slider_label)
shots_slider.pack(pady=5, padx=20, fill="x")
shots_slider.set(1000)

iter_label_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
iter_label_frame.pack(fill="x", padx=20, pady=5)
ctk.CTkLabel(iter_label_frame, text="Grover Iterations (T):", font=("Arial", 12)).pack(side="left")
iter_dropdown = ctk.CTkComboBox(iter_label_frame, values=["Auto (Theoretical)", "1 Iteration", "2 Iterations", "3 Iterations", "4 Iterations"], width=180)
iter_dropdown.pack(side="right")
iter_dropdown.set("Auto (Theoretical)")

btn = ctk.CTkButton(window, text="LAUNCH QUANTUM COMPUTATION", command=run_simulation, font=("Arial", 14, "bold"), height=45, corner_radius=10)
btn.pack(pady=15)

result_frame = ctk.CTkFrame(window, corner_radius=10)
result_frame.pack(pady=10, padx=20, fill="both", expand=True)
output = ctk.CTkLabel(result_frame, text="\nSystem Ready. Press Launch...", justify="left", font=("Courier New", 13), anchor="w")
output.pack(pady=15, padx=20, fill="both")

window.mainloop()
