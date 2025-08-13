import numpy as np
import pandas as pd
import os
''''
csv_path= '/home/karim/code/offre_culturelle/data/culturecheznous.csv' # Chemin vers le fichier CSV
if os.path.exists(csv_path):
    print(f"Le fichier {csv_path} existe.")
    culture_chez_nous = pd.read_csv(csv_path, sep=';')
else:
    print(f"Le fichier {csv_path} n'existe pas.")

print(culture_chez_nous.head()) # 5 rows x 30 columns
print(culture_chez_nous.info()) # 7283 données - dtypes: float64(1), object(29)
print(culture_chez_nous.describe())
'''
csv_path= '/home/karim/code/offre_culturelle/data/culturecheznous.csv' # Chemin vers le fichier CSV
culture_chez_nous = pd.read_csv(csv_path, sep=';')
#print(culture_chez_nous.info())
print(culture_chez_nous['Nom de l\'organisme'].value_counts(dropna=False))