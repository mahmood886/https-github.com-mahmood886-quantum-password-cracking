from grovers_password_cracker import GroverPasswordCracker

class ClassicalPasswordCracker:
    def __init__(self, target):
        self.target = target
    def crack(self):
        return {"attempts": (2**len(self.target) + 1) // 2}

def compare_classical_vs_quantum(target="1010", num_qubits=4, custom_iter=None):
    print("\n" + "="*60)
    print("CLASSICAL vs QUANTUM COMPARISON")
    print("="*60)
    classical = ClassicalPasswordCracker(target)
    classical_results = classical.crack()
    
    quantum = GroverPasswordCracker(target, num_qubits)
    q_attempts = custom_iter if custom_iter is not None else quantum.calculate_iterations()
    speedup = classical_results["attempts"] / q_attempts if q_attempts > 0 else 0
    
    print(f"Classical Brute Force: {classical_results['attempts']} attempts")
    print(f"Quantum Grover Search: {q_attempts} attempts")
    print(f"Quantum Speedup: {speedup:.2f}x")
    print("="*60)
