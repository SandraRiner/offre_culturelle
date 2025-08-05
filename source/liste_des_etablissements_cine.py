import numpy as np
import pandas as pd
import os

csv_path= '/home/karim/code/offre_culturelle/data/exploitation-2024_etablissements-actifs.csv' # Chemin vers le fichier CSV
if os.path.exists(csv_path):
    print(f"Le fichier {csv_path} existe.")
    exploitation_2024_etablissements_actifs = pd.read_csv(csv_path, sep=';',  encoding='latin1')
else:
    print(f"Le fichier {csv_path} n'existe pas.")

print(exploitation_2024_etablissements_actifs.head()) # 5 rows x 9 columns
print(exploitation_2024_etablissements_actifs.info()) # 2055 données - dtypes: object(9)