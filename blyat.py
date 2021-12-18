import bnlearn
import pandas as pd
import math

dag = bnlearn.load(filepath="oh_god_please_dont_crash.pkl")

df = pd.read_csv("input.csv", sep=';')

columns = []

for key in df.iloc[0].keys():
  if type(df.iloc[0][key]) != type("") and math.isnan(df.iloc[0][key]):
    columns.append(key)

print(columns)

prediction = bnlearn.predict(dag, df, columns)

print(prediction.head())