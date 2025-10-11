import numpy as np
import matplotlib.pyplot as plt


def goertzel(samples, f_target, fs):
    """Einfacher Frequenzdetektor"""
    N = len(samples)
    k = int(0.5 + N * f_target / fs)
    omega = 2 * np.pi * k / N
    coeff = 2 * np.cos(omega)
    s_prev = 0
    s_prev2 = 0
    for sample in samples:
        s = sample + coeff * s_prev - s_prev2
        s_prev2 = s_prev
        s_prev = s
    power = s_prev2**2 + s_prev**2 - coeff * s_prev * s_prev2
    return power

fs = 10000  # Abtastrate
f0 = 1000   # Frequenz für Bit 0
f1 = 2000   # Frequenz für Bit 1
Tb = 0.01   # Bitdauer (10 ms)
samples_per_bit = int(Tb * fs)

# Beispielbitfolge
bits = [0, 1, 0, 1, 1, 0]

# CFSK Signal erzeugen
t = np.arange(0, Tb * len(bits), 1/fs)
signal = np.zeros_like(t)
phase = 0

for i, bit in enumerate(bits):
    f = f1 if bit == 1 else f0
    for j in range(samples_per_bit):
        idx = i * samples_per_bit + j
        phase += 2 * np.pi * f / fs
        signal[idx] = np.cos(phase)

plt.plot(t[:500], signal[:500])
plt.title("CFSK-Signal")
plt.xlabel("Zeit [s]")
plt.ylabel("Amplitude")
plt.grid()
plt.show()




demodulated_bits = []

for i in range(len(bits)):
    chunk = signal[i*samples_per_bit : (i+1)*samples_per_bit]
    p0 = goertzel(chunk, f0, fs)
    p1 = goertzel(chunk, f1, fs)
    bit = 1 if p1 > p0 else 0
    demodulated_bits.append(bit)

print("Empfangene Bits:", demodulated_bits)

