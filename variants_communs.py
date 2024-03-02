#!/usr/bin/env python3
import pandas as pd

def similaire(alt1, alt2, pdb=10): #fonction qui compare 2 séquences ALT et renvoie True si elles sont semblable (différence de longueur +ou- 10 pdb)
    return abs(len(alt1) - len(alt2)) <= pdb

# Function to find similar variants within the specified pdb for ALT sequence lengths
def variants_identiques(df_list, pdb=10): #fonction qui trouve des variants identiques dans différents passages en fonction de la sequence ALT, de sa taille et de la position
    var_ident = df_list[0].copy() #initialise var_ident comme une cope du premier dataframe (1er passsage dans le fichier excel)
    
    
    for df in df_list[1:]: # iteration sur chaque passage (1 passage= 1 feuille dans le fichier excel)
        match_var = [] #crée une liste des indices de matchs entre les deux df
        
        for base_index, base_row in var_ident.iterrows(): # On itère sur chacune des lignes  du data frame de référence (comparaison) et on les compare avec les variants du df actuel
            matching_rows = df[(df['CHROM'] == base_row['CHROM']) & (df['POS'] == base_row['POS'])] #récupère les lignes où il trouve les memes POS et CHROM dans les 2 df
            # Check if any of the filtered ALT sequences are similar within the pdb
            for comp_index, comp_row in matching_rows.iterrows():   #verifie si les ALT sont similaires là où les CHROM et POS sont les memes 
                if similaire(base_row['ALT'], comp_row['ALT'], pdb):
                    match_var.append(base_index) #si elle  est similaire on ajoute son index à  la listes des matches
                    break
        
        # Filter the base DataFrame to keep only the matched variants
        var_ident = var_ident.loc[match_var] #update la liste var_ident pour ne conserver que les variants dans match_var
    
    return var_ident


excel_file_path = "/mnt/c/Users/hsndk/OneDrive/Bureau/BILL/fichier_merge.xlsx"

sheet_names = ['P15', 'P30', 'P50', 'P65']

# crée une lsite de dataframes  à partir des sheet names (1 dataframe=une page du xlsx)
donnees = [pd.read_excel(excel_file_path, sheet_name=sheet, skiprows=52) for sheet in sheet_names] #skiprows=52 ignore les lignes contenant des #

#Comparaison entre P15, P30, P50, P65
variants_communs = variants_identiques(donnees[ : ], pdb=10)

#enregistre les résultats dans le meme fichier, dans une nouvelle feuille
with pd.ExcelWriter(excel_file_path, mode='a', if_sheet_exists='replace') as writer:
    variants_communs.to_excel(writer, sheet_name='Communs_A_TOUT', index=False)

#Comparaison entre P30 et P50, P65
variants_communs_apres = variants_identiques(donnees[ 1: ], pdb=10)

with pd.ExcelWriter(excel_file_path, mode='a', if_sheet_exists='replace') as writer:
    variants_communs_apres.to_excel(writer, sheet_name='Communs_Apres_Choc', index=False)

#Comparaison entre P30 et P65
variants_communs_3065 = variants_identiques([donnees[1], donnees[3]], pdb=10)

with pd.ExcelWriter(excel_file_path, mode='a', if_sheet_exists='replace') as writer:
    variants_communs.to_excel(writer, sheet_name='Communs_30_65', index=False)

#Comparaison entre P50 et P65
variants_communs_5065 = variants_identiques([donnees[2], donnees[3]], pdb=10)

with pd.ExcelWriter(excel_file_path, mode='a', if_sheet_exists='replace') as writer:
    variants_communs_5065.to_excel(writer, sheet_name='Communs_50_65', index=False)

#Comparaison entre P30 et P65
variants_communs_1565 = variants_identiques([donnees[0], donnees[3]], pdb=10)

with pd.ExcelWriter(excel_file_path, mode='a', if_sheet_exists='replace') as writer:
    variants_communs_1565.to_excel(writer, sheet_name='Communs_15_65', index=False)
#Comparaison entre P15 et P30
variants_communs_1530 = variants_identiques([donnees[0], donnees[1]], pdb=10)

with pd.ExcelWriter(excel_file_path, mode='a', if_sheet_exists='replace') as writer:
    variants_communs_1530.to_excel(writer, sheet_name='Communs_15_30', index=False)

#Comparaison entre P15 et P50
variants_communs_1550 = variants_identiques([donnees[0], donnees[2]], pdb=10)

with pd.ExcelWriter(excel_file_path, mode='a', if_sheet_exists='replace') as writer:
    variants_communs_1550.to_excel(writer, sheet_name='Communs_15_50', index=False)
#Comparaison entre P30 et P50
variants_communs_3050 = variants_identiques([donnees[1], donnees[2]], pdb=10)

with pd.ExcelWriter(excel_file_path, mode='a', if_sheet_exists='replace') as writer:
    variants_communs_3050.to_excel(writer, sheet_name='Communs_30_50', index=False)