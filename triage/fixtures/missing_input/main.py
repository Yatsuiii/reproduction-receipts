import pandas as pd
df = pd.read_csv("data/raw_prices.csv")
df.to_csv("out.csv")
