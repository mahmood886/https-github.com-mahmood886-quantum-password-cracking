
import sys
from grovers_password_cracker import GroverPasswordCracker
from visualization import plot_histogram
from comparison import compare_classical_vs_quantum

print(chr(10) + '='*70)
print('🔐 QUANTUM PASSWORD CRACKING')
print('='*70)

target = '1010'
cracker = GroverPasswordCracker(target, 4)
circuit, counts = cracker.run(shots=1000)
cracker.print_results(counts)

fig = plot_histogram(counts, target)
fig.savefig('histogram.png')
print('✅ Histogram saved!')

compare_classical_vs_quantum(target, 4, 1000)
