import pandas as pd
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
  
  bbn = Factory.from_data(structure, dataset)
  
  # This function helps to calculate probability distribution, which goes into BBN (note, can handle up to 2 parents)
  # def probs(data, child, parent1=None, parent2=None):
  #     if parent1==None:
  #         # Calculate probabilities
  #         prob=pd.crosstab(data[child], 'Empty', margins=False, normalize='columns').sort_index().to_numpy().reshape(-1).tolist()
  #     elif parent1!=None:
  #             # Check if child node has 1 parent or 2 parents
  #             if parent2==None:
  #                 # Caclucate probabilities
  #                 prob=pd.crosstab(data[parent1],data[child], margins=False, normalize='index').sort_index().to_numpy().reshape(-1).tolist()
  #             else:
  #                 # Caclucate probabilities
  #                 prob=pd.crosstab([data[parent1],data[parent2]],data[child], margins=False, normalize='index').sort_index().to_numpy().reshape(-1).tolist()
  #     else: print("Error in Probability Frequency Calculations")
  #     return prob
  
  # Miete = BbnNode(Variable(0, 'Miete', list(dataset["Miete"].unique())), probs(dataset, child='Miete'))
  # Kaution = BbnNode(Variable(1, 'Kaution', list(dataset["Kaution"].unique())), probs(dataset, child='Kaution'))
  # Nebenkosten = BbnNode(Variable(2, 'Nebenkosten', list(dataset["Nebenkosten"].unique())), probs(dataset, child='Nebenkosten'))
  # Studierende = BbnNode(Variable(3, 'Studierende', list(dataset["Studierende"].unique())), probs(dataset, child='Studierende', parent1="Miete", parent2="Kaution"))

  # bbn = bbn.add_node(Miete) \
  #   .add_node(Kaution) \
  #   .add_node(Studierende) \
  #   .add_edge(Edge(Miete, Studierende, EdgeType.DIRECTED)) \
  #   .add_edge(Edge(Kaution, Studierende, EdgeType.DIRECTED)) \
    # .add_node(Nebenkosten) \
    # .add_edge(Edge(Nebenkosten, Studierende, EdgeType.DIRECTED)) \

  # Zimmerzahl = BbnNode(Variable(0, 'Zimmerzahl', ['5-6 Zimmer', '3-4 Zimmer', 'Zwei Zimmer', 'Ein Zimmer', '4 Zimmer', '3 Zimmer', '2-3 Zimmer']), probs(dataset, child='Zimmerzahl'))
  # Hausmeister = BbnNode(Variable(1, 'Hausmeister', ['ja', 'nein']), probs(dataset, child='Hausmeister'))
  # Kleinfamilie = BbnNode(Variable(2, 'Kleinfamilie', ['ja', 'nein']), probs(dataset, child='Kleinfamilie', parent1='Zimmerzahl', parent2='Hausmeister'))

  # # Create Network
  # bbn = Bbn() \
  #     .add_node(Zimmerzahl) \
  #     .add_node(Hausmeister) \
  #     .add_node(Kleinfamilie) \
  #     .add_edge(Edge(Zimmerzahl, Kleinfamilie, EdgeType.DIRECTED)) \
  #     .add_edge(Edge(Hausmeister, Kleinfamilie, EdgeType.DIRECTED)) \

  join_tree = InferenceController.apply(bbn)
  
  # Define a function for printing marginal probabilities
  def print_probs(join_tree):
      for node in join_tree.get_bbn_nodes():
          potential = join_tree.get_bbn_potential(node)
          print("Node:", node)
          print("Values:")
          print(potential)
          print('----------------')

  # Use the above function to print marginal probabilities
  print_probs(join_tree)