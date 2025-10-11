import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

# Parameter
fs = 10000  # Abtastrate [Hz]
fc = 1000   # Trägerfrequenz [Hz]
f_dev = 200  # Frequenzabweichung für CFSK [Hz]
symbol_rate = 100  # Symbolrate [Symbole/s]
samples_per_symbol = int(fs / symbol_rate)

# Zeitachse
duration = 1  # Sekunden
t = np.arange(0, duration, 1/fs)

# Generiere zufällige Binärdaten
np.random.seed(0)
data = np.random.randint(0, 2, int(duration * symbol_rate))

# CFSK-Signal generieren
freqs = np.where(data == 0, fc - f_dev, fc + f_dev)
signal = np.zeros(len(t))

for i, bit in enumerate(data):
    idx_start = i * samples_per_symbol
    idx_end = idx_start + samples_per_symbol
    freq = freqs[i]
    if idx_end <= len(t):
        signal[idx_start:idx_end] = np.cos(2 * np.pi * freq * t[idx_start:idx_end])

# === Quadratur-Demodulation ===

# 1. Mischen mit Träger (IQ Demodulation)
i_mix = signal * np.cos(2 * np.pi * fc * t)
q_mix = -signal * np.sin(2 * np.pi * fc * t)

# 2. Tiefpassfilter definieren
def lowpass_filter(data, cutoff=500, fs=10000, order=5):
    b, a = butter(order, cutoff / (0.5 * fs), btype='low')
    return lfilter(b, a, data)

# 3. Filtere I und Q
i_baseband = lowpass_filter(i_mix)
q_baseband = lowpass_filter(q_mix)

# 4. Komplexes Basisbandsignal
z = i_baseband + 1j * q_baseband

# 5. Instantane Phase und Frequenz
phase = np.unwrap(np.angle(z))
inst_freq = np.diff(phase) * fs / (2 * np.pi)  # in Hz
inst_freq = np.append(inst_freq, inst_freq[-1])  # gleiche Länge wie t

# 6. Symbolentscheidung basierend auf Frequenz
demod_bits = []

for i in range(0, len(inst_freq), samples_per_symbol):
    symbol_freq = np.mean(inst_freq[i:i+samples_per_symbol])
    bit = 1 if symbol_freq > fc else 0
    demod_bits.append(bit)

demod_bits = np.array(demod_bits[:len(data)])

# === Ergebnisse anzeigen ===

plt.figure(figsize=(12, 6))

plt.subplot(3, 1, 1)
plt.plot(t, signal)
plt.title("Empfangenes CFSK-Signal")
plt.xlabel("Zeit [s]")
plt.ylabel("Amplitude")

plt.subplot(3, 1, 2)
plt.plot(t, inst_freq)
plt.title("Instantane Frequenz")
plt.xlabel("Zeit [s]")
plt.ylabel("Frequenz [Hz]")

plt.subplot(3, 1, 3)
plt.step(np.arange(len(data)), data, label="Original")
plt.step(np.arange(len(demod_bits)), demod_bits, linestyle='--', label="Demoduliert")
plt.title("Originale vs. demodulierte Bits")
plt.xlabel("Symbol Index")
plt.ylabel("Bit")
plt.legend()

plt.tight_layout()
plt.show()
