
from grovers_password_cracker import GroverPasswordCracker

class ClassicalPasswordCracker:
    def __init__(self, target):
        self.target = target
    def crack(self):
        num_bits = len(self.target)
        return {"attempts": (2**num_bits + 1) // 2}

def compare_classical_vs_quantum(target="1010", num_qubits=4, quantum_shots=1000):
    print(chr(10) + "="*70)
    print("CLASSICAL vs QUANTUM COMPARISON")
    print("="*70)
    classical = ClassicalPasswordCracker(target)
    classical_results = classical.crack()
    quantum = GroverPasswordCracker(target, num_qubits)
    iterations = quantum.calculate_iterations()
    speedup = classical_results["attempts"] / iterations
    print(f"Classical: {classical_results["attempts"]} attempts")
    print(f"Quantum: {iterations} attempts")
    print(f"Speedup: {speedup:.2f}x")
    print("="*70)
