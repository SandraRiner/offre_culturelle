import numpy as np
import pandas as pd
import os

''''
csv_path= '/home/karim/code/offre_culturelle/data/liste-officielle-museesdf-20220127-data.csv' # Chemin vers le fichier CSV
if os.path.exists(csv_path):
    print(f"Le fichier {csv_path} existe.")
    liste_museesdf = pd.read_csv(csv_path, sep=';', encoding='latin-1')
else:
    print(f"Le fichier {csv_path} n'existe pas.")

print(liste_museesdf.head()) # 5 rows x 55 columns
print(liste_museesdf.info()) # 88036 données - dtypes: float64(26), object(20)
print(liste_museesdf.describe())
'''

csv_path= '/home/karim/code/offre_culturelle/data/liste-officielle-museesdf-20220127-data.csv' # Chemin vers le fichier CSV
liste_museesdf = pd.read_csv(csv_path, sep=';', encoding='latin-1')
print(liste_museesdf['Région administrative'].value_counts(dropna=False))