import matplotlib.pyplot as plt
import scipy.signal as sig
import numpy as np
from math import pi

plt.close('all')

# Filter parameters
N = 20          # Filter order
fc = 1200       # Cutoff frequency (Hz)
Fs = 19020       # Sampling frequency (Hz)

# Normalize the cutoff frequency
w_c = 2 * fc / Fs

# Design the FIR filter using the window method
t = sig.firwin(N, w_c)

# Compute the frequency response
[w, h] = sig.freqz(t, worN = 2000)

# Convert frequency to Hz
w = Fs * w / (2 * pi)

# Convert magnitude to dB
h_db = 20 * np.log10(abs(h))

# Plot the frequency response
plt.figure()
plt.plot(w, h_db)
plt.title('FIR filter response')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.grid(True)

# --- Anwendung des Filters auf ein Signal ---

# 1. FSK-Signal als Eingangssignal erzeugen
bitrate = 1200  # Bitrate [bps]
# Wähle Frequenzen, um den Filter zu testen:
# f_pass liegt im Durchlassbereich (< 1200 Hz)
# f_stop liegt im Sperrbereich (> 1200 Hz)
f_pass = 1000   # Frequenz für Bit '1'
f_stop = 2200   # Frequenz für Bit '0'

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
# sig.lfilter(b, a, x) wendet den Filter an. Für FIR ist a=1.
signal_out = sig.lfilter(t, 1.0, signal_in)

# 3. Ergebnisse plotten

# Plot im Zeitbereich
plt.figure()
plt.plot(t_signal, signal_in, label='Original Signal')
plt.plot(t_signal, signal_out, label='Gefiltertes Signal', linewidth=3)
plt.title('Filterung im Zeitbereich')
plt.xlabel('Zeit (s)')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)

# Plot im Frequenzbereich (FFT)
N_fft = len(signal_in)
freqs = np.fft.rfftfreq(N_fft, 1/Fs)
fft_in = np.abs(np.fft.rfft(signal_in))
fft_out = np.abs(np.fft.rfft(signal_out))

plt.figure()
plt.plot(freqs, fft_in, label='FFT Original')
plt.plot(freqs, fft_out, label='FFT Gefiltert', linewidth=3)
plt.title('Filterung im Frequenzbereich')
plt.xlabel('Frequenz (Hz)')
plt.ylabel('Magnitude')
plt.legend()
plt.grid(True)

plt.show()