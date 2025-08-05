import numpy as np
import pandas as pd
import os

csv_path= '/home/karim/code/offre_culturelle/data/festivals-global-festivals-_-pl.csv' # Chemin vers le fichier CSV
if os.path.exists(csv_path):
    print(f"Le fichier {csv_path} existe.")
    festivals_global = pd.read_csv(csv_path, sep=';')
else:
    print(f"Le fichier {csv_path} n'existe pas.")

print(festivals_global.head()) # 5 rows x 30 columns
print(festivals_global.info()) # 7283 données - dtypes: float64(1), object(29)
print(festivals_global.describe())