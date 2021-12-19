import pandas as pd
from pgmpy.models import BayesianNetwork

df = pd.read_csv("P1_DP13_Wohnungen_X.csv", sep=";")

edges = [
  ('Quadratmeter', 'Zimmerzahl'),
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
         ('Kueche', 'SingleHighIncome')
         ]

net = BayesianNetwork(edges)

net.fit(df, n_jobs=10)

print(net)