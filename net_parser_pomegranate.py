from pomegranate import *
from itertools import product
import pandas as pd
import matplotlib
import os

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
  
  def probs(data, child, parents=[]):
      if len(parents) == 0:
        # Calculate probabilities
        prob=pd.crosstab(data[child], 'Empty', margins=False, normalize='columns').sort_index().to_numpy().reshape(-1).tolist()
      elif len(parents) > 0:
        print([data[parent] for parent in parents])
        print([data[parents[0]], data[parents[1]]])
        
        prob=pd.crosstab([data[parents[0]], data[parents[1]]], data[child], margins=False, normalize='index').sort_index().to_numpy().reshape(-1).tolist()
        
      else: print("Error in Probability Frequency Calculations")
      return prob
  
  net = BayesianNetwork("Wohnungen")
  
  Kleinfamilie = Node(DiscreteDistribution(probs(dataset, child='Kleinfamilie', parents=['Zimmerzahl', 'Kindergarten'])), name="Kleinfamilie")
  Zimmerzahl = Node(DiscreteDistribution(probs(dataset, "Zimmerzahl")), name="Zimmerzahl")
  Kindergarten = Node(DiscreteDistribution(probs(dataset, "Kindergarten"), name="Kindergarten"))
  
  net.add_nodes(Kleinfamilie, Zimmerzahl, Kindergarten)
  net.add_edge(Zimmerzahl, Kleinfamilie)
  net.add_edge(Kindergarten, Kleinfamilie)
  
  net.bake()
  
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

def _calc_probabilities(series: pd.core.series.Series) -> dict:
  counts = series.value_counts()
  full_amount = series.size - 1
  
  probabilities = dict()
  
  for key in counts.keys():
    probabilities[key] = float(counts[key])/float(full_amount) + 0.0
  
  return probabilities

def _calc_prob_distribution(dataset: pd.DataFrame, target_name: str, exclude):
  working_set = dataset.drop(exclude, axis=1)
  target_options = working_set[target_name].unique()
  
  conditional_table = []
  
  for option in target_options:
    filtered_set = working_set[working_set[target_name] == option]
    # filtered_set = filtered_set.drop(target_name, axis=1)
    conditional_table.append(_assemble_conditional_prob_table_part(filtered_set))
  
  conditional_table = ConditionalProbabilityTable(conditional_table)
  
  return conditional_table

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

def _assemble_conditional_prob_table_part(filtered_set: pd.DataFrame):
  column_uniques = dict()
  
  for column in filtered_set.columns:
    column_uniques[column] = filtered_set[column].unique()
  
  combinations = product(*column_uniques.values())
  keys = list(column_uniques.keys())
  
  return _evaluate_combinations(combinations, keys, filtered_set)

# def _generate_combinations(columns: dict):
#   for options in columns:
#     for options[1]

def _check_probabilities(probabilities: dict) -> bool:
  overall_prob = 0
  for key in probabilities.keys():
    overall_prob += probabilities[key]
  
  return bool(overall_prob == 1)

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
