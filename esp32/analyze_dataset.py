import pandas as pd
import matplotlib.pyplot as plt

# Завантаження CSV
df = pd.read_csv(r"C:\Users\zenas\Desktop\Me\Applied ML Methods on an ECU in MicroPython (ESP32)\esp32\touch_dataset_example.csv")


# Розділимо по класам
classes = {0: "noise", 1: "short", 2: "valid"}
for label in df['label'].unique():
    sample = df[df['label'] == label].iloc[0, :-1].values
    plt.plot(sample, label=classes[label])

plt.title("Examples of signals by class")
plt.xlabel("Time (sample index)")
plt.ylabel("Signal (value)")
plt.legend()
plt.grid(True)
plt.show()
