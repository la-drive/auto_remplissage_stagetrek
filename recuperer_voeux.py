import pandas as pd
from bs4 import BeautifulSoup
import os
import sys

def resource_path(relative_path):
    """ Obtenir le chemin absolu, nécessaire pour l'exécutable PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def extraire_voeux(html_file):
    """ Extrait les vœux depuis le code source HTML """
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    voeux = {}
    
    # On cherche le tableau dont l'ID commence par 'liste-preferences'
    table = soup.find('table', id=lambda x: x and x.startswith('liste-preferences'))
    if table and table.find('tbody'):
        rows = table.find('tbody').find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            # Ajuste les index (0, 1...) selon la structure réelle de ton tableau HTML
            if len(cols) >= 2:
                try:
                    rang = int(cols[0].text.strip())
                    nom_stage = cols[1].text.strip()
                    voeux[nom_stage] = rang
                except ValueError:
                    continue
    else:
        print("Avertissement : Le tableau des préférences n'a pas pu être lu depuis le HTML.")
    
    return voeux

def main():
    print("--- StageTrek Auto-Filler ---")
    html_file = input("Glissez-déposez le fichier source HTML ici puis appuyez sur Entrée : ").strip().strip("'").strip('"')
    excel_file = "modele_voeux_campagne_4-3.xlsx"
    
    if not os.path.exists(html_file):
        print("Erreur : Le fichier HTML est introuvable.")
        input("Appuyez sur Entrée pour quitter...")
        return
        
    if not os.path.exists(excel_file):
        print(f"Erreur : Le fichier {excel_file} doit être dans le même dossier que l'exécutable.")
        input("Appuyez sur Entrée pour quitter...")
        return

    # 1. Récupération des choix
    voeux_etudiant = extraire_voeux(html_file)
    
    if not voeux_etudiant:
        print("Aucun vœu extrait. Utilisation des données de test (BRETONNEAU, BOURGES...).")
        # Données de test basées sur tes informations
        voeux_etudiant = {
            "BRETONNEAU NEUROCHIRURGIE": 1,
            "BOURGES ANESTHESIOLOGIE": 2,
            "BOURGES IMAGERIE MEDICALE": 3
        }
    else:
        print(f"{len(voeux_etudiant)} vœux extraits avec succès !")

    # 2. Modification de l'Excel
    try:
        # Assure-toi d'installer openpyxl (moteur par défaut pour lire du xlsx avec pandas)
        df = pd.read_excel(excel_file)
        
        # NOTE : Adapte 'Nom_du_stage' et 'Rang' avec les vrais noms de colonnes de ton fichier Excel
        colonne_stage = 'Nom_du_stage' 
        colonne_rang = 'Rang'
        
        if colonne_rang not in df.columns:
            df[colonne_rang] = None # Création de la colonne si elle n'existe pas

        for stage, rang in voeux_etudiant.items():
            mask = df[colonne_stage].str.contains(stage, case=False, na=False)
            df.loc[mask, colonne_rang] = rang

        output_file = "voeux_campagne_REMPLIS.xlsx"
        df.to_excel(output_file, index=False)
        print(f"\nSuccès ! Fichier sauvegardé sous : {output_file}")

    except Exception as e:
        print(f"Erreur lors du traitement du fichier Excel : {e}")

    input("\nAppuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()
