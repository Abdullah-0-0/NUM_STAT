import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Création d'une Series à partir d'un dictionnaire
# Les clés deviennent l'index, les valeurs deviennent les données
dict_club={1:'Arsenal',2:'Aston Villa',5:'Chelsea',7:'Everton',8:'Leeds United'}
serie_club_d=pd.Series(dict_club)
print(f'Avec un dict, serie_club_d :\n{serie_club_d}')

# Création d'une Series avec données et index spécifiés
serie_club=pd.Series(['Arsenal','Aston Villa','Chelsea','Everton','Leeds United'],index=[1,2,5,7,8])
print(f'Avec index renseigné, serie_club :\n{serie_club}')

#Sans index renseigné, une indexation est définie par défaut (0,1,2,...)
serie_club2=pd.Series(['Arsenal','Aston Villa','Chelsea','Everton','Leeds United'])
print(f'Sans index renseigné\n{serie_club2}')

#Avec une double indexation (MultiIndex)
serie_club_3=pd.Series(['Arsenal','Aston Villa','Chelsea','AS Monaco','Angers SCO'],index=[['English Premier League']*3+['French Ligue 1']*2,[1,2,3,1,2]])
print(f'Avec une double indexation\n{serie_club_3}')

serie_club.name='Nom club'
serie_club.index.name='Id_club'
print(serie_club)


print(serie_club.values)
print(type(serie_club.values))
print(serie_club.index.values)


print(serie_club)
print('serie_club.loc[1] : ',serie_club.loc[1])
print('serie_club[1] : ',serie_club[1])
print(f'serie_club[[1,7]] :\n{serie_club[[1,7]]}')
print(f'serie_club.iloc[1] : {serie_club.iloc[1]}')
print(f'serie_club.iloc[0:3] :\n{serie_club.iloc[0:3]}')
print(f'serie_club[1:] :\n{serie_club[1:]}')


dico_players={
    "Player_name" : pd.Series(['L. Messi','P. Dybala','E. Martinez','G. Lo Celso','N.Otamendi','K. Mbappé','J. Veretout','H. Lloris']),
    "Nationality" : pd.Series(['Argentina']*5+['France']*3),
    "Player_club_id" : pd.Series([73,45,2,18,234,73,52,18]),
    "Age" : pd.Series([33,26,27,24,32,21,27,33]),
    "ValueEUR" : pd.Series([103500000,95000000,33000000,38500000,13500000,185500000,26500000,26000000])
}
data_players=pd.DataFrame(dico_players)
print(data_players,'\n')
print(data_players['Nationality'])
print(data_players.iloc[:2],'\n')
print(data_players.loc[1:3],'\n')
print(data_players.loc[2],'\n')
print(data_players.sort_values(['ValueEUR'],ascending=False).head(3))#head(3) agit ici comme [:3].head(3))#head(3) agit ici comme [:3]




df_reduit=data_players[['Player_name','Nationality','Age']]
serie_age=data_players['Age']
print(df_reduit)
print(f'La moyenne des âges est de {serie_age.mean()} ')



new_df=data_players.copy()
new_df.loc[new_df.Nationality=='Argentina','ValueEUR']=new_df.ValueEUR+5000000#Augmentation de la valeur pour Argentins
new_df['Valeur par année avant retraite']=np.floor(new_df['ValueEUR']/(40-new_df['Age']))#Estimation avec âge de retraite fixé à 40 ans
print(new_df[['Player_name','Nationality','Age','ValueEUR','Valeur par année avant retraite']])


print(data_players['Age'].describe())
data_players.set_index([pd.Series([158023,211110,202811,226226,192366,231747,201519,167948],name='Player_ID')],inplace=True)
print(f"L\'index s'appelle comme ça : {data_players.index.name}")
data_players.index.name='nom_index'
print(f"Une fois renommé il s'appelle comme ça : {data_players.index.name}")
#et si on veut revenir sur ce dernier choix :
data_players.reset_index(inplace=True,drop=True)
#Ci-dessus l'argument drop permet de décider si on abandonne l'index supprimé (paramètre=True) ou si on le place en colonne (paramètre=False)
print(f"Et voici les noms en index une fois qu'on l'a supprimé :{data_players.index.names}",' ou ',data_players.index.name)
print(data_players.shape)
print(data_players)


