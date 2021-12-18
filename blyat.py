import bnlearn
import pandas as pd

dag = bnlearn.load(filepath="oh_god_please_dont_crash.pkl")

df = pd.read_csv("input.csv", sep=';')

prediction = bnlearn.predict(dag, df, ["Studierende", "Kleinfamilie", "SingleHighIncome", "DINK", "Expatriate", "Rentnerpaar"])

print(prediction)