import pandas as pd 
# 1) Charger les données depuis un fichier CSV
chemin = r"C:\Users\chams\Documents\IUT\PC IUT\Documents\Documents\NUM_STAT\players.csv"
chemin2 = r"C:\Users\chams\Documents\IUT\PC IUT\Documents\Documents\NUM_STAT\teams.csv"
data_player = pd.read_csv(chemin, sep=';')
data_team = pd.read_csv(chemin2, sep=';')
data_fusion = pd.merge(data_player,data_team, left_on="Club_id",right_on="ID",how="inner")
data_tri1 = data_player[["Name","Age"]]
# On groupe par âge et on calcule la moyenne sur la colonne numérique Age seulement
data_fr = data_tri1[data_tri1["Age"]==25]

league1 = data_fusion[data_fusion["League"]=="French Ligue 1 (1)"]
data_question_1 = league1.groupby("Name_y").agg({"Age": "mean",
                                               "WageEUR": ["mean", "median","max"]})
print(data_question_1)
