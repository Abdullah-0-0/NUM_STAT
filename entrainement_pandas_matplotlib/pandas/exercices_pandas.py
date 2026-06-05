"""Exercices Pandas pour s'entraîner."""

import pandas as pd

# 1) Charger les données depuis un fichier CSV
# change le chemin si besoin, par exemple '../players.csv'
chemin = r"C:\Users\chams\Documents\IUT\PC IUT\Documents\Documents\NUM_STAT\players.csv"
try:
    df = pd.read_csv(chemin)
except FileNotFoundError:
    print(f"Fichier non trouvé : {chemin}")
    df = pd.DataFrame()

# 2) Afficher les informations principales
print("\t\t\t=== Aperçu des données ===")

print("\t\t\t\t=== head ===")
print(df.head())
print("\t\t\t\t=== info ===")
print(df.info())
print("\t\t\t\t=== columns ===")
print(df.columns)

# 3) Sélectionner des colonnes
if not df.empty:
    colonnes = df.columns.tolist()[:5]  
    print("\n=== Colonnes sélectionnées ===")
    print(df[colonnes].head())

# 4) Filtrer les lignes (exemple générique)
if not df.empty:
    if "age" in df.columns:
        print("\n=== Joueurs de moins de 25 ans ===")
        print(df[df["age"] < 25].head())
    else:
        print("\nAucune colonne 'age' dans le jeu de données.")

# 5) Groupby et moyenne
if not df.empty and "team" in df.columns:
    print("\n=== Moyenne par équipe ===")
    print(df.groupby("team").mean(numeric_only=True).head())
else:
    print("\nImpossible de faire un groupby par équipe : colonne 'team' manquante.")

# 6) Trier les données
if not df.empty and len(df.columns) > 1:
    print("\n=== Données triées par la première colonne numérique ===")
    numeriques = df.select_dtypes(include="number").columns
    if len(numeriques) > 0:
        print(df.sort_values(by=numeriques[0], ascending=False).head())
    else:
        print("Aucune colonne numérique pour trier.")

# 7) Ajouter une colonne calculée
if not df.empty:
    df["exemple_calcule"] = 1
    print("\n=== Ajout d'une colonne exemple_calcule ===")
    print(df.head())

print("\nExercices Pandas terminés.")
