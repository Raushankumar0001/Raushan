import numpy as np
import matplotlib.pyplot as plt

# Define the data stream
data = [1, 1, 1, 1, 0, 0, 0, 1, 1, 1]
bit_duration = 1  # duration of one bit in seconds
fs = 1000  # sampling frequency
t = np.linspace(0, bit_duration, int(fs * bit_duration), endpoint=False)

# BPSK Parameters
fc_bpsk = 10  # carrier frequency for BPSK

# BFSK Parameters
fc0 = 5   # frequency for binary 0
fc1 = 15  # frequency for binary 1

# Generate BPSK signal
bpsk_signal = np.array([])
for bit in data:
    if bit == 1:
        bpsk_signal = np.concatenate((bpsk_signal, np.cos(2 * np.pi * fc_bpsk * t)))
    else:
        bpsk_signal = np.concatenate((bpsk_signal, -np.cos(2 * np.pi * fc_bpsk * t)))

# Generate BFSK signal
bfsk_signal = np.array([])
for bit in data:
    if bit == 1:
        bfsk_signal = np.concatenate((bfsk_signal, np.cos(2 * np.pi * fc1 * t)))
    else:
        bfsk_signal = np.concatenate((bfsk_signal, np.cos(2 * np.pi * fc0 * t)))

# Time vector for plotting
time_vector = np.linspace(0, bit_duration * len(data), len(data) * len(t), endpoint=False)

# Plotting
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(time_vector, bpsk_signal)
plt.title("BPSK Signal for Data Stream 1111000111")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")

plt.subplot(2, 1, 2)
plt.plot(time_vector, bfsk_signal)
plt.title("BFSK Signal for Data Stream 1111000111")
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")

plt.tight_layout()
plt.show()