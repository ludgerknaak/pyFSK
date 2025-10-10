# %%
import matplotlib.pyplot as plt

# Parameter
fs = 19200  # Abtastrate
f1 = 1200  # Frequenz für logische 0
f2 = 2200  # Frequenz für logische 1
bitrate = 1200  # Bitrate
A = 1.0  # Amplitude

# Beispiel-Daten: 0 1 0 1 1 0
data = [0, 1]

# Samples pro Bit
samples_per_bit = fs // bitrate

# Zeitvektor und Frequenzvektor aufbauen
import numpy as np

f_t = []
for bit in data:
    f = f1 if bit == 0 else f2
    f_t.extend([f] * samples_per_bit)

f_t = np.array(f_t)

# Phasenakkumulation
dt = 1 / fs
phi = 2 * np.pi * np.cumsum(f_t) * dt

# %%
# test
test = np.cumsum(f_t)
# Signal erzeugen
s = A * np.sin(phi)

plt.plot(s)
plt.show()

# %%
import numpy as np
import matplotlib.pyplot as plt

# Parameter
fs = 19200  # Abtastrate [Hz]
f1 = 1200  # Frequenz für logische 0 [Hz]
f2 = 2200  # Frequenz für logische 1 [Hz]
bitrate = 1200  # Bitrate [bps]
A = 1.0  # Amplitude

# Beispiel-Daten: 0 1 0 1 1 0
data = [0, 1, 0, 1, 1, 0]

# Abgeleitete Werte
samples_per_bit = fs // bitrate
total_samples = samples_per_bit * len(data)

# Frequenz über die Zeit aufbauen
f_t = np.zeros(total_samples)

for i, bit in enumerate(data):
    freq = f1 if bit == 0 else f2
    f_t[i * samples_per_bit : (i + 1) * samples_per_bit] = freq

# Zeitachse
t = np.arange(total_samples) / fs

# Phase berechnen (phasenkontinuierlich!)
dt = 1 / fs
phi = 2 * np.pi * np.cumsum(f_t) * dt

# FSK-Signal erzeugen
s = A * np.sin(phi)

# Plotten
plt.figure(figsize=(12, 4))
plt.plot(t, s, label="FSK Signal")
plt.title("Phasenkontinuierliches FSK Signal")
plt.xlabel("Zeit [s]")
plt.ylabel("Amplitude")
plt.grid(True)
plt.tight_layout()
plt.show()

# %%
