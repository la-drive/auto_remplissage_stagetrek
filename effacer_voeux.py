"""
effacer_voeux.py
--------------
Automatise la suppression de tous les voeux de stage présents sur stagetrek.univ-tours.fr
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
    print("=== Auto Vœux Stagetrek - EFFACEUR DE VŒUX ===\n")
    ensure_browser_installed()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=300000)
        context = browser.new_context()
        page = context.new_page()
        
        # Redirection vers la page contenant la liste des voeux
        page.goto("https://stagetrek.univ-tours.fr/mes-stages")

        pause_avant_fermeture(
            "\n>>> Connecte-toi dans la fenêtre du navigateur.\n"
            ">>> Va sur la page 'Mes préférences' où se trouve ton classement actuel.\n"
            ">>> Reviens ici et appuie sur Entrée pour LANCER LA SUPPRESSION DE TOUS LES VŒUX.\n"
            "/!\\ ATTENTION : Cette action effacera un par un tout le classement visible à l'écran /!\\"
        )

        voeux_supprimes = 0
        while True:
            # Sélecteur ciblant précisément le bouton de suppression de la ligne
            selecteur_suppr = "a[data-event='event-supprimer-preference']"
            
            boutons = page.locator(selecteur_suppr)
            
            # S'il n'y a plus aucun bouton de suppression sur la page, la boucle s'arrête
            if boutons.count() == 0:
                break
                
            print("-> Suppression d'un vœu...")
            
            # On clique sur le tout premier bouton de suppression trouvé dans le tableau
            boutons.first.click()
            
            # Attente et gestion de la pop-up de confirmation avec patience extrême (3 minutes)
            try:
                # Cherche spécifiquement le bouton "Oui" avec l'ID confirmBtn dans la modale
                modal_submit = page.locator(".modal.show #confirmBtn")
                modal_submit.first.wait_for(state="visible", timeout=300000)
                
                # Clique pour valider la suppression
                modal_submit.first.click()
                
                # On attend que la pop-up disparaisse de l'écran, signifiant que la suppression est envoyée
                page.wait_for_selector(".modal.show", state="hidden", timeout=300000)
                
                # Petite pause pour laisser le tableau se mettre à jour en arrière-plan via AJAX
                page.wait_for_timeout(10000)
                
            except PWTimeout:
                # S'il n'y a pas de pop-up ou de rafraichissement clair, on attend simplement
                print("   (Lenteur extrême détectée de la part du site, le script patiente...)")
                page.wait_for_timeout(20000)
            
            voeux_supprimes += 1

        print(f"\nTerminé ! {voeux_supprimes} vœux ont été supprimés avec succès.")
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
