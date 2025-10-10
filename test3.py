import numpy as np
import matplotlib.pyplot as plt

phi1 = np.ones(256)


def test1():
    y = []
    t = []
    phase = 0
    for i in range(0, 8):
        y.append(np.sin(2 * np.pi * f0 / fs * i))
        print(2 * np.pi * f0 / fs * i / (2 * np.pi) * 360)
        t.append(i * 1 / 1200)

    plt.plot(t, y)


# Helper: FSK ohne Phasensprung (kontinuierlich)
def fsk_without_phase_jumps(bits, f0, f1, fs, Tb):
    phase = 0
    signal = []
    phi = []
    dt = 0
    for bit in bits:
        f = f1 if bit == 1 else f0
        t_bit = np.arange(0, Tb, 1 / fs)

        for _ in t_bit:
            phase += 2 * np.pi * f * dt
            phi.append(phase)
            dt = 1 / fs
            signal.append(np.sin(phase))
            print()

    return np.array(signal), np.array(phi)


# Parameter
bit_rate = 1200  # Bitrate in bits per second
f0 = 1200  # Frequenz für Bit 0
f1 = 2200  # Frequenz für Bit 1
fs = 9600 # Abtastrate

test1()

# bits = [1, 0, 1, 1, 0, 1, 0, 0]
bits = [0, 1]

N = fs / bit_rate

# sig = np.zeros(int(N))
dt = 1 / fs
t = np.arange(0, 2 / bit_rate, dt)

y_cont, phi1 = fsk_without_phase_jumps(bits, f0, f1, fs, 1 / bit_rate)


# Plotten
plt.figure(figsize=(12, 6))


plt.subplot(2, 1, 1)
plt.title("FSK ohne Phasensprünge")
# plt.plot(t, y_cont*60, t, phi1)
plt.plot(t, y_cont)
plt.xticks(np.arange(0, 8 / (bit_rate), 1 / bit_rate))
plt.grid(True)
plt.show()
print("stop")
