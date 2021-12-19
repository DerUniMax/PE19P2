from edgesAndNodes import edges, nodes
import pandas as pd
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import BayesianEstimator
import networkx as nx
import matplotlib.pyplot as plt
from pgmpy.estimators import MaximumLikelihoodEstimator

df = pd.read_csv("P1_DP13_Wohnungen_X.csv", sep=";")

net = BayesianNetwork(edges)

# net.fit(df, n_jobs=10)
# print(net)

estimator = BayesianEstimator(net, df)

# schnell für alle, falsche estimates, immer gleich 50%
for node in nodes:
	CPD = estimator.estimate_cpd(node, prior_type='BDeu')
	print(CPD)

# braucht allein für die Kleinfamilie ewig
# likelihood = MaximumLikelihoodEstimator(net, df).estimate_cpd('Kleinfamilie')
# print(likelihood)

nx.draw_kamada_kawai(net, with_labels=True)
plt.show()
