# Déploiement sur Streamlit Community Cloud

> **Objet :** procédure à appliquer **après** les phases 1–9. Aucun site n'a été déployé lors de la préparation de ce dossier. Références : https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy ; https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies ; https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management

## 1. Préparation locale et sécurité

1. Vérifier `python -m pytest -q`, `python -m ruff check .`, `python -m ruff format --check .` et reporter les sorties réelles.
2. Confirmer `app.py` à la racine, `requirements.txt` complet (Streamlit, google-genai, gTTS, pypdf, openpyxl ; Ruff/pytest seulement selon stratégie), imports `src` fonctionnels et Python **3.12** compatible avec versions choisies.
3. Valider le fonctionnement local sur les quatre formats, traduction et MP3 avec autorisation du compte API ; documenter les tests impossibles.
4. Inspecter `git status --short`, `git ls-files`, `.gitignore` : aucun `.streamlit/secrets.toml`, `.env`, audio ni texte privé. N'ajouter aucun fichier avec vraie clé.
5. Publier le dépôt GitHub avec les autorisations adéquates ; privilégier dépôt privé si la politique scolaire le permet. Obtenir l'autorisation avant de créer/pousser sur un dépôt distant.

## 2. Création de l'application

1. Ouvrir https://share.streamlit.io/ et se connecter via GitHub ; choisir le bon compte/organisation et dépôt, branche (p. ex. `main`) et **main file path** `app.py`.
2. Choisir un sous-domaine disponible, sans secrets dans le nom.
3. Dans **Advanced settings**, sélectionner **Python 3.12** si proposé ; la documentation Community Cloud indique que le défaut peut changer et que modifier Python après création peut imposer un nouveau déploiement.
4. Dans **Secrets**, insérer **uniquement** les valeurs TOML appropriées, par exemple `GEMINI_API_KEY = "<valeur réelle renseignée dans l'interface sécurisée>"`. La valeur illustrative n'est pas à recopier telle quelle. Ne pas afficher/coller la clé dans chat, Git ou captures.
5. Déployer et consulter logs de build/démarrage ; vérifier installation des dépendances et accès aux packages. Un `packages.txt` système n'est **pas** requis avec la pile choisie sauf preuve contraire.

## 3. Contrôle post-déploiement

| Étape | Preuve |
|---|---|
| Ouvrir URL publique/autorisée | adresse exacte, date/heure, chargement sans exception |
| Saisir texte et traduire vers deux langues | résultat visible, sens acceptable, pas d'ancien état |
| Importer TXT, PDF textuel, CSV, XLSX | extraction affichée et corrigible, traduction déclenchée sur clic |
| Générer audio | lecteur MP3 opérationnel ; pas de seconde requête Gemini |
| Télécharger MP3 | nom et MIME attendus ; MP3 lisible |
| Invalider état | changement de langue/source efface anciens résultats |
| Tester entrée vide et PDF image | message explicite, pas de crash |
| Contrôler logs et secrets | pas de clé/texte privé dans logs, secret uniquement dans console |

Reporter URL et résultats dans [RAPPORT_FINAL.md](RAPPORT_FINAL.md). Si un contrôle échoue, préciser cause, correctif et résultat du retest. Ne pas écrire « déployé » sans URL réellement accessible.

## 4. Dépannage guidé

- `ModuleNotFoundError` : revoir `requirements.txt`, paquet exact (installation `google-genai`, import `from google import genai`), chemin `src` ; vérifier cohérence locale/cloud.
- Erreur `GEMINI_API_KEY` : secret absent/mal nommé ou TOML incorrect ; corriger dans console sans imprimer la valeur.
- Modèle inaccessible/404/permission : confirmer l'identifiant actuel dans documentation et accès du compte, mettre à jour `GEMINI_MODEL`, retester ; ne pas changer silencieusement la famille sans documenter.
- HTTP 429/quota : revoir quotas et budget Gemini, informer utilisateur sans retry illimité ; l'authentification de la plateforme n'est pas impliquée.
- Timeout gTTS/indisponibilité réseau : vérifier l'accès sortant, tester brièvement et conserver la traduction sans MP3.
- Mémoire excessive : vérifier taille uploadée et quotas de traitement des PDF/XLSX ; refuser grosses entrées ; pas de cache des fichiers/audios entre utilisateurs.
- Redémarrages/reruns : état `st.session_state` non garanti après refresh ; vérifier que les téléchargements n'appellent pas les services.
- Python/version incompatible : choisir une version officiellement supportée et compatible ; selon les règles Cloud, un redéploiement peut être nécessaire pour changer Python.

## 5. Reproductibilité, coût et limites

Documenter versions réellement résolues (`python --version`, `pip freeze` si utile), branche/commit Git, modèle Gemini testé, date et auteur du contrôle, restrictions du service. Cloud, Gemini et gTTS ont disponibilités, quotas et politiques pouvant évoluer. L'hébergement public expose l'application à usage non contrôlé, potentiellement facturé côté Gemini ; définir restrictions/quotas côté fournisseur avant de diffuser publiquement, et envisager partage restreint selon l'environnement.
