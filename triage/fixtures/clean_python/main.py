import os
import numpy as np
import pandas as pd

df = pd.read_csv("data/input.csv")
os.makedirs("output", exist_ok=True)
df.assign(z=np.log(df["x"])).to_csv("output/table1.csv", index=False)
