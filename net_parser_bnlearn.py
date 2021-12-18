import bnlearn
import pandas as pd # for data manipulation

# Import example dataset
df= pd.read_csv('P1_DP13_Wohnungen_X.csv', encoding='utf-8', delimiter=';')
print(df)


# Define the network structure
edges = [('Quadratmeter', 'Zimmerzahl'),
        ('Quadratmeter', 'Miete'),
        ('Garage', 'Miete'),
        ('Stockwerk', 'Aufzug'),
        ('Stockwerk', 'Terrasse'),
        ('Alter', 'Kueche'),
        ('Alter', 'Stockwerk'),
        ('Balkon', 'Terrasse'),
        ('Lage', 'S-Bahn'),
        ('Lage', 'Entfernung'),
        ('Lage', 'Kindergarten'),
        ('Lage', 'Schule'),
        ('Miete', 'Kaution'),
        ('Kueche', 'Kaution'),
        ('Hausmeister', 'Nebenkosten'),
        ('Hausmeister', 'Kehrwoche'),
        ('Nebenkosten', 'Kleinfamilie'),
        ('Zimmerzahl', 'Kleinfamilie'),
        ('Kaution', 'Kleinfamilie'),
        ('Miete', 'Kleinfamilie'),
        ('Bad', 'Kleinfamilie'),
        ('Kueche', 'Kleinfamilie'),
        ('Kindergarten', 'Kleinfamilie'),
        ('Schule', 'Kleinfamilie'),
        ('Miete', 'Studierende'),
        ('Kaution', 'Studierende'),
        ('Nebenkosten', 'Studierende'),
        ('Entfernung', 'Studierende'),
        ('S-Bahn', 'Studierende'),
        ('Kueche', 'Expatriate'),
        ('Bad', 'Expatriate'),
        ('S-Bahn', 'Expatriate'),
        ('Entfernung', 'Expatriate'),
        ('Kehrwoche', 'Expatriate'),
        ('Hausmeister', 'Expatriate'),
        ('Miete', 'Rentnerpaar'),
        ('Kueche', 'Rentnerpaar'),
        ('Stockwerk', 'Rentnerpaar'),
        ('Aufzug', 'Rentnerpaar'),
        ('Garage', 'Rentnerpaar'),
        ('Balkon', 'Rentnerpaar'),
        ('Terrasse', 'Rentnerpaar'),
        ('Bad', 'Rentnerpaar'),
        ('Bad', 'DINK'),
        ('Kueche', 'DINK'),
        ('Balkon', 'DINK'),
        ('Terrasse', 'DINK'),
        ('S-Bahn', 'DINK'),
        ('Garage', 'DINK'),
        ('Entfernung', 'DINK'),
        ('S-Bahn', 'SingleHighIncome'),
        ('Entfernung', 'SingleHighIncome'),
        ('Garage', 'SingleHighIncome'),
        ('Balkon', 'SingleHighIncome'),
        ('Terrasse', 'SingleHighIncome'),
        ('Bad', 'SingleHighIncome'),
        ('Kueche', 'SingleHighIncome')]
# Make the actual Bayesian DAG
DAG = bnlearn.make_DAG(edges)

# [BNLEARN.print_CPD] No CPDs to print. Use bnlearn.plot(DAG) to make a plot.
# Plot the DAG
# bnlearn.plot(DAG)

DAG = bnlearn.parameter_learning.fit(DAG, df)

# Print the learned CPDs
# bnlearn.print_CPD(DAG)

bnlearn.save(DAG, filepath='oh_god_please_dont_crash')