mask_selection_1=(data_players['Nationality']=='Argentina')&(data_players['Age']>=30) #Vous avez essayé avec and ?
mask_selection_2=(data_players.Nationality=='France')|(data_players['Age']<30)
mask_selection_3=data_players.Player_club_id.isin([73,18,2])#Pour filtrer selon les valeurs présentes dans une liste
selection_1=data_players[mask_selection_1][['Nationality','Age']]
selection_2=data_players[mask_selection_2]
selection_3=data_players[mask_selection_3][['Player_name','Player_club_id']]
print(selection_1)
print(selection_2)
print(selection_3)


selection=pd.concat([selection_1,selection_2])
print(selection)
df1=data_players[mask_selection_1][['Player_name','Nationality']]
serie2=data_players[mask_selection_2]['Age']
df3=data_players[mask_selection_3][['Player_club_id']]
print('\n Concaténation sur les colonnes :')
print(df1,'\n')
print(serie2)
print(df3)
df_concatene=pd.concat([df1,serie2,df3],axis=1)
print(df_concatene)



print(selection[selection['Player_name'].isnull()],'\n')
print(selection[selection['Player_name'].notnull()],'\n')
print(selection.dropna(inplace=False),'\n')
print(selection.fillna(value={'Player_name':'Footballeur inconnu','ValueEUR':0}))




df_evenements=pd.DataFrame({'année':np.random.randint(2020,2023,100),'mois':np.random.randint(1,12,100),'jour':np.random.randint(1,30)})
print(df_evenements.head(10))
print('type mois : ',type(df_evenements.mois[0]))
df_evenements['mois_bis']=df_evenements.mois.astype('str')
print('type mois bis : ',type(df_evenements.mois_bis[0]))
df_evenements['mois_bis']=df_evenements['mois_bis'].str.zfill(2)
df_evenements['date']=df_evenements.année.astype(str)+'-'+df_evenements.mois_bis+'-'+df_evenements.jour.astype(str)
print('type date : ',type(df_evenements['date'][0]))
df_evenements['date']=df_evenements['date'].astype('datetime64[ns]')
print(df_evenements['date'].dtype)
print('durée entre deux premières dates : ',df_evenements['date'][1]-df_evenements['date'][0])





dico_clubs={
    'Club_id':[2,5,18,45,52,71,73,234],
    'Club_name':['Aston Villa','Chelsea','Tottenham Hotspur','Juventus','Roma','FC Nantes','Paris Saint-Germain','SL Benfica'],
    'League':['English Premier League']*3+['Italian Serie A']*2+['French Ligue 1']*2+['Portuguese Liga']
}
data_clubs=pd.DataFrame(dico_clubs)
data_clubs_anglais=data_clubs[(data_clubs.League=='English Premier League')]

qui_qui_joue_dans_ces_clubs=pd.merge(left=data_clubs_anglais,right=data_players,how='left',left_on=['Club_id'],right_on=['Player_club_id'])
print(f"left :\n{qui_qui_joue_dans_ces_clubs[['Club_name','Player_name']]}\n")

qui_qui_joue_dans_ces_clubs_2=pd.merge(left=data_clubs_anglais,right=data_players,how='inner',left_on=['Club_id'],right_on=['Player_club_id'])
print(f"inner :\n{qui_qui_joue_dans_ces_clubs_2[['Club_name','Player_name']]}\n")

qui_qui_joue_dans_ces_clubs_3=pd.merge(left=data_clubs_anglais,right=data_players,how='outer',left_on=['Club_id'],right_on=['Player_club_id'])
print(f"outer :\n{qui_qui_joue_dans_ces_clubs_3[['Club_name','Player_name']]}")





joueurs_par_clubs=pd.merge(left=data_clubs,right=data_players,how='inner',left_on=['Club_id'],right_on=['Player_club_id'])[['Club_name','Player_name','League','Age','ValueEUR']]
print(f"joueurs_par_clubs :\n{joueurs_par_clubs}\n")
joueurs_par_clubs_reindexe=joueurs_par_clubs.set_index(['League','Club_name'],inplace=False)
print(f"joueurs_par_clubs_reindexe :\n{joueurs_par_clubs_reindexe}\n")
calculs_moyennes_par_league_via_index=joueurs_par_clubs_reindexe.groupby(['League'])[['Age','ValueEUR']].mean()
calculs_moyennes_par_club_via_index=joueurs_par_clubs_reindexe.groupby(level=1)[['Age','ValueEUR']].mean()
print(f'Calculs âge et valeur moyenne par League via index :\n{calculs_moyennes_par_league_via_index}\n')
print(f'Calculs âge et valeur moyenne par Club via index :\n{calculs_moyennes_par_club_via_index}\n')
calculs_moyennes_par_league=joueurs_par_clubs.groupby(['League'])[['Age','ValueEUR']].mean()
print(f'Calculs âge et valeur moyenne par league :\n{calculs_moyennes_par_league}\n')
calculs_divers_par_league=joueurs_par_clubs.groupby(['League']).agg({'Age':['mean'],'ValueEUR':['mean','sum']})
print(f'Calculs divers par league :\n{calculs_divers_par_league}\n')



data_joueurs = pd.read_csv('players.csv',sep=';')
data_equipes=pd.read_csv('teams.csv',sep=';')
print(list(data_joueurs.columns))
print(data_joueurs[data_joueurs.columns[:5]].head(5),'\n')
print(data_equipes[data_equipes.columns[:3]].head(5))



mask=data_equipes['LeagueId'].isin([13,16,19,31,53])
data_equipes_r=data_equipes[mask]
df_data_joueurs_clubs=pd.merge(data_joueurs,data_equipes_r,how='inner',left_on='Club_id',right_on='ID')[['BestPosition','League','ValueEUR','Height' ]]
#print(df_data_joueurs_clubs)
df_stats_positions=df_data_joueurs_clubs.groupby(['BestPosition','League']).agg({'Height':['count','mean'],'ValueEUR':['mean']})
print('df base :',df_stats_positions)
#(df_stats_positions.index)
#print(df_stats_positions.columns)
#print('level values : ',df_stats_positions.index.get_level_values(0))
df_unstacke=df_stats_positions.unstack(level=1)
print('df_unstacke : ',df_unstacke)
df_stacke=df_unstacke.stack(level=2)
print(df_stacke)
print('stats french central attacking midfielder : \n',df_stats_positions.loc[('CAM','French Ligue 1 (1)'),'Height'])
print(df_stats_positions.loc[slice('CAM','GK'),'Height'])
print(df_stats_positions.loc[(slice('CAM','GK'),slice(None))])



"""**Question 1** : Afficher le tableau présentant l'âge moyen et les moyennes, médianes et valeurs maximales pour les revenus (`WageEUR`) à l'intérieur de chaque club de ligue 1 en France."""
print("#######################################")
print("\t\t\t\tEcercices 1")

fus = pd.merge(data_joueurs,data_equipes,right_on='ID',left_on='Club_id',how="inner")
filtr = fus[fus['League']=='French Ligue 1 (1)']
fina_group = filtr.groupby(['Name_y']).agg({
    'Age': 'mean',
    'WageEUR':['mean','median','max']
})
print(fina_group)


"""**Question 2** : Comparer avec des diagrammes en boîtes à moustaches (`plt.boxplot`) les salaires de ligue 1 et de ligue 2."""


print("#######################################")
print("\t\t\t\tEcercices 2")
ligue_salaire1 = filtr['WageEUR']
ligue2 = fus[fus["League"]=='French Ligue 2 (2)']
ligue2_salaire = ligue2["WageEUR"]

plt.figure(figsize=(8,6))
plt.boxplot([ligue_salaire1,ligue2_salaire],labels=['League 1', 'League 2'])
plt.title('Comparaison des salaires en Ligue 1 et Ligue 2')
plt.show()

