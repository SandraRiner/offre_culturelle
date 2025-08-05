#Répertoire des ressources documentaires du ministère de la Culture

import numpy as np
import pandas as pd
import os

''''
csv_path= '/home/karim/code/offre_culturelle/data/repertoire-des-ressources-documentaires.csv' # Chemin vers le fichier CSV
if os.path.exists(csv_path):
    print(f"Le fichier {csv_path} existe.")
    repertoire_des_ressources_documentaires = pd.read_csv(csv_path, sep=';')
else:
    print(f"Le fichier {csv_path} n'existe pas.")

print(repertoire_des_ressources_documentaires.head()) # 5 rows x 50 columns
print(repertoire_des_ressources_documentaires.info()) # 163 données - dtypes: object(50)
print(repertoire_des_ressources_documentaires.describe())
'''

csv_path= '/home/karim/code/offre_culturelle/data/repertoire-des-ressources-documentaires.csv' # Chemin vers le fichier CSV
repertoire_des_ressources_documentaires = pd.read_csv(csv_path, sep=';')
print(repertoire_des_ressources_documentaires['Type d’établissement'].value_counts(dropna=False)) # Connaître les valeurs uniques d'une colonne