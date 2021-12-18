import pandas as pd
from itertools import product
from pybbn.graph.factory import Factory
from pybbn.graph.dag import Bbn
from pybbn.graph.edge import Edge, EdgeType
from pybbn.graph.jointree import EvidenceBuilder
from pybbn.graph.node import BbnNode
from pybbn.graph.variable import Variable
from pybbn.pptc.inferencecontroller import InferenceController

def parse(dataset: pd.DataFrame):
  structure = {
    "Miete": [],
    "Kaution": [],
    "Hausmeister": [],
    "Nebenkosten": ["Hausmeister"],
    "Kehrwoche": ["Hausmeister"],
    "Studierende": ["Miete", "Kaution", "Nebenkosten"]
  }
  
  # dataset = dataset.drop(dataset.columns.difference(["Miete", "Kaution", "Hausmeister", "Nebenkosten", "Kehrwoche", "Studierende"]), axis=1)
  # print(dataset.head())
  # bbn = Factory.from_data(structure, dataset)
  
  # This function helps to calculate probability distribution, which goes into BBN (note, can handle up to 2 parents)
  def probs(data, child, parents=[]):
    if len(parents) == 0:
      # Calculate probabilities
      prob=pd.crosstab(data[child], 'Empty', margins=False, normalize='columns').sort_index().to_numpy().reshape(-1).tolist()
    elif len(parents) > 0:
      prob = []
      child_uniqes = data[child].unique()
      uniques = [data[parent].unique() for parent in parents]
      
      for val in child_uniqes:
        work_data = data[data[child] == val]
      
        for unique in product(*uniques):
          conditions = ""
          for i in range(len(parents)):
            conditions += f"({parents[i]} == \"{unique[i]}\") & "
          
          conditions = conditions.rstrip("& ")
          
          amount = work_data.query(conditions).size
          
          probability = amount/work_data.size
          prob.append(probability)
      
      # prob=pd.crosstab([data[parent] for parent in parents], data[child], margins=False, normalize='index').sort_index().to_numpy().reshape(-1).tolist()
      
    else: print("Error in Probability Frequency Calculations")
    return prob

  Zimmerzahl = BbnNode(Variable(0, 'Zimmerzahl', dataset["Zimmerzahl"].unique()), probs(dataset, child='Zimmerzahl'))
  Kaution = BbnNode(Variable(1, 'Kaution', dataset["Kaution"].unique()), probs(dataset, child='Kaution'))
  Hausmeister = BbnNode(Variable(2, 'Hausmeister', dataset["Hausmeister"].unique()), probs(dataset, child='Hausmeister'))
  Nebenkosten = BbnNode(Variable(3, 'Nebenkosten', dataset["Nebenkosten"].unique()), probs(dataset, child='Nebenkosten'))
  Kindergarten = BbnNode(Variable(4, 'Kindergarten', dataset["Kindergarten"].unique()), probs(dataset, child='Kindergarten'))
  Kleinfamilie = BbnNode(Variable(5, 'Kleinfamilie', dataset["Kleinfamilie"].uniqe()), probs(dataset, child='Kleinfamilie', parents=['Zimmerzahl', 'Kindergarten', 'Kaution', 'Hausmeister', 'Nebenkosten']))

  # Create Network
  bbn = Bbn() \
      .add_node(Zimmerzahl) \
      .add_node(Hausmeister) \
      .add_node(Kleinfamilie) \
      .add_node(Kaution) \
      .add_node(Kindergarten) \
      .add_node(Nebenkosten) \
      .add_edge(Edge(Zimmerzahl, Kleinfamilie, EdgeType.DIRECTED)) \
      .add_edge(Edge(Kindergarten, Kleinfamilie, EdgeType.DIRECTED)) \
      .add_edge(Edge(Hausmeister, Kleinfamilie, EdgeType.DIRECTED)) \
      .add_edge(Edge(Kaution, Kleinfamilie, EdgeType.DIRECTED)) \
      .add_edge(Edge(Nebenkosten, Kleinfamilie, EdgeType.DIRECTED)) \

  # print(bbn)

  join_tree = InferenceController.apply(bbn)
  
  def print_probs(join_tree):
      for node in join_tree.get_bbn_nodes():
          potential = join_tree.get_bbn_potential(node)
          print("Node:", node)
          print("Values:")
          print(potential)
          print('----------------')

  
  
  # Use the above function to print marginal probabilities
  print_probs(join_tree)