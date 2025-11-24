import pandas as pd

df = pd.read_csv("detections.csv")

# Korjataan aikaleimojen erottimet
df["timestamp"] = df["timestamp"].str.replace(":", "-", 2)

# Ylikirjoitetaan alkuperäinen tiedosto
df.to_csv("detections.csv", index=False)

print("Tiedosto korjattu ja ylikirjoitettu.")
