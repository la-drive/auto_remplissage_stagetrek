"""
recuperer_voeux.py
--------------
Automatise la récupération et la sauvegarde des voeux de stage présents sur stagetrek.univ-tours.fr
"""

import sys
import os
import traceback
from pathlib import Path

_DOSSIER_NAVIGATEURS = str(Path.home() / ".cache" / "auto-voeux-stagetrek" / "playwright-browsers")
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = _DOSSIER_NAVIGATEURS

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

def pause_avant_fermeture(message="\nAppuie sur Entrée pour fermer cette fenêtre..."):
    try:
        input(message)
    except EOFError:
        pass

def ensure_browser_installed():
    print("Vérification du navigateur nécessaire (Chromium)...")
    try:
        from playwright.__main__ import main as playwright_cli_main
    except Exception as e:
        raise RuntimeError(f"Impossible de préparer Playwright : {e}")

    old_argv = sys.argv
    exit_code = 0
    try:
        sys.argv = ["playwright", "install", "chromium"]
        try:
            playwright_cli_main()
        except SystemExit as e:
            exit_code = e.code
    finally:
        sys.argv = old_argv

    if exit_code not in (0, None):
        raise RuntimeError("L'installation du navigateur a échoué.")

def run():
    print("=== Auto Vœux Stagetrek - RÉCUPÉRATEUR DE VŒUX ===\n")
    ensure_browser_installed()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        context = browser.new_context()
        page = context.new_page()
        
        # Redirection vers la page contenant la liste des voeux
        page.goto("https://stagetrek.univ-tours.fr/mes-stages")

        pause_avant_fermeture(
            "\n>>> Connecte-toi dans la fenêtre du navigateur.\n"
            ">>> Va sur la page 'Mes préférences' où se trouve ton classement actuel.\n"
            ">>> Reviens ici et appuie sur Entrée pour LANCER LA RÉCUPÉRATION DES VŒUX.\n"
        )

        print("-> Analyse de la page en cours...")
        
        # --- DÉBUT DE LA LOGIQUE D'EXTRACTION ---
        # Tu devras peut-être ajuster ce sélecteur en fonction du code HTML du site
        # Ici, on part du principe que les vœux sont dans les lignes (tr) du tableau principal
        selecteur_voeux = "tbody tr" 
        
        lignes = page.locator(selecteur_voeux)
        nombre_voeux = lignes.count()
        
        if nombre_voeux == 0:
            print("Aucun vœu n'a été trouvé à l'écran. Vérifie que tu es sur la bonne page.")
        else:
            print(f"-> {nombre_voeux} vœux trouvés. Sauvegarde en cours...")
            
            nom_fichier = "mes_voeux_sauvegardes.txt"
            
            with open(nom_fichier, "w", encoding="utf-8") as f:
                f.write("=== MES VŒUX STAGETREK ===\n\n")
                
                for i in range(nombre_voeux):
                    # Récupère tout le texte de la ligne, en nettoyant les espaces superflus
                    texte_voeu = lignes.nth(i).inner_text().strip()
                    # Remplace les sauts de ligne internes par des espaces ou des tirets pour plus de lisibilité
                    texte_voeu_propre = " | ".join(texte_voeu.splitlines())
                    
                    ligne_finale = f"Vœu {i+1} : {texte_voeu_propre}\n"
                    f.write(ligne_finale)
                    print(f"  - Vœu {i+1} sauvegardé.")
                    
            print(f"\nTerminé ! Tes vœux ont été exportés dans le fichier : {nom_fichier}")
        
        pause_avant_fermeture("\nAppuie sur Entrée pour fermer le navigateur.")
        browser.close()

def main():
    try:
        run()
    except SystemExit:
        raise
    except Exception:
        print("\nUne erreur inattendue est survenue :\n")
        traceback.print_exc()
        pause_avant_fermeture("\nAppuie sur Entrée pour fermer.")
        sys.exit(1)

if __name__ == "__main__":
    main()
