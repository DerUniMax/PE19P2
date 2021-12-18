from pomegranate import *
from itertools import product
import pandas
import matplotlib
import os

def parse(dataset: pandas.DataFrame):
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
  test = [{'Zimmerzahl': '5-6 Zimmer', 'Stockwerk': '1.Stock', 'Hausmeister': 'nein'}]
  people_stuff.remove("Kleinfamilie")
  dataset.drop(people_stuff, axis=1)
  print(_calc_prob_distribution(dataset, "Kleinfamilie", []))

def _create_node(series: pandas.Series, name: str) -> Node:
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

def _calc_probabilities(series: pandas.core.series.Series) -> dict:
  counts = series.value_counts()
  full_amount = series.size - 1
  
  probabilities = dict()
  
  for key in counts.keys():
    probabilities[key] = float(counts[key])/float(full_amount) + 0.0
  
  return probabilities

def _calc_prob_distribution(dataset: pandas.DataFrame, target_name: str, exclude):
  working_set = dataset.drop(exclude, axis=1)
  target_options = working_set[target_name].unique()
  
  conditional_table = []
  
  for option in target_options:
    filtered_set = working_set[working_set[target_name] == option]
    # filtered_set = filtered_set.drop(target_name, axis=1)
    conditional_table.append(_assemble_conditional_prob_table_part(filtered_set))
  
  conditional_table = ConditionalProbabilityTable(conditional_table)
  
  return conditional_table

def _evaluate_combinations(column_combinations: [dict], filtered_set):
  print(column_combinations)
  for optional in column_combinations:
    conditions = ""
    for key in optional.keys():
      conditions += f"({key} == \"{optional[key]}\") & "
    
    conditions = conditions.rstrip("& ")
    
    amount = filtered_set.query(conditions).size
    probability = amount/filtered_set.size
    optional["prob"] = probability
    
  return column_combinations

def _assemble_conditional_prob_table_part(filtered_set: pandas.DataFrame):
  column_uniques = dict()
  probabilities = []
  for column in filtered_set.columns:
    column_uniques[column] = filtered_set[column].unique()
  
  combinations = product(*column_uniques)
  
  print(type(combinations))
  
  return _evaluate_combinations(combinations, filtered_set)

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
