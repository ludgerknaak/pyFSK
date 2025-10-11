import numpy as np
import matplotlib.pyplot as plt

# Parameter
bit_rate = 1200  # Bitrate in bits per second
f0 = 1200  # Frequenz für Bit 0
f1 = 2200  # Frequenz für Bit 1
fs = 19200  # Abtastrate
Start = 0
Stop = 1
Parity = 1
# bits = [Start, 1, 1, 1, 1, 0, 0, 0, 0, Parity, Stop]
bits = [0, 1]

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
            # phase += 2 * np.pi * f * dt
            phi.append(phase)
            signal.append(np.sin(phase))
            phase += 2 * np.pi * f * dt
    return np.array(signal)


# Helper: FSK ohne Phasensprung (kontinuierlich)
def fsk0_without_phase_jumps(bits, f0, f1, fs, Tb):
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
# y_jump = fsk_with_phase_jumps(bits, f0, f1, fs, Tb)
y_cont = fsk_without_phase_jumps(bits, f0, f1, fs, Tb)
y0_cont = fsk0_without_phase_jumps(bits, f0, f1, fs, Tb)

# Plotten
plt.figure(figsize=(12, 6))


plt.subplot(2, 1, 1)
plt.title("FSK mit Phasensprüngen")
plt.stem(t, y0_cont)
plt.xticks(np.arange(0, Tb * len(bits), Tb))
plt.grid(True)

plt.subplot(2, 1, 2)
plt.title("FSK ohne Phasensprünge (kontinuierliche Phase)")
plt.stem(t, y_cont)
plt.grid(True)

plt.tight_layout()
plt.xticks(np.arange(0, Tb * len(bits), Tb))
plt.show()
