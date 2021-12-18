import pandas as pd
from pomegranate import bayes
from net_parser_pybbn import parse



def __main__():
  dataset = pd.read_csv("./P1_DP13_Wohnungen_X.csv", sep=";")

  net = parse(dataset)
  
  

__main__()