import numpy as np
import pandas as pd
import os

''''

csv_path= '/home/karim/code/offre_culturelle/data/base-des-lieux-et-des-equipements-culturels.csv' # Chemin vers le fichier CSV
if os.path.exists(csv_path):
    print(f"Le fichier {csv_path} existe.")
    base_des_lieux_et_des_equipements_culturels = pd.read_csv(csv_path, sep=';')
else:
    print(f"Le fichier {csv_path} n'existe pas.")

print(base_des_lieux_et_des_equipements_culturels.head()) # 5 rows x 55 columns
print(base_des_lieux_et_des_equipements_culturels.info()) # 88036 données - dtypes: float64(26), object(20)
print(base_des_lieux_et_des_equipements_culturels.describe())

'''
csv_path= '/home/karim/code/offre_culturelle/data/base-des-lieux-et-des-equipements-culturels.csv' # Chemin vers le fichier CSV
base_des_lieux_et_des_equipements_culturels = pd.read_csv(csv_path, sep=';')
print(base_des_lieux_et_des_equipements_culturels['Précision équipement'].value_counts(dropna=False))