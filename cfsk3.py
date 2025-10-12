import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

# CFSK-Modulation hier stimmt etwas nicht
def cfsk_modulate(bits, f0, f1, sample_rate, symbol_duration):
    t = np.linspace(0, symbol_duration, int(sample_rate * symbol_duration), endpoint=False)
    signal = np.concatenate([
        np.sin(2 * np.pi * (f0 if bit == 0 else f1) * t)
        for bit in bits
    ])
    return signal

# 🔧 Parameter
sample_rate = 19200      # Hz
symbol_duration = 1/1200    # Sekunden, Bitdauer
f0 = 1200                # Hz für Bit 0
f1 = 2200                # Hz für Bit 1
#bits = [0,0,1,1,1,0,0,1]
bits = [1,1,1,0,0,1,1,0]

# 🔄 Modulation
mod_signal = cfsk_modulate(bits, f0, f1, sample_rate, symbol_duration)

# 📊 Input-Signal plotten
time = np.linspace(0, len(mod_signal)/sample_rate, len(mod_signal), endpoint=False)
plt.figure(figsize=(12, 3))
plt.plot(time, mod_signal)

# Ticks auf der x-Achse in 1/1200er Schritten setzen
# np.arange(start, stop, step) erzeugt die gewünschten Werte
plt.xticks(np.arange(0, 9*symbol_duration, symbol_duration))

plt.title("CFSK-Moduliertes Signal")
plt.xlabel("Zeit [s]")
plt.ylabel("Amplitude")
plt.grid(True)
plt.tight_layout()
plt.show()