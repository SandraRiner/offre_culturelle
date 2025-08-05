import pandas as pd
import os

file_path = "home/karim/code/offre_culturelle/data/adresses-des-bibliotheques-publiques.csv"

if not os.path.exists(file_path):
    print(f"Le fichier {file_path} n'existe pas.")
else:
    adresses_des_biblio_publiques = pd.read_csv(file_path)
    print(adresses_des_biblio_publiques.head()) # 5 rows x 46 columns