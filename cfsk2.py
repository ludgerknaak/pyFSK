import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

# Bandpass-Filter
def bandpass_filter(signal, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, signal)

# CFSK-Modulation
def cfsk_modulate(bits, f0, f1, sample_rate, symbol_duration):
    t = np.linspace(0, symbol_duration, int(sample_rate * symbol_duration), endpoint=False)
    signal = np.concatenate([
        np.sin(2 * np.pi * (f0 if bit == 0 else f1) * t)
        for bit in bits
    ])
    return signal

# CFSK-Demodulation (ohne Symbolvisualisierung)
def cfsk_demodulate(signal, f0, f1, sample_rate, symbol_duration):
    samples_per_symbol = int(symbol_duration * sample_rate)
    num_symbols = len(signal) // samples_per_symbol
    bits = []

    for i in range(num_symbols):
        symbol = signal[i*samples_per_symbol:(i+1)*samples_per_symbol]

        # Energie im Band um f0
        s0 = bandpass_filter(symbol, f0 - 50, f0 + 50, sample_rate)
        e0 = np.sum(s0**2)

        # Energie im Band um f1
        s1 = bandpass_filter(symbol, f1 - 50, f1 + 50, sample_rate)
        e1 = np.sum(s1**2)

        bit = 0 if e0 > e1 else 1
        bits.append(bit)

    return bits

# 🔧 Parameter
sample_rate = 19200      # Hz
symbol_duration = 1/1200    # Sekunden
f0 = 1200                # Hz für Bit 0
f1 = 2200                # Hz für Bit 1
bits = [0]

# 🔄 Modulation
mod_signal = cfsk_modulate(bits, f0, f1, sample_rate, symbol_duration)

# 📊 Input-Signal plotten
time = np.linspace(0, len(mod_signal)/sample_rate, len(mod_signal), endpoint=False)
plt.figure(figsize=(12, 3))
plt.stem(time, mod_signal)
plt.title("CFSK-Moduliertes Signal")
plt.xlabel("Zeit [s]")
plt.ylabel("Amplitude")
plt.grid(True)
plt.tight_layout()
plt.show()

# 🔁 Demodulation
recovered_bits = cfsk_demodulate(mod_signal, f0, f1, sample_rate, symbol_duration)

# 🖨️ Ergebnisse
print("Gesendete Bits:  ", bits)
print("Demodulierte Bits:", recovered_bits)
