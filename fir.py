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

# 1. Testsignal erzeugen
# Das Signal besteht aus zwei Frequenzen: 500 Hz (unter fc) und 2000 Hz (über fc)
f1 = 500
f2 = 2000
t_signal = np.arange(0, 0.1, 1/Fs) # 100ms Signal
signal_in = np.sin(2 * pi * f1 * t_signal) + 0.5 * np.sin(2 * pi * f2 * t_signal)

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