import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec



path=''
data_radios=pd.read_csv(path+'reponses_radio_test1.csv',sep=';')
#test0 est là pour retrouver les résultats de l'énoncé papier, test1 les résultats des 4 premières fonctions et des deux premiers graphiques et test2 les deux derniers graphiques
def calcul_eff_obs(mon_df,var_lignes,var_colonnes):
    res = mon_df.groupby([var_lignes,var_colonnes]).size().unstack()
    return res

res_list_jazz=[16, 9, 13, 2, 19, 4]
res_list_radio6=[8, 52, 2, 4, 1, 75, 29, 29]
eff_obs_radios=calcul_eff_obs(data_radios,'Style musical','Radio')
print('test calcul_eff_obs : ',len(res_list_jazz)-list(np.isclose(eff_obs_radios.loc['Jazz'],res_list_jazz)).count(True)==0)
print('test calcul_eff_obs : ',len(res_list_radio6)-list(np.isclose(eff_obs_radios['Radio 6'],res_list_radio6)).count(True)==0)

def calcul_eff_theo(eff_obs):
    total_ligne = eff_obs.sum(axis=1)
    total_colone = eff_obs.sum(axis=0)
    total_element = eff_obs.values.sum()
    res = np.outer(total_ligne,(total_colone/total_element))
    return pd.DataFrame(res,eff_obs.index,eff_obs.columns)

res_list_indie=[4.41, 6.384, 9.576, 5.754, 7.476, 8.4]
res_list_radio2=[17.784, 27.056, 6.384, 9.576, 8.816, 31.464, 23.56, 27.36]
eff_theo_radios=calcul_eff_theo(eff_obs_radios)
print('test calcul_eff_theo : ',len(res_list_indie)-list(np.isclose(eff_theo_radios.loc['Indie'].to_list(),res_list_indie)).count(True)==0)
print('test calcul_eff_theo : ',len(res_list_radio2)-list(np.isclose(eff_theo_radios['Radio 2'].to_list(),res_list_radio2)).count(True)==0)

def calcul_contrib(eff_obs,eff_theo):

    pd.set_option("display.precision", 5)
    res = ((eff_obs-eff_theo)**2)/eff_theo
    return res

res_list_rock=[0.032296466973886453, 3.7824108658743643, 1.9681833616298825, 0.844606781257358, 0.7048967017035158, 0.12903225806451613]
res_list_radio1=[0.6000183150183149, 7.311722846441949, 2.6367573696145126, 13.314924414210127, 86.1852380952381, 11.391314699792959, 0.032296466973886453, 1.2703703703703697]
contrib_radios=calcul_contrib(eff_obs_radios,eff_theo_radios)
print('test calcul_contrib : ',len(res_list_rock)-list(np.isclose(contrib_radios.loc['Rock'].to_list(),res_list_rock)).count(True)==0)
print('test calcul_contrib : ',len(res_list_radio1)-list(np.isclose(contrib_radios['Radio 1'].to_list(),res_list_radio1)).count(True)==0)

def analyse_contrib(n,eff_obs,eff_theo,contrib):
    diff = eff_obs - eff_theo
    liste = []
    signe = ""
    for idx in contrib.index:
        for col in contrib.columns:
            values = float(contrib.at[idx,col])
            if diff.at[idx,col]>0:
                signe="+"
            else:
                signe="-"
            liste.append((idx,col,signe,values))
    liste.sort(key=lambda item:item[3],reverse = True)
    return liste

ntest=6
ana_contrib_radios=analyse_contrib(ntest,eff_obs_radios,eff_theo_radios,contrib_radios)
res_list=[('Musique classique', 'Radio 1', '+', 86.1852380952381), ('Pop', 'Radio 6', '+', 27.269565217391307), ('Electro', 'Radio 4', '+', 24.88245311622684), ('Hip-Hop & RnB', 'Radio 2', '-', 16.386573625073922), ('Variété', 'Radio 2', '+', 15.570526315789476), ('Jazz', 'Radio 1', '+', 13.314924414210127)]
test_contrib=(list(np.isclose([res_list[i][3] for i in range(ntest)],[ana_contrib_radios[i][3] for i in range(ntest)])).count(True)==ntest)
test_sens_dep=([res_list[i][2]==ana_contrib_radios[i][2] for i in range(ntest)].count(True)==ntest)
test_radios=([res_list[i][1]==ana_contrib_radios[i][1] for i in range(ntest)].count(True)==ntest)
test_styles=([res_list[i][0]==ana_contrib_radios[i][0] for i in range(ntest)].count(True)==ntest)
print('test analyse_contrib : ',test_contrib and test_sens_dep and test_radios and test_styles)

def diagrammes(eff_obs,eff_theo,ana_contrib,lien):
    contri_tri= []
    for rang , (style, radio, signe, valeur) in enumerate(ana_contrib):
        if signe == lien:
            contri_tri.append((rang,style, radio, valeur))

    if lien == '+':
        texte_lien = "attractifs"
    if lien == '-':
        texte_lien = "répulsifs"

    radios = eff_obs.columns.to_list()
    styles = []
    for rang, style, radio,valeur in contri_tri:
        if style not in styles: 
            styles.append(style)
    nb_styles = len(styles)

    maxi = 0.2
    nb_contri = len(ana_contrib)
    exploratrion_par_styles = {}
    for style in styles:
        exploratrion_par_styles[style] = [1] * len(radio)
    for range , style,radio , valeur in contri_tri:
        if radio in radios:
            idx_radio = radios.index(radio)

            exploration_valeur = maxi * (nb_contri - rang) / nb_contri

            exploratrion_par_styles[style][idx_radio] = max(
                exploratrion_par_styles[style][idx_radio],
                exploration_valeur
            )
    nb_place_legend = 1 if nb_styles < 4  else 2
    nb_colone = max(nb_styles,nb_place_legend+ 1)
    fig = plt.figure(figsize=(4 * nb_colone, 8))
    gs = GridSpec(2,nb_colone,figure=fig)

    for i , style in enumerate(styles):
        ax = fig.add_subplot(gs[0,i])
        valeurs = eff_obs.loc[style].reindex(radios).fillna(0)
        ax.pie(
            valeurs,
            autopct="%0.0f%%"
        )
        ax.set_title("Répartition pour "+style,fontsize=10)
    fig.suptitle(
        "Comparaison entre répartition observée sur la sous-population "
        "par rapport à celle de l'ensemble de la population sur liens " + texte_lien,
        fontsize=10
    )
    plt.tight_layout()
    plt.show()

diagrammes(eff_obs_radios,eff_theo_radios,ana_contrib_radios,'+')

