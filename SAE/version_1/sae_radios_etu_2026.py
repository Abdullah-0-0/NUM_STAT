import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# Chargement des données
path = ''
data_radios = pd.read_csv(path + 'reponses_radio_test1.csv', sep=';')
# On charge le fichier CSV contenant les réponses radio.
# test0, test1 et test2 sont des fichiers de validation décrits dans la consigne.

# 1) Calcul des effectifs observés
def calcul_eff_obs(mon_df, var_lignes, var_colonnes):
    # Regroupe les données selon les variables de ligne et de colonne,
    # puis compte le nombre d'observations pour chaque case du tableau.
    res = mon_df.groupby([var_lignes, var_colonnes]).size().unstack()
    return res

res_list_jazz = [16, 9, 13, 2, 19, 4]
res_list_radio6 = [8, 52, 2, 4, 1, 75, 29, 29]
# calcul du tableau d'effectifs observés par style musical et radio
eff_obs_radios = calcul_eff_obs(data_radios, 'Style musical', 'Radio')
print('test calcul_eff_obs : ', len(res_list_jazz) - list(np.isclose(eff_obs_radios.loc['Jazz'], res_list_jazz)).count(True) == 0)
print('test calcul_eff_obs : ', len(res_list_radio6) - list(np.isclose(eff_obs_radios['Radio 6'], res_list_radio6)).count(True) == 0)

# 2) Calcul des effectifs théoriques sous indépendance
def calcul_eff_theo(eff_obs):
    # Sommes par lignes et par colonnes
    total_ligne = eff_obs.sum(axis=1)
    total_colo = eff_obs.sum(axis=0)
    total_elem = eff_obs.values.sum()
    # Produit des marges divisé par le total général
    res = np.outer(total_ligne, total_colo) / total_elem
    # Conversion en DataFrame pour garder les mêmes index et colonnes
    return pd.DataFrame(res, index=eff_obs.index, columns=eff_obs.columns)

res_list_indie = [4.41, 6.384, 9.576, 5.754, 7.476, 8.4]
res_list_radio2 = [17.784, 27.056, 6.384, 9.576, 8.816, 31.464, 23.56, 27.36]
eff_theo_radios = calcul_eff_theo(eff_obs_radios)
print('test calcul_eff_theo : ', len(res_list_indie) - list(np.isclose(eff_theo_radios.loc['Indie'].to_list(), res_list_indie)).count(True) == 0)
print('test calcul_eff_theo : ', len(res_list_radio2) - list(np.isclose(eff_theo_radios['Radio 2'].to_list(), res_list_radio2)).count(True) == 0)

# 3) Calcul de la contribution au khi-2
def calcul_contrib(eff_obs, eff_theo):
    # Contribution du khi-2 pour chaque case : (obs - théorique)^2 / théorique
    pd.set_option("display.precision", 5)
    res = ((eff_obs - eff_theo) ** 2) / eff_theo
    return res

res_list_rock = [0.032296466973886453, 3.7824108658743643, 1.9681833616298825, 0.844606781257358, 0.7048967017035158, 0.12903225806451613]
res_list_radio1 = [0.6000183150183149, 7.311722846441949, 2.6367573696145126, 13.314924414210127, 86.1852380952381, 11.391314699792959, 0.032296466973886453, 1.2703703703703697]
contrib_radios = calcul_contrib(eff_obs_radios, eff_theo_radios)
print('test calcul_contrib : ', len(res_list_rock) - list(np.isclose(contrib_radios.loc['Rock'].to_list(), res_list_rock)).count(True) == 0)
print('test calcul_contrib : ', len(res_list_radio1) - list(np.isclose(contrib_radios['Radio 1'].to_list(), res_list_radio1)).count(True) == 0)

# 4) Analyse des contributions les plus fortes
def analyse_contrib(n, eff_obs, eff_theo, contrib):
    # diff indique si l'observé est supérieur ou inférieur au théorique
    diff = eff_obs - eff_theo
    contributions = []
    for style in contrib.index:
        for radio in contrib.columns:
            value = float(contrib.at[style, radio])
            # signe + si on a plus d'observations que prévu, - si on en a moins
            signe = '+' if diff.at[style, radio] > 0 else '-'
            contributions.append((style, radio, signe, value))
    # tri par contribution décroissante
    contributions.sort(key=lambda item: item[3], reverse=True)
    return contributions[:n]

ntest = 6
ana_contrib_radios = analyse_contrib(ntest, eff_obs_radios, eff_theo_radios, contrib_radios)
res_list = [('Musique classique', 'Radio 1', '+', 86.1852380952381), ('Pop', 'Radio 6', '+', 27.269565217391307), ('Electro', 'Radio 4', '+', 24.88245311622684), ('Hip-Hop & RnB', 'Radio 2', '-', 16.386573625073922), ('Variété', 'Radio 2', '+', 15.570526315789476), ('Jazz', 'Radio 1', '+', 13.314924414210127)]
test_contrib = (list(np.isclose([res_list[i][3] for i in range(ntest)], [ana_contrib_radios[i][3] for i in range(ntest)])).count(True) == ntest)
test_sens_dep = ([res_list[i][2] == ana_contrib_radios[i][2] for i in range(ntest)].count(True) == ntest)
test_radios = ([res_list[i][1] == ana_contrib_radios[i][1] for i in range(ntest)].count(True) == ntest)
test_styles = ([res_list[i][0] == ana_contrib_radios[i][0] for i in range(ntest)].count(True) == ntest)
print('test analyse_contrib : ', test_contrib and test_sens_dep and test_radios and test_styles)

# 5) Diagrammes des résultats
def diagrammes(eff_obs, eff_theo, ana_contrib, lien):
    # labels pour chaque case sélectionnée : style + radio
    labels = [f"{style}\n{radio}" for style, radio, _, _ in ana_contrib]
    obs_values = [eff_obs.at[style, radio] for style, radio, _, _ in ana_contrib]
    theo_values = [eff_theo.at[style, radio] for style, radio, _, _ in ana_contrib]
    contrib_values = [value for _, _, _, value in ana_contrib]
    # on met en couleur les contributions qui ont le même signe que le lien demandé
    colors = ['tab:red' if signe == lien else 'tab:gray' for _, _, signe, _ in ana_contrib]

    fig, axes = plt.subplots(2, 1, figsize=(12, 10), constrained_layout=True)

    x = np.arange(len(labels))
    width = 0.35
    axes[0].bar(x - width/2, obs_values, width, label='Observé', color='tab:blue')
    axes[0].bar(x + width/2, theo_values, width, label='Théorique', color='tab:orange')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels, rotation=45, ha='right')
    axes[0].set_ylabel('Effectifs')
    axes[0].set_title('Comparaison des effectifs observés et théoriques pour les plus fortes contributions')
    axes[0].legend()

    axes[1].bar(x, contrib_values, color=colors)
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels, rotation=45, ha='right')
    axes[1].set_ylabel('Contribution khi-2')
    axes[1].set_title('Top contributions au khi-2')
    axes[1].axhline(0, color='black', linewidth=0.8)
    plt.show()

# Appel du tracé avec les contributions analysées
diagrammes(eff_obs_radios, eff_theo_radios, ana_contrib_radios, '+')

