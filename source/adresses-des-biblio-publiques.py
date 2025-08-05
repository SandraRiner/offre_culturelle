import numpy as np
import pandas as pd
import os

''''
csv_path= '/home/karim/code/offre_culturelle/data/adresses-des-bibliotheques-publiques.csv' # Chemin vers le fichier CSV
if os.path.exists(csv_path):
    print(f"Le fichier {csv_path} existe.")
    adresses_des_bibliotheques_publiques = pd.read_csv(csv_path, sep=';')
else:
    print(f"Le fichier {csv_path} n'existe pas.")

print(adresses_des_bibliotheques_publiques.head()) # 5 rows x 46 columns
print(adresses_des_bibliotheques_publiques.info()) # 15 704 données - dtypes: float64(26), object(20)
print(adresses_des_bibliotheques_publiques.describe())
'''

csv_path= '/home/karim/code/offre_culturelle/data/adresses-des-bibliotheques-publiques.csv' # Chemin vers le fichier CSV
adresses_des_bibliotheques_publiques = pd.read_csv(csv_path, sep=';')
print(adresses_des_bibliotheques_publiques['Région'].value_counts(dropna=False))