from pgmpy.models import BayesianNetwork
from pgmpy.readwrite import XMLBIFReader
import pandas as pd
import numpy as np

def predict_file(filename: str, predict: pd.DataFrame):
  net = XMLBIFReader(filename).get_model()
  
  predict_net(net, predict)

def predict_net(net: BayesianNetwork, predict: pd.DataFrame):
  predictdfs = _parse_prediction_df(predict)
  
  predictions = []
  
  for predictdf in predictdfs:
    print(predictdf)
    predictions.append(net.predict(predictdf))
  
  return predictions

def _parse_prediction_df(predictdf: pd.DataFrame) -> [pd.DataFrame]:
  dfs = []
  
  for row in predictdf.to_numpy():
    print(row)
    rowdf = pd.DataFrame(row, predictdf.columns)
    
    columns = []
    
    for key in rowdf.iloc[0].keys():
      if type(rowdf.iloc[0][key]) != type("") and math.isnan(rowdf.iloc[0][key]):
        columns.append(key)
    
    rowdf.drop(columns, axis=1)
    
    dfs.append(rowdf)
  
  return dfs