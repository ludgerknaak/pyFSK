import matplotlib.pyplot as plt
import scipy.signal as sig
import numpy as np
from math import pi

plt.close("all")

# Filter parameters
N = 3  # Filter order
fc = 1300  # Cutoff frequency (Hz)
Fs = 19200  # Sampling frequency (Hz)

# Normalize the cutoff frequency
w_c = 2 * fc / Fs

# Design the IIR filter (Butterworth, 3rd order)
b, a = sig.iirfilter(N, w_c, btype="low", ftype="butter")

# Compute the frequency response
[w, h] = sig.freqz(b, a, worN=2000)

# Convert frequency to Hz
w = Fs * w / (2 * pi)

# Convert magnitude to dB
h_db = 20 * np.log10(abs(h))

# Plot the frequency response
plt.figure()
plt.plot(w, h_db)
plt.title("IIR Filter Response (Butterworth, 3. Ordnung)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (dB)")
plt.grid(True)

# --- Anwendung des Filters auf ein Signal ---

# 1. FSK-Signal als Eingangssignal erzeugen
bitrate = 1200  # Bitrate [bps]
# Wähle Frequenzen, um den Filter zu testen:
# f_pass liegt im Durchlassbereich (< 1200 Hz)
# f_stop liegt im Sperrbereich (> 1200 Hz)
f_pass = 1200  # Frequenz für Bit '1'
f_stop = 2200  # Frequenz für Bit '0'

# Beispiel-Bitsequenz
data = [1, 1, 0, 0, 1, 0, 1, 1, 0]

# Samples pro Bit und Gesamtzahl der Samples berechnen
samples_per_bit = Fs // bitrate
total_samples = samples_per_bit * len(data)

# Frequenzverlauf über die Zeit erstellen
f_t = np.zeros(total_samples)
for i, bit in enumerate(data):
    freq = f_pass if bit == 1 else f_stop
    f_t[i * samples_per_bit : (i + 1) * samples_per_bit] = freq

# Zeitachse für das Signal
t_signal = np.arange(total_samples) / Fs

# Phasenkontinuierliches FSK-Signal durch Phasenakkumulation erzeugen
phi = 2 * pi * np.cumsum(f_t) * (1 / Fs)
signal_in = np.sin(phi)

# 2. Filter anwenden
# sig.lfilter(b, a, x) wendet den IIR-Filter an.
signal_out = sig.lfilter(b, a, signal_in)

# 3. Ergebnisse plotten

# Plot im Zeitbereich
plt.figure()
plt.plot(t_signal, signal_in, label="Original Signal")
plt.plot(t_signal, signal_out, label="Gefiltertes Signal", linewidth=3)
plt.title("Filterung im Zeitbereich")
plt.xlabel("Zeit (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)

# Plot im Frequenzbereich (FFT)
N_fft = len(signal_in)
freqs = np.fft.rfftfreq(N_fft, 1 / Fs)
fft_in = np.abs(np.fft.rfft(signal_in))
fft_out = np.abs(np.fft.rfft(signal_out))

plt.figure()
plt.plot(freqs, fft_in, label="FFT Original")
plt.plot(freqs, fft_out, label="FFT Gefiltert", linewidth=3)
plt.title("Filterung im Frequenzbereich")
plt.xlabel("Frequenz (Hz)")
plt.ylabel("Magnitude")
plt.legend()
plt.grid(True)

# --- 4. Signal dekodieren ---
decoded_bits = []
energy_levels = []  # Zum Visualisieren der Energie pro Bit

# Wir gehen das gefilterte Signal in "Bit-Stücken" durch
for i in range(len(data)):
    # Signal-Abschnitt für das aktuelle Bit extrahieren
    start_index = i * samples_per_bit
    end_index = (i + 1) * samples_per_bit
    chunk = signal_out[start_index:end_index]

    # Energie des Abschnitts berechnen (mittlere absolute Amplitude ist hier ausreichend)
    energy = np.mean(np.abs(chunk))
    energy_levels.append(energy)

    # Entscheidung treffen: Wenn Energie über einem Schwellenwert liegt -> Bit 1, sonst 0
    # Der Schwellenwert 0.1 ist hier empirisch gewählt und liegt zwischen den erwarteten Energien.
    if energy > 0.3:
        decoded_bits.append(1)
    else:
        decoded_bits.append(0)

print(f"Originale Bitsequenz:  {data}")
print(f"Dekodierte Bitsequenz: {decoded_bits}")

errors = np.sum(np.array(data) != np.array(decoded_bits))
print(f"Anzahl der Bitfehler: {errors}")

plt.show()
