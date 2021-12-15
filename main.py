import pandas as pd
from net_parser import parse



def __main__():
  dataset = pd.read_csv("./P1_DP13_Wohnungen_X.csv", sep=";")

  print(dataset.head())

  net = parse(dataset)

__main__()