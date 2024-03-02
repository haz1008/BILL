#!/usr/bin/env python3
import pandas as pd
def extract_info_value(info_str, key): #fonction pour extraire la colonne INFO 
    for part in info_str.split(';'): #on split l'information en fonction des ;
        if part.startswith(f'{key}='): #si le premier élément de la chaîne commence par notre clé 
            try:
                return float(part.split('=')[1]) #on retourne le nombre aprés = (donc valeur du AF)
            except ValueError:
                return None
    return None  # retouurne NONE si la clé n'existe pas

def is_similar_length(len1, len2, tolerance=10):
    return abs(len1 - len2) <= tolerance

def find_common_variants(donnees):
    common_variants = donnees[0][['CHROM', 'POS', 'INFO']].copy()  # Starting point
    
    for df in donnees[1:]:
        common_variants = common_variants.merge(df[['CHROM', 'POS', 'INFO']], on=['CHROM', 'POS'], how='inner', suffixes=('', '_next'))
        
        # Filter variants by comparing SVLEN within tolerance
        common_variants = common_variants[common_variants.apply(lambda row: is_similar_length(extract_info_value(row['INFO'], 'SVLEN'), extract_info_value(row['INFO_next'], 'SVLEN')), axis=1)]
        
        # Drop the 'INFO_next' column after comparison
        common_variants.drop('INFO_next', axis=1, inplace=True)
    
    return common_variants

def analyze_increasing_af(common_variants, donnees):
    increasing_af_variants = []
    
    
    for _, variant in common_variants.iterrows(): #pour chaque ligne dans common_variant
        af_values = [extract_info_value(variant['INFO'], 'AF')]  # On récupère les AF actuels
        
        
        for df in donnees[1:]: #  Pour chaque passage suivant
            row = df[(df['CHROM'] == variant['CHROM']) & (df['POS'] == variant['POS'])].iloc[0]
            af_values.append(extract_info_value(row['INFO'], 'AF'))
        
        if all(earlier <= later for earlier, later in zip(af_values, af_values[1:])): #  Si la fréquence est dans l'ordre croissant 
            increasing_af_variants.append(variant) # on ajoute la variante à la liste
    
    return pd.DataFrame(increasing_af_variants)

excel_file_path = "/mnt/c/Users/hsndk/OneDrive/Bureau/BILL/fichier_merge.xlsx"
sheet_names = ['P15', 'P30', 'P50', 'P65']

donnees = [pd.read_excel(excel_file_path, sheet_name=sheet, skiprows=52) for sheet in sheet_names]

common_variants = find_common_variants(donnees)

variants_with_increasing_af = analyze_increasing_af(common_variants, donnees)

# Save the results to a new sheet in the Excel file
with pd.ExcelWriter(excel_file_path, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
    variants_with_increasing_af.to_excel(writer, sheet_name='Common_Inc_AF', index=False)
