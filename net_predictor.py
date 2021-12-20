from pgmpy.models import BayesianNetwork

from pgmpy.factors.discrete import TabularCPD
import pandas as pd

import math

import json


def predict_file(filename: str, predict: pd.DataFrame):

  net = _parse_json(filename)
  
  return predict_net(net, predict)


def predict_net(net: BayesianNetwork, predict: pd.DataFrame):
  predictdfs = _parse_prediction_df(predict)
  
  predictions = []
  
  for predictdf in predictdfs:
    predictions.append(net.predict(predictdf))
  
  return predictions


def _parse_prediction_df(predictdf: pd.DataFrame) -> [pd.DataFrame]:
  dfs = []
  
  for row in predictdf.to_numpy():

    rowdf = pd.DataFrame([row], columns=predictdf.columns)
    
    columns = []
    
    for key in rowdf.iloc[0].keys():
      if type(rowdf.iloc[0][key]) != type("") and math.isnan(rowdf.iloc[0][key]):
        columns.append(key)
    
    rowdf = rowdf.drop(columns, axis=1)
    
    dfs.append(rowdf)
  
  return dfs


def _parse_json(filename: str):
  with open(filename, "r") as file:
    save_obj = json.load(file)
  
  net = BayesianNetwork([(edge[0], edge[1]) for edge in save_obj['edges']])

  for node in save_obj['nodes']:
    net.add_node(node)
  
  for cpd in save_obj['cpds']:
    net.add_cpds(_create_cpd(cpd))
  
  # print the read cpds (takes a long time)
  # for cpd in net.get_cpds():
  #   print(cpd)
  
  return net

def _create_cpd(cpd_dict: dict) -> TabularCPD:
  evidence_card = []
  for evidence in cpd_dict['evidence']:
    evidence_card.append(len(cpd_dict['state_names'][evidence]))
  
  return TabularCPD(variable=cpd_dict['variable'], variable_card=cpd_dict['variable_card'], evidence=cpd_dict['evidence'], evidence_card=evidence_card, state_names=cpd_dict['state_names'], values=cpd_dict['values'])

