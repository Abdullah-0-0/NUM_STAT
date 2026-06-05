"""# Manipulation de données avec pandas


Pour avoir accès aux fonctionnalités de `pandas`, 
il est de coutume de charger la librairie en lui accordant l'alias `pd`. 
Nous allons également utiliser des fonctions de `numpy` et 
des outils de visualisation de ```matplotlib.pyplot```
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""Pandas fournit essentiellement deux structures de données pour manipuler les données, ce sont les `Series` et les `Dataframe`

## Les `Series`

Une série est un tableau étiqueté unidimensionnel pouvant contenir tout type de données. Lors de l'affichage la (ou les)  première(s) colonne(s) contiennent les étiquettes qui représentent l'index de la série
"""
dict_club={1:'Arsenal',2:'Aston Villa',5:'Chelsea',7:'Everton',8:'Leeds United'}
serie_club_d=pd.Series(dict_club)
print(f'Avec un dict, serie_club_d :\n{serie_club_d}')

serie_club=pd.Series(['Arsenal','Aston Villa','Chelsea','Everton','Leeds United'],index=[1,2,5,7,8])
print(f'Avec index renseigné, serie_club :\n{serie_club}')

#Sans index renseigné, une indexation est définie par défaut
serie_club2=pd.Series(['Arsenal','Aston Villa','Chelsea','Everton','Leeds United'])
print(f'Sans index renseigné\n{serie_club2}')

#Avec une double indexation 
serie_club_3=pd.Series(['Arsenal','Aston Villa','Chelsea','AS Monaco','Angers SCO'],index=[['English Premier League']*3+['French Ligue 1']*2,[1,2,3,1,2]])
print(f'Avec une double indexation\n{serie_club_3}')

"""
Si on veut ajouter des noms à la série ou à l'index :"""
print("\n\tteste_perso\n")

serie_club.name='Nom club'
serie_club.index.name='Id_club'
print(serie_club)

"""
Si on veut récupérer l'ensemble des valeurs de la série ou de l'index :"""

print(serie_club.values)
print(type(serie_club.values))
print(serie_club.index.values)

"""
Pour interroger les valeurs stockées dans un objet `Series` on peut fonctionner de différentes manières. La méthode `iloc` fournit une méthode de sélection selon la position de l'élément voulu alors que `loc` exploite la valeur de l'index. L'opérateur d'indexation `[]` appliqué directement à un objet `Series` peut être également utilisé mais il faut être conscient de son comportement qui correspond soit à celui de `loc` soit à celui de `iloc` selon la valeur passée. Lorsque les deux traitements sont possibles le comportement adopté est celui de la méthode `loc`"""
print("\n\t\t\tinterroger les valeurs stockées:\n")
print(serie_club)
print("*******************************")
print('serie_club.loc[1] : ',serie_club.loc[1])
print("*******************************")
print('serie_club[1] : ',serie_club[1])
print("*******************************")
print(f'serie_club[[1,7]] :\n{serie_club[[1,7]]}')
print("*******************************")
print(f'serie_club.iloc[1] : {serie_club.iloc[1]}')
print("*******************************")
print(f'serie_club.iloc[0:3] :\n{serie_club.iloc[0:3]}')
print("*******************************")
print(f'serie_club[1:] :\n{serie_club[1:]}')
print("*******************************")

                                ## Les `Dataframe`
print("\n\t\t\t\tLes Dataframes\n\n")
"""
La `Dataframe` est une structure qui organise les données en lignes et en colonnes. On peut aussi se la représenter comme un dictionnaire d'objets `Series`. C'est l'objet `pandas` le plus utilisé. Pour accéder aux colonnes on utilise l'opérateur ['nom de la colonne' ] qui n'est plus exploitable pour l'accès aux lignes qui doit se faire par l'utilisation des méthodes `loc` et `iloc`"""

dico_players={
    "Player_name" : pd.Series(['L. Messi','P. Dybala','E. Martinez','G. Lo Celso','N.Otamendi','K. Mbappé','J. Veretout','H. Lloris']),
    "Nationality" : pd.Series(['Argentina']*5+['France']*3),
    "Player_club_id" : pd.Series([73,45,2,18,234,73,52,18]),
    "Age" : pd.Series([33,26,27,24,32,21,27,33]),
    "ValueEUR" : pd.Series([103500000,95000000,33000000,38500000,13500000,185500000,26500000,26000000])
}
data_players=pd.DataFrame(dico_players)

print(data_players,'\n')
print("*****************************")
print(data_players['Nationality'])

print("*****************************")
print(data_players.iloc[:2],'\n')
print("*****************************")
print(data_players.loc[1:3],'\n')
print("*****************************")
print(data_players.loc[2],'\n')
print("*****************************")
print(data_players.sort_values(['ValueEUR'],ascending=False).head(3))#head(3) agit ici comme [:3].head(3))#head(3) agit ici comme [:3]

"""
On peut extraire d'un `dataframe` un autre `dataframe` avec un nombre de colonnes restreint en spécifiant les noms des champs conservés dans une double paire de crochets.
On peut extraire d'un `dataframe` un objet `series` ce qui peut tout particulièrement être utile pour des représentations graphiques dans `matplotlib` quand le paramètre doit être un objet d'une dimension réduite à 1."""


