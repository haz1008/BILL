
# Analyse des Variants Viraux

Ce projet utilise un script Python pour analyser les variations génétiques d'un virus à travers différentes passages et conditions expérimentales. Les données sont stockées et analysées à partir de fichiers Excel contenant des informations génomiques.

## Objectif

L'objectif est d'identifier les variants communs et leur évolution à travers différents passages pour comprendre comment le virus s'adapte aux changements environnementaux, tels que le choc thermique.

## Méthodologie

- **Comparaisons Séquentielles** : Analyse des séquences ALT pour trouver des variants génomiques identiques entre différents passages en tenant compte d'une tolérance de longueur de ±10 paires de bases.
- **Filtrage Basé sur les Données Excel** : Les données génomiques sont extraites de fichiers Excel, chaque feuille correspondant à un passage différent du virus.
- **Enregistrement des Résultats** : Les variants identiques trouvés sont enregistrés dans de nouvelles feuilles Excel pour une analyse ultérieure.
- **Script evolution_variant.py** : Un script Python supplémentaire est utilisé pour automatiser l'analyse des variants à travers les passages, en comparant les séquences génétiques pour identifier des similitudes et des différences significatives.

## Dépendances

- Python 3
- Pandas
- openpyxl

## Usage

1. Assurez-vous que toutes les dépendances sont installées.
2. Placez le script Python dans le même répertoire que le fichier Excel contenant les données de séquençage.
3. Exécutez le script. Les résultats seront ajoutés au fichier Excel existant sous forme de nouvelles feuilles.

## Structure du Fichier Excel

- Les données doivent être formatées avec les colonnes `CHROM`, `POS` et `ALT`, avec des informations supplémentaires dans la colonne `INFO`.
- Les premières lignes (jusqu'à 52) peuvent être ignorées si elles contiennent des métadonnées ou des en-têtes non pertinents.

## Résultats Attendus

- **Communs_A_TOUT** : Variants présents dans tous les passages analysés.
- **Communs_Apres_Choc** : Variants présents dans les passages suivant immédiatement le choc thermique.
- **Communs_[Passage1]_[Passage2]** : Variants communs entre deux passages spécifiques.

