# Translator TTS — Capstone Generative AI & ML

Application Streamlit en français : texte saisi ou import TXT/PDF/CSV/XLSX, extraction éditable, traduction Gemini, synthèse gTTS, lecture et téléchargement MP3.

**État au 29/10/2026 : recette locale confirmée par l'utilisateur, 9/9 tests réussis.** Traduction réelle, audio/écoute/téléchargement, invalidations et quatre imports validés manuellement. Dernière suite automatisée : 145 tests réussis. Publication GitHub et déploiement public non réalisés ; URL publique encore non disponible. Voir [RAPPORT_FINAL.md](RAPPORT_FINAL.md).

## Installation locale

Python **3.12** recommandé ; environnement existant vérifié avec **3.12.10**. Les versions sont épinglées dans `requirements.txt`, qui installe aussi le package sous `src/` avec `-e .`. `pyproject.toml` décrit le packaging sans dupliquer les dépendances. La réinstallation en environnement neuf reste à valider : `ensurepip` échoue dans les répertoires temporaires privés de ce sandbox Windows.

Dans un PowerShell normal ouvert à la racine du projet :

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
if (-not (Test-Path .streamlit/secrets.toml)) {
    Copy-Item .streamlit/secrets.toml.example .streamlit/secrets.toml
}
# Éditer personnellement le fichier privé ; ne jamais publier la clé.
.venv\Scripts\python.exe -m streamlit run app.py
```

Sous Linux/macOS : `python3.12 -m venv .venv`, `source .venv/bin/activate`, `python -m pip install -r requirements.txt`, puis `python -m streamlit run app.py`. Copier l’exemple de secrets seulement si le fichier privé n’existe pas déjà.

Pile : Streamlit, SDK officiel `google-genai`, gTTS, pypdf, openpyxl, CSV/IO standard ; pytest et Ruff pour la qualité. Aucun pandas, ffmpeg, compte utilisateur ou base de données requis.

## Configurer Gemini personnellement

1. Ouvrir [Google AI Studio](https://aistudio.google.com/api-keys) et se connecter soi-même. Ne partager ni mot de passe ni code de connexion.
2. Sélectionner/créer un projet, puis créer une clé API. Importer le projet existant s’il n’est pas visible ; consulter son administrateur si les droits manquent. [Guide officiel](https://ai.google.dev/gemini-api/docs/api-key).
3. Consulter les quotas et tarifs. Ne pas activer la facturation payante sans décision explicite ; l’accès gratuit dépend du modèle et du projet.
4. Le fichier local `.streamlit/secrets.toml` est préparé avec un placeholder. L’ouvrir dans un éditeur, remplacer `REPLACE_ME_LOCALLY` par la clé et enregistrer. Alternative : définir personnellement la variable d’environnement `GEMINI_API_KEY`.
5. Vérifier `git check-ignore .streamlit/secrets.toml`, puis confirmer seulement « configuration terminée ». Ne jamais envoyer la clé ou le fichier dans le chat. Autoriser ensuite explicitement les appels réels et leur consommation de quota.

L’application lit d’abord la variable d’environnement non vide, puis les secrets Streamlit ; le placeholder est refusé. Aucune clé demandée aux visiteurs. `gemini-3.8-flash` reste le modèle par défaut, listé officiellement au 28/10/2026. La traduction réelle est confirmée par l'utilisateur ; l'identifiant exact employé pendant sa recette n'a pas été consigné. Changement possible par `GEMINI_MODEL` après vérification.

[Modèle](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash) · [SDK Python](https://googleapis.github.io/python-genai/) · [Quotas](https://ai.google.dev/gemini-api/docs/rate-limits) · [Tarifs](https://ai.google.dev/gemini-api/docs/pricing).

## Utilisation et limites

1. Choisir **Saisie** ou **Fichier**, puis saisir le texte ou importer le document.
2. Vérifier et éventuellement corriger le texte extrait ; choisir la langue cible.
3. Cliquer **Traduire**, examiner et éventuellement corriger la traduction.
4. Cliquer séparément **Générer l’audio**, écouter puis **Télécharger le MP3**.

Source, fichier, mode ou langue modifiés : traduction et audio invalidés. Traduction modifiée : audio invalidé. Aucun appel sur simple rerun. Langues en intersection avec `gtts.lang.tts_langs()`.

Limites par défaut : **5 Mio** par fichier, **10 000 caractères** source, **5 000 caractères** pour l’audio ; refus sans troncature silencieuse. PDF natifs uniquement, sans OCR ; PDF chiffrés et classeurs VBA refusés. Toutes les feuilles Excel non vides sont extraites sans exécuter de formule. Les budgets ne garantissent pas une isolation CPU/mémoire complète.

Seul le texte validé part vers Gemini ; seule la traduction validée part vers le service Google utilisé par gTTS au clic audio. MP3 en RAM, aucun historique permanent ni cache global. Les prestataires appliquent leurs politiques de rétention. `.streamlit/config.toml` désactive les statistiques et borne l’upload serveur à 5 Mio. Si `MAX_FILE_BYTES` change, ajuster aussi cette limite serveur. Voir [SECURITE_ET_CONFIG.md](SECURITE_ET_CONFIG.md).

## Vérifications

En cas d'échec, noter la référence `TR_...` affichée dans le message. Le terminal
fournit un événement sûr : `translation_failure category=TR_... http_status=...`.
Seuls une catégorie fixe et un statut numérique sont journalisés, sans texte,
fichier, clé, corps d'exception ou traceback fournisseur. Aucune erreur n'est
transformée en succès. Après autorisation d'un nouvel essai consommant du quota,
suivre « Incident TXT de 338 caractères » dans [TESTS.md](TESTS.md).

```powershell
.venv\Scripts\python.exe -m pytest -p no:cacheprovider -o addopts= -q
.venv\Scripts\python.exe -m ruff check .
.venv\Scripts\python.exe -m ruff format --check .
.venv\Scripts\python.exe -m pip check
```

Les mocks sont réservés aux tests. La suite bloque le réseau externe (loopback interne asyncio Windows autorisé). Le cache pytest est désactivé pour éviter une restriction d’accès observée. Streamlit AppTest crée un dossier privé `0700` inaccessible dans ce sandbox : les assertions passent, mais le nettoyage signale `WinError 5`. Ce diagnostic n’est pas masqué et aucune permission système n’est modifiée. Voir [TESTS.md](TESTS.md).

Outil manuel, jamais lancé par pytest ni par le produit :

```powershell
# gTTS seul, sans clé Gemini ; choisir un nouveau nom de fichier.
.venv\Scripts\python.exe scripts/verify_services.py --audio --allow-network --audio-output .tmp/recette-fr.mp3
# Après autorisation de consommation du quota Gemini :
.venv\Scripts\python.exe scripts/verify_services.py --gemini --allow-network
```

Phrases synthétiques uniquement ; métadonnées du modèle puis trois traductions. Aucun secret, texte utilisateur ou corps d’exception imprimé. L’export volontaire de diagnostic est limité à `.tmp/`, ignoré par Git, sans écrasement. La recette humaine locale est confirmée dans [TESTS.md](TESTS.md) ; une recette distincte sera nécessaire sur l'URL Cloud.

## Déploiement et références

**Non réalisé.** Après recette et accord explicite : publication GitHub autorisée, Streamlit Community Cloud, `app.py`, Python 3.12, clé uniquement dans le gestionnaire de secrets Cloud. Aucun compte connecté ni accès confirmé présumé. Procédure : [DEPLOIEMENT.md](DEPLOIEMENT.md).

Les **24 fichiers** proposés sont listés dans [PUBLICATION_FILES.txt](PUBLICATION_FILES.txt).
Les huit documents de gouvernance et de rapport restent locaux ; le README public
est préparé séparément dans la copie de publication, sans lien vers ces documents.
Le guide de déploiement sépare connexion personnelle, publication après accord,
configuration privée des secrets et lancement public après un second accord.
Aucun fichier secret local, environnement virtuel, audio ou document utilisateur
n'est inclus dans cette liste.

Le besoin Edureka est transcrit dans [SPECIFICATIONS.md](SPECIFICATIONS.md) ; le PDF original du sujet est absent du dépôt audité. Architecture : [ARCHITECTURE.md](ARCHITECTURE.md). Phases et critères : [PLAN_IMPLEMENTATION.md](PLAN_IMPLEMENTATION.md). Gouvernance : [AGENTS.md](AGENTS.md). Preuves et limites : [RAPPORT_FINAL.md](RAPPORT_FINAL.md).
