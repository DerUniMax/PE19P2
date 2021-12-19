from pomegranate import *
from itertools import product
import pandas as pd
import matplotlib
import os

# DEPRECATED

def parse(dataset: pd.DataFrame):
  people_stuff = ["Kleinfamilie", "DINK", "Alter", "SingleHighIncome", "Expatriate", "Rentnerpaar", "Studierende"]
  
  # nodes = dict()
  
  # for column in dataset.columns:
  #   nodes[column] = (_create_node(dataset[column], column))
  
  # network = BayesianNetwork("Wohnungen")
  # network.add_nodes(*nodes.values())
  
  # for node_name in nodes.keys():
  #   if node_name in people_stuff:
  #     continue
    
  #   for people in people_stuff:
  #     network.add_edge(nodes[node_name], nodes[people])
  
  # # _add_custom_edges(network, nodes)
  
  # network.bake()
  
  # file = open("net", "w")
  # file.write(network.to_json())
  # file.close()
  
  # network.plot("plot.pdf")
  
  # return network
  # test = [{'Zimmerzahl': '5-6 Zimmer', 'Stockwerk': '1.Stock', 'Hausmeister': 'nein'}]
  # people_stuff.remove("Kleinfamilie")
  # dataset = dataset.drop(people_stuff, axis=1)
  # dataset = dataset.drop(["S-Bahn", "Hausmeister", "Stockwerk", ""], axis=1)
  # dataset = dataset[dataset["Kleinfamilie"] == "ja"]
  # print(_calc_prob_distribution(dataset, "Kleinfamilie", []))
  
  net = BayesianNetwork("Wohnungen")
  
  Kleinfamilie = _create_node_stub(dataset, "Kleinfamilie")
  Zimmerzahl = _create_node_stub(dataset, "Zimmerzahl")
  # Kleinfamilie = _create_node(dataset, "Kleinfamilie", parents=["Zimmerzahl"])
  
  net.add_nodes(Kleinfamilie, Zimmerzahl)
  # net.add_edge(Zimmerzahl, Kleinfamilie)
  # net.add_edge(Kindergarten, Kleinfamilie)
  
  print(net)
  
  net.bake()
  
  print("baked")
  
  net = net.fit(dataset.drop(dataset.columns.difference(["Kleinfamilie", "Zimmerzahl"]), axis=1))
  # fit(net, dataset)
  
  print(net)

def _create_node(series: pd.Series, name: str) -> Node:
  counts = series.value_counts()
  full_amount = series.size - 1
  
  probabilities = dict()
  
  for key in counts.keys():
    probabilities[key] = float(counts[key])/float(full_amount) + 0.0
  
  no_error = _check_probabilities(probabilities)
  
  if not no_error:
    print("Calculation inaccuracy in: ", name)
  
  # probabilities = DiscreteDistribution(probabilities)
  
  return Node(DiscreteDistribution(probabilities), name=name)

def _evaluate_combinations(column_combinations: [tuple], column_names, filtered_set):
  print("oh ffs")
  ret = []
  for optional in column_combinations:
    conditions = ""
    for i in range(len(column_names)):
      conditions += f"({column_names[i]} == \"{optional[i]}\") & "
    
    conditions = conditions.rstrip("& ")
    
    amount = filtered_set.query(conditions).size
    probability = amount/filtered_set.size
    opt_list = list(optional)
    opt_list.append(probability)
    ret.append(opt_list)
    if probability > 0.0:
      print(opt_list)
  
  return ret

def _assemble_conditional_prob_table(filtered_set: pd.DataFrame, name: str, parents: [dict]):
  column_uniques = dict()
  
  for column in filtered_set.columns:
    column_uniques[column] = filtered_set[column].unique()
  
  combinations = []
  
  for parent in parent_probs:
    combination = []
    for key in parent["Probs"].keys():
      combination.append(key)
    combinations.append(combination)
  
  combinations = product(*column_uniques.values())
  keys = list(column_uniques.keys())
  
  evaluated = _evaluate_combinations(combinations, keys, filtered_set)
  
  return ConditionalProbabilityTable(evaluated, parent_probs)

def _create_node(df: pd.DataFrame, name: str, parents = [dict]):
  print("Creating node: ", name)
  drop_list = []
  
  for parent in parents:
    drop_list.append(parent['Name'])
  
  # drop_list.append(name)
  filtered_set = df.drop(df.columns.difference(drop_list), axis=1)
  
  distribution = _assemble_conditional_prob_table(filtered_set, name, parents)
  
  return Node(distribution, name=name)

def _create_node_stub(df: pd.DataFrame, name, parents=[]):
  keys = df[name].unique()
  
  prob_dist = dict()
  
  for key in keys:
    prob_dist[key] = 0
  
  return Node(DiscreteDistribution(prob_dist), name=name)

def _add_custom_edges(network: BayesianNetwork, nodes: dict):
  network.add_edge(nodes["DINK"], nodes["Rentnerpaar"])
  network.add_edge(nodes["Alter"], nodes["Rentnerpaar"])
  network.add_edge(nodes["Alter"], nodes["Studierende"])
  network.add_edge(nodes["SingleHighIncome"], nodes["Studierende"])
  network.add_edge(nodes["Miete"], nodes["Kaution"])
  network.add_edge(nodes["S-Bahn"], nodes["Miete"])
  network.add_edge(nodes["Garage"], nodes["Miete"])
  network.add_edge(nodes["Lage"], nodes["Miete"])
  network.add_edge(nodes["Terrasse"], nodes["Miete"])
  network.add_edge(nodes["Stockwerk"], nodes["Miete"])
  network.add_edge(nodes["Bad"], nodes["Miete"])
  network.add_edge(nodes["Kueche"], nodes["Miete"])
  network.add_edge(nodes["Quadratmeter"], nodes["Miete"])
  network.add_edge(nodes["Zimmerzahl"], nodes["Miete"])
  network.add_edge(nodes["Aufzug"], nodes["Miete"])
  network.add_edge(nodes["Balkon"], nodes["Miete"])
  network.add_edge(nodes["Hausmeister"], nodes["Kehrwoche"])
  network.add_edge(nodes["Hausmeister"], nodes["Nebenkosten"])
  network.add_edge(nodes["Quadratmeter"], nodes["Zimmerzahl"])
  network.add_edge(nodes["Stockwerk"], nodes["Terrasse"])
  network.add_edge(nodes["Balkon"], nodes["Terrasse"])
