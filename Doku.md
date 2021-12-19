#KI PE19 P2 Wohnung
##Wer wohnt hier?
####Methode: Probabilistische Netze
####Aufgabenstellung: 
Es wird eine Wohnung beschrieben und aufgrund der gegebenen Faktoren soll errechnet werden wer in dieser Wohnung wohnt.
####Gegebene Faktoren:
- Zimmerzahl
- Stockwerk
- Hausmeister
- Kindergarten
- Schule
- S-Bahn
- Garage
- Miete
- Nebenkosten
- Alter
- Aufzug
- Lage
- Entfernung
- Kaution
- Kueche
- Bad
- Balkon
- Terrasse
- Kehrwoche
- Quadratmeter

####Gesucht:
- Studierende
- Kleinfamilie
- DINK
- SingleHighIncome
- Expatriate
- Rentnerpaar

####Ansatz
Zu Beginn haben wir die Attribute wie oben aufgeführt die Attribute in zwei Gruppen aufgeteilt. Zum einen in die Gruppe Attribute zur Wohnung, sowie die Bewohner.
Zusätzlich haben wir diese in Untergruppen aufgeteilt, welche miteinander in Relation stehen:
######Direkte Kosten
- Miete
- Kaution
- Nebenkosten
- Kehrwoche
- Hausmeister

######Lage
- Lage
- S-Bahn
- Entfernung
- Kindergarten
- Schule
- Garage

######Physische Faktoren
- Quadratmeter
- Zimmerzahl
- Stockwerk
- Terrasse
- Balkon
- Bad
- Küche
- Aufzug

Mithilfe dieser Untergruppen wurde folgendes Netz aufgestellt:
![Aufbau Bayes Netz](https://raw.githubusercontent.com/DerUniMax/PE19P2/main/planning/net.png "Wer wohnt hier?")
#####Abhängigkeiten der Wohnungsattribute
S-Bahn, Schule, Kindergarten und Entfernung hängen direkt von der Lage ab, da diese die Entfernung zu den genannten Attributen bestimmt.
Das Stockwerk, sowie das Alter bzw. das vorhandensein einer Küche werden direkt vom Alter des Hauses in welchem sich die Wohnung befindet beeinflusst. Dies entsteht durch Variation in der Bauweise, welche sich über die Jahre hinweg verändert. Somit sind in einem moderneren Haus meist mehr Stockwerke, sowie meist eine moderne Küche vorzufinden, wohingegen in einem älteren Haus die Wahrscheilichkeit für eine ältere Küche zunimmt und die Anzahl der Stockwerke meist abnimmt.
Das Stockwerk beeinflusst die Wahrscheinlichkeit, bzw. Möglichkeit auf eine Terasse oder Balkon, sowie einen Aufzug. Im Erdgeschoss ist die Wahrscheinlichkeit eines Balkons gegen Null, wohingegen das Erdgeschoss als einziges Stockwerk die Wahrscheinlichkeit auf eine Terasse bietet. Zusätzlich beinflusst das Stockwerk den Aufzug, da in Häusern mit höheren Stockwerken meist ein Aufzug vorhanden ist.
Das Vorhandensein einer Terrasse hängt direkt vom Vorhandensein eines Balkons ab, da nur eines der beiden geben kann.
Die Häufigkeit einer Kehrwoche hängt, wie die höhe der Nebenkosten vom Hausmeister ab. Da sich der Hausmeister meist um die Sauberkeit kümmert entfällt die Kehrwoche meist sobald ein Hausmeister eingestellt ist. Jedoch steigen dann meist die Nebenkosten.
Die Miete wird von der Garage und den Quadratmetern direkt beinflusst, da die Garage den Mietkostenbeitrag erhöht. Die Miete wird ebenfalls erhöht sobald sich die Quadratmeter erhöhen.
Die Quadratmeter beeinflussen direkt die Zimmerzahl, da mehr Quadratmeter mehr Möglichkeit für Zimmer bietet.
Die Kaution erhöht sich mit dem Zustand der Küche und der Höhe der Miete.
#####Relation zu den Bewohnern
Für einen Expatriaten sind die relevantesten und somit auch die fokussiertesten Wohnungsattribute die Nähe zur S-Bahn, die Entfernung zum Arbeitgeber, das Bad, die Küche, sowie die Kehrwoche und der Hausmeister. Diese favoririsierten Attribute ergeben sich daraus, dass für einen Expatriaten die Kosten eher irrelevant sind, da diese meist von der Firma getragen werden, er jedoch meist keine Lust auf Reinigung der öffentlichen Räumlichkeiten hat (Hausmeister und Kehrwoche). Er jedoch lange genug in der Wohnung bleibt um ein Bad und eine Küche, meist in der Wohnung, möchte. Da der Arbeitgeber meist die Wohnung zahlt legt dieser Wert auf die Nähe zum Arbeitsplatz und die Anbindung mit der S-Bahn. Er jedoch zu kurz vor Ort ist um sich ein eigenes Auto zuzulegen.
Für SingleHighIncome und DINK legen auf die gleichen Attribute wert. Diese umfassen das Vorhandensein eines Balkons, bzw. einer Terrasse, sowie eines Bades, einer Küche und einer Garage. Die Entfernung zum Arbeitgeber spielt mit der Entfernung zu S-Bahn ebenfalls eine Rolle. Balkon, Terrasse sind meist aus Luxus vorhanden. Die Garage, die Entfernung und die S-Bahn spielen für die Fortbewegung beider Bewohnerarten eine Rolle.
Für eine Kleinfamilie liegt meist der Haupaugenmerk auf möglichst groß für wenig Geld, somit sind für eine Kleinfamilie Miete, Zimmerzahl, Quadratmeter und Nebenkosten sehr relevant. Hinzu kommt ebenfalls die Nähe zu Kindergarten und Schule für die Kinder, wobei die Entfernung für die Eltern, sowie die Anbingung an die S-Bahn vernachlässigt wird. Für die Kleinfamilie ist ein Bad und eine Küche ebenfalls essentiell.
Für ein Rentnerpaar spielen als Luxus Balon und Terrasse eine Rolle, aus geldlichen Gründen meist Miete und Nebenkosten eine Rolle. Ebenfalls ist für Rentner eine Küche, ein Bad und eine Garage relevant.
Für einen Studenten ist der Hauptaugenmerk auf Geld, die S-Bahn, sowie die Entfernung. Geld bezieht sich in diesem Fall auf Kaution, Miete und Nebenksoten.
