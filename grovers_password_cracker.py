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
        target_bits = [int(bit) for bit in target[::-1]]
        for i, bit in enumerate(target_bits):
            if bit == 0: qc.x(i)
        qc.mcp(np.pi, list(range(self.n_qubits - 1)), self.n_qubits - 1)
        for i, bit in enumerate(target_bits):
            if bit == 0: qc.x(i)

    def create_diffusion(self, qc):
        qc.h(range(self.n_qubits))
        qc.x(range(self.n_qubits))
        qc.mcp(np.pi, list(range(self.n_qubits - 1)), self.n_qubits - 1)
        qc.x(range(self.n_qubits))
        qc.h(range(self.n_qubits))

    def calculate_iterations(self):
        N = 2 ** self.n_qubits
        return max(1, int((np.pi / 4) * np.sqrt(N)))

    def create_circuit(self, custom_iter=None):
        qr = QuantumRegister(self.n_qubits, "q")
        cr = ClassicalRegister(self.n_qubits, "c")
        qc = QuantumCircuit(qr, cr)
        qc.h(range(self.n_qubits))
        qc.barrier()
        
        iterations = custom_iter if custom_iter is not None else self.calculate_iterations()
        for _ in range(iterations):
            self.create_oracle(qc, self.target)
            qc.barrier()
            self.create_diffusion(qc)
            qc.barrier()
        qc.measure(qr, cr)
        self.circuit = qc
        return qc

    def run(self, shots=1000, custom_iter=None):
        self.create_circuit(custom_iter)
        job = self.simulator.run(self.circuit, shots=shots)
        counts = job.result().get_counts(self.circuit)
        return self.circuit, counts
