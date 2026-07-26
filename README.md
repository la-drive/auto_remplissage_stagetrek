# Auto Vœux Stagetrek

Automatise la saisie des vœux de stage sur stagetrek.univ-tours.fr à partir
d'un fichier récépissé `.xlsx`.

Ce dépôt compile automatiquement, via GitHub Actions, **un exécutable Windows
(.exe)** et **un exécutable Mac**, chacun en un seul fichier, sans que
personne n'ait besoin d'installer Python.

---

## 1. Mettre ce projet sur GitHub (à faire une seule fois)

1. Crée un compte GitHub si tu n'en as pas (gratuit) : https://github.com/join
2. Crée un nouveau dépôt (bouton "New repository"), par exemple nommé
   `auto-voeux-stagetrek`. Laisse-le public (plus simple pour partager le lien
   ensuite), ne coche aucune case d'initialisation.
3. Sur ton ordinateur, dans le dossier contenant `app.py`, `requirements.txt`
   et le dossier `.github/`, lance :

   ```bash
   git init
   git add .
   git commit -m "Premier envoi"
   git branch -M main
   git remote add origin https://github.com/TON-COMPTE/auto-voeux-stagetrek.git
   git push -u origin main
   ```

   (remplace `TON-COMPTE` par ton nom d'utilisateur GitHub)

## 2. Déclencher la compilation

La compilation se lance automatiquement dès que tu crées un "tag" de version
(ex: `v1.0.0`) :

```bash
git tag v1.0.0
git push origin v1.0.0
```

Va ensuite dans l'onglet **"Actions"** de ton dépôt GitHub : tu verras deux
builds tourner (un pour Windows, un pour Mac), ça prend 2-3 minutes.

Une fois terminé, va dans l'onglet **"Releases"** (à droite de la page
principale du dépôt) : tu y trouveras une release `v1.0.0` avec deux fichiers
téléchargeables :
- `AutoVoeuxStagetrek-Windows.exe`
- `AutoVoeuxStagetrek-Mac.zip`

**C'est le lien de cette page "Releases" que tu peux partager avec les
étudiants** (ex: `https://github.com/TON-COMPTE/auto-voeux-stagetrek/releases`).

Si tu modifies le script plus tard, il suffit de pousser un nouveau tag
(`v1.0.1`, etc.) pour déclencher une nouvelle compilation.

Tu peux aussi lancer une compilation manuellement sans tag, depuis l'onglet
Actions > "Build executables" > "Run workflow" — les fichiers seront alors
disponibles en tant qu'"artefacts" de ce run (pas sur la page Releases).

## 3. Utilisation par les étudiants

### Windows
1. Télécharger `AutoVoeuxStagetrek-Windows.exe`.
2. Double-cliquer dessus.
   - Windows affichera probablement un avertissement SmartScreen ("Windows a
     protégé votre ordinateur") car l'exécutable n'est pas signé
     numériquement (la signature coûte de l'argent). Cliquer sur
     **"Informations complémentaires"** puis **"Exécuter quand même"**.
3. Au premier lancement, une fenêtre noire (console) s'ouvre et télécharge le
   navigateur nécessaire (~150 Mo, une seule fois). Patienter.
4. Une fenêtre s'ouvre pour choisir le fichier récépissé `.xlsx`.
5. Un navigateur Chrome s'ouvre sur stagetrek : se connecter, puis revenir
   dans la fenêtre noire et appuyer sur Entrée pour lancer la saisie.

### Mac
1. Télécharger et dézipper `AutoVoeuxStagetrek-Mac.zip`.
2. Double-cliquer sur **"Lancer AutoVoeuxStagetrek.command"** (pas sur le
   fichier `AutoVoeuxStagetrek` seul).
   - macOS Gatekeeper bloquera probablement le premier lancement
     ("impossible d'ouvrir car l'éditeur ne peut pas être vérifié"), car
     l'application n'est pas signée avec un compte développeur Apple (payant,
     99$/an). Pour autoriser : **clic droit sur le fichier .command > Ouvrir**,
     puis confirmer dans la boîte de dialogue. Cela ne sera à faire qu'une fois.
3. Une fenêtre Terminal s'ouvre et télécharge le navigateur nécessaire
   (~150 Mo, une seule fois au premier lancement).
4. Une fenêtre s'ouvre pour choisir le fichier récépissé `.xlsx`.
5. Un navigateur Chrome s'ouvre sur stagetrek : se connecter, puis revenir
   dans le Terminal et appuyer sur Entrée pour lancer la saisie.

---

## Fichiers de ce dépôt

- `app.py` : le script principal (basé sur Playwright).
- `requirements.txt` : dépendances Python.
- `.github/workflows/build.yml` : la configuration qui compile
  automatiquement les exécutables Windows et Mac sur les serveurs GitHub.

## Limites à connaître

- Les exécutables ne sont pas signés numériquement (Windows/Apple font payer
  cette signature), d'où les avertissements de sécurité au premier lancement
  décrits ci-dessus — c'est normal, il suffit d'autoriser une fois.
- Le premier lancement télécharge le navigateur Chromium (~150 Mo), il faut
  donc une connexion internet correcte la première fois.
- Le site stagetrek pouvant changer de structure, si un jour la saisie
  automatique ne fonctionne plus, il faudra probablement mettre à jour les
  sélecteurs dans `app.py` (voir la fonction `add_one_wish`).
