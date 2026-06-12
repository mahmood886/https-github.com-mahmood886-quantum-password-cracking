from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import AerSimulator
import numpy as np

class GroverPasswordCracker:
    def __init__(self, target_password, num_qubits=4):
        self.target = target_password
        self.n_qubits = num_qubits
        self.simulator = AerSimulator()
        self.circuit = None
    
    def create_oracle(self, qc, target):
        target_bits = [int(bit) for bit in target]
        for i, bit in enumerate(target_bits):
            if bit == 0:
                qc.x(i)
        if self.n_qubits == 4:
            qc.h(3)
            qc.ccx(2, 1, 3)
            qc.cx(0, 1)
            qc.ccx(2, 1, 3)
            qc.cx(0, 1)
            qc.h(3)
        for i, bit in enumerate(target_bits):
            if bit == 0:
                qc.x(i)
    
    def create_diffusion(self, qc):
        qc.h(range(self.n_qubits))
        qc.x(range(self.n_qubits))
        qc.h(self.n_qubits - 1)
        if self.n_qubits == 4:
            qc.h(3)
            qc.ccx(2, 1, 3)
            qc.cx(0, 1)
            qc.ccx(2, 1, 3)
            qc.cx(0, 1)
            qc.h(3)
        qc.h(self.n_qubits - 1)
        qc.x(range(self.n_qubits))
        qc.h(range(self.n_qubits))
    
    def calculate_iterations(self):
        N = 2 ** self.n_qubits
        return int((np.pi / 4) * np.sqrt(N))
    
    def create_circuit(self):
        qr = QuantumRegister(self.n_qubits, "q")
        cr = ClassicalRegister(self.n_qubits, "c")
        qc = QuantumCircuit(qr, cr)
        qc.h(range(self.n_qubits))
        qc.barrier()
        iterations = self.calculate_iterations()
        for _ in range(iterations):
            self.create_oracle(qc, self.target)
            qc.barrier()
            self.create_diffusion(qc)
            qc.barrier()
        qc.measure(qr, cr)
        self.circuit = qc
        return qc
    
    def run(self, shots=1000):
        if self.circuit is None:
            self.create_circuit()
        job = self.simulator.run(self.circuit, shots=shots)
        result = job.result()
        counts = result.get_counts(self.circuit)
        return self.circuit, counts
    
    def get_statistics(self, counts):
        total = sum(counts.values())
        correct = counts.get(self.target, 0)
        return {"correct": correct, "total": total, "prob": (correct/total)*100}
    
    def print_results(self, counts):
        print(chr(10) + "="*60)
        print(f"🔐 Results for {self.target}")
        print("="*60)
        stats = self.get_statistics(counts)
        print(f"Target: {self.target}")
        print(f"Success Probability: {stats["prob"]:.2f}%")
        print(f"Correct Results: {stats["correct"]} / {stats["total"]}")
        print(chr(10) + "Top 5 Results:")
        for result, count in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            pct = (count/stats["total"])*100
            print(f"  {result}: {count:4d} ({pct:5.1f}%)")
        print("="*60)
