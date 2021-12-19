import pandas as pd
import net_predictor
from pomegranate import bayes
from net_parser_pgmpy import parse
from edgesAndNodes import edges


def __main__():
  dataset = pd.read_csv("./P1_DP13_Wohnungen_X.csv", sep=";")

  net = parse(dataset, edges)
  
  predict_set = pd.read_csv("input.csv", sep=";")
  
  print(net_predictor.predict_file("net.xml", predict_set))

__main__()