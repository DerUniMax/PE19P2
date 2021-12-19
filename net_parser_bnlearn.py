from edgesAndNodes import edges, nodes
import bnlearn
import pandas as pd

# Import example dataset
df = pd.read_csv('P1_DP13_Wohnungen_X.csv', encoding='utf-8', delimiter=';')
# print(df)

# Make the actual Bayesian DAG
DAG = bnlearn.make_DAG(edges)

# Plot the DAG as interactive plot
# bnlearn.plot(DAG, interactive=True)

# learn the parameter
# DAG = bnlearn.parameter_learning.fit(DAG, df)

bayesian_net = bnlearn.to_bayesianmodel(DAG)

print(bayesian_net.fit(df))

bnlearn.pgmpy.readwrite.BIFWriter(bayesian_net).write_bif(filename="net.bif")

# Print the learned CPDs
# bnlearn.print_CPD(DAG)

# bnlearn.save(DAG, filepath='oh_god_please_dont_crash', overwrite=True)
