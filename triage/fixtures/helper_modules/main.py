import pandas as pd
from utils import helpers

df = helpers.clean(pd.read_csv("data/d.csv"))
