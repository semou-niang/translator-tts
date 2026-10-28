# Sécurité, confidentialité et configuration

> **Objet :** règles obligatoires de protection des données et de configuration. À appliquer dès la phase 1. Voir [ARCHITECTURE.md](ARCHITECTURE.md) et [TESTS.md](TESTS.md).

## 1. Secrets et ordre de priorité

Nom canonique : `GEMINI_API_KEY`. Chargement : (1) variable d'environnement si définie et non vide ; (2) `.streamlit/secrets.toml` via mécanisme `st.secrets` (accès tolérant à l'absence de fichier) ; (3) erreur `ConfigurationError`. Ne pas écrire la clé, même partielle, ni une URL l'incluant dans une exception visible. Ne jamais demander à l'utilisateur final de saisir ou publier sa clé sur le site déployé.

Créer pendant la phase 2 :

```toml
# .streamlit/secrets.toml.example — PUBLIC, PLACEHOLDER SEULEMENT
GEMINI_API_KEY = "REPLACE_ME_LOCALLY"
```

Copier localement en `.streamlit/secrets.toml` et remplacer le placeholder hors Git. Dans Community Cloud, configurer le secret de même nom dans le panneau sécurisé, pas dans GitHub. Tester clé absente, clé vide, secret inaccessible ; aucune requête réseau.

## 2. Configuration non sensible (décisions V1)

| Paramètre | Défaut recommandé | Validation |
|---|---|---|
| `GEMINI_MODEL` | `gemini-3.8-flash` | identifiant non vide ; confirmer accessibilité réelle |
| `MAX_FILE_BYTES` | `5242880` | entier strictement positif |
| `MAX_SOURCE_CHARS` | `10000` | entier strictement positif |
| `MAX_TTS_CHARS` | `5000` | entier strictement positif, <= source par convention (pas une obligation fournisseur) |
| `GEMINI_MAX_ATTEMPTS` | `2` | entier dans 1..2 |

Implémenter dans `config.py` avec valeurs par défaut sûres, éventuellement variables d'environnement pour l'administration. Éviter d'exposer un écran public de configuration. Prioriser la simplicité : valeurs constantes si la configuration env devient trop coûteuse, mais maintenir un seul endroit de vérité.

## 3. `.gitignore` minimal requis

```gitignore
.venv/
venv/
__pycache__/
*.py[cod]
.pytest_cache/
.ruff_cache/
.coverage
htmlcov/
.env
.env.*
!.env.example
.streamlit/secrets.toml
*.log
.DS_Store
*.mp3
.tmp/
tmp/
```

**Attention :** `.streamlit/secrets.toml.example` **doit rester suivi** ; ne pas exclure tout le répertoire `.streamlit/`. Auditer Git (`git status --short`, `git ls-files`) pour vérifier qu'aucun secret n'est suivi. Si une clé fuit : révocation/rotation immédiate ; nettoyage Git suivant procédure approuvée.

## 4. Frontières de confiance et données sortantes

1. Le navigateur transmet les textes/fichiers au serveur Streamlit ; leur contenu peut être conservé temporairement en RAM dans la session. Éviter cache global et logs bruts.
2. Seul le **texte source validé** est envoyé à Gemini via `google-genai` ; **jamais le fichier binaire** ou son nom.
3. Le **texte traduit validé** est envoyé au service externe appelé par gTTS pour générer l'audio ; ne pas présenter gTTS comme moteur hors ligne.
4. Le MP3 reste en bytes mémoire dans la session et est transmis au navigateur pour lecture/téléchargement. Effacer les références après changement d'entrée ou fermeture de session (selon comportement Streamlit, pas garantie d'effacement immédiat RAM).
5. Informer clairement l'utilisateur de ces transferts et des politiques des prestataires ; ne pas promettre zéro conservation du côté fournisseurs, ni chiffrement de bout en bout au-delà de ce qui est vérifié.

## 5. Entrées non fiables et protections

- Autoriser **uniquement** TXT, PDF, CSV, XLSX. Extension et inspection de structure/signature lorsque possible ; les extensions ne sont pas une preuve de sûreté.
- Contrôler taille **avant** parsing ; `5 Mio` max par fichier ; pas d'accès au chemin local provenant du nom fourni par l'utilisateur. Les XLSX ZIP bomb et PDF pathologiques restent un risque : budget de traitement/limitation d'itérations en plus de la taille compressée ; mise à jour régulière des packages.
- Ne jamais ouvrir de macro, évaluer de formule Excel, lancer des commandes, suivre automatiquement des liens dans documents, traiter le texte source comme du HTML ou des instructions système.
- Protéger contre prompt injection : séparer instruction système et texte source, refuser de divulguer des informations de configuration ; résultat non garanti, vérifier avec tests malveillants.
- Pas de noms utilisateur réutilisés pour fichiers téléchargés ; fabriquer `traduction_<code_langue>.mp3` où code est issu d'une allowlist et nettoyé.
- Interdire sortie audio si traduction vide ou > 5000 caractères ; désactiver boutons non pertinents ; pas de sauvegarde systématique de MP3.

## 6. Gestion des erreurs et journalisation

Messages non techniques côté UI. Logs sans texte source, traduction, audio, URL avec token, clé, stack trace brut des fournisseurs. Les exceptions réelles peuvent contenir des payloads : ne pas appeler `st.exception(exception)` sur erreur d'authentification/API. Capturer erreurs attendues par classes d'application et offrir une relance manuelle. Tests de non-divulgation requis (`SEC-01..04`).

## 7. Gouvernance et limites

Pas d'identité utilisateur, d'historique, de base de données, de télémétrie, de téléchargement de documents originaux ni de sauvegarde cloud additionnelle. Le fournisseur Gemini et l'endpoint gTTS ont leurs propres termes, quotas, disponibilité et règles de confidentialité à contrôler avant diffusion publique. Restreindre accès au dépôt et aux paramètres cloud. Politique de rétention opérationnelle des hébergeurs hors du contrôle de l'application : ne pas la confondre avec l'absence d'historique applicatif.

**Références :** https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management ; https://ai.google.dev/gemini-api/docs/api-key ; https://gtts.readthedocs.io/en/latest/module.html
