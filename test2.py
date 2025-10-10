import numpy as np
import matplotlib.pyplot as plt

# Parameter
bit_rate = 1.200  # Bitrate in bits per second
f0 = 1.2  # Frequenz für Bit 0
f1 = 2.2  # Frequenz für Bit 1
fs = 2 * 19.2  # Abtastrate
bits = [1, 0, 1, 1, 0, 0, 0, 0]
Tb = 1 / bit_rate  # Bitdauer
t = np.arange(0, Tb * len(bits), 1 / fs)
phi = []


# Helper: FSK mit Phasensprung
def fsk_with_phase_jumps(bits, f0, f1, fs, Tb):
    signal = np.array([])
    for bit in bits:
        f = f1 if bit == 1 else f0
        t_bit = np.arange(0, Tb, 1 / fs)
        signal = np.concatenate((signal, np.sin(2 * np.pi * f * t_bit)))
    return signal


# Helper: FSK ohne Phasensprung (kontinuierlich)
def fsk_without_phase_jumps(bits, f0, f1, fs, Tb):
    phase = 0
    signal = []

    for bit in bits:
        f = f1 if bit == 1 else f0
        t_bit = np.arange(0, Tb, 1 / fs)
        dt = 1 / fs
        for _ in t_bit:
            phase += 2 * np.pi * f * dt
            phi.append(phase)
            signal.append(np.sin(phase))
    return np.array(signal)


# Generiere Signale
y_jump = fsk_with_phase_jumps(bits, f0, f1, fs, Tb)
y_cont = fsk_without_phase_jumps(bits, f0, f1, fs, Tb)

# Plotten
plt.figure(figsize=(12, 6))


plt.subplot(2, 1, 1)
plt.title("FSK mit Phasensprüngen")
plt.plot(t, y_jump * 10, t, phi)
plt.xticks(np.arange(0, Tb * len(bits), Tb))
plt.grid(True)

plt.subplot(2, 1, 2)
plt.title("FSK ohne Phasensprünge (kontinuierliche Phase)")
plt.plot(t, y_cont * 40, t, phi)
plt.grid(True)

plt.tight_layout()
plt.xticks(np.arange(0, Tb * len(bits), Tb))
plt.show()
