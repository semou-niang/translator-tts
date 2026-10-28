# Plan d'implémentation par phases pour Codex

> **Objet :** séquence exécutable et mesurable, sans prétendre que le travail est déjà effectué. Codex doit lire [AGENTS.md](AGENTS.md) en premier. Les tests cités sont spécifiés dans [TESTS.md](TESTS.md). **Toutes les phases sont À FAIRE au 24/10/2026.**

## Règles communes à chaque phase

Avant de modifier : inspecter dépôt, branche et fichiers, lire documents utiles ; annoncer objectif et risques ; créer/modifier uniquement les fichiers de la phase. Après modification : exécuter vérifications pertinentes, rapporter commandes et résultats exacts, enregistrer décisions/écarts. Si un test bloque le passage, corriger avant de continuer ; solliciter l'utilisateur uniquement pour secret, permission, choix réellement ambigu ou erreur bloquante. Ne pas annoncer une réussite non exécutée.

### Phase 1 — Initialisation et reproductibilité

- **Objectif :** environnement Python et structure importable.
- **Prérequis :** dépôt accessible, Python 3.12 disponible ou variante officiellement supportée.
- **Fichiers :** `requirements.txt`, `.gitignore`, `src/translator_tts/__init__.py`, répertoires `tests/`, fichiers existants conservés.
- **Tâches :** inspecter dépôt ; configurer packaging minimal `src` (ex. `pytest` avec `pythonpath = src` dans `pytest.ini` si nécessaire, à ajouter seulement si utile) ; choisir versions actuellement compatibles de Streamlit, `google-genai`, gTTS, pypdf, openpyxl, pytest, ruff ; enregistrer versions réellement installées/testées ; installer environnement ; vérifier imports ; éviter double fichier de dépendances contradictoire.
- **Tests :** commande d'import de chaque package ; `python -m pytest -q` (peut signaler absence de tests au tout début) ; `python -m ruff check .` quand fichiers présents.
- **Acceptation :** dépendances installables, imports réussis, arborescence cohérente, secrets ignorés.
- **Risques :** conflit des dépendances, chemin `src` non importable, version Python cloud incompatible.
- **Passage :** installation et imports prouvés ; sinon corriger.

### Phase 2 — Configuration et secrets

- **Objectif :** configuration centralisée sans fuite.
- **Prérequis :** phase 1 acceptée.
- **Fichiers :** `config.py`, `tests/test_config.py`, `.streamlit/secrets.toml.example`, `.gitignore`, éventuellement `.env.example` sans clés.
- **Tâches :** implémenter `Settings`, validations de bornes, priorité `GEMINI_API_KEY` env puis secrets Streamlit ; erreur de configuration claire ; modèle paramétrable ; ne pas créer de secret réel.
- **Tests :** UT-01, UT-02, UT-19, SEC-01, SEC-02 ; simuler env/Streamlit secrets sans connexion.
- **Acceptation :** cas absent/vide/present couverts, aucune clé suivie dans Git ni erreur affichée.
- **Risques :** `st.secrets` échoue si fichier absent ; état global importé trop tôt.
- **Passage :** tests de configuration réussis, aucun secret réel requis.

### Phase 3 — Validation et extraction

- **Objectif :** extraire les quatre formats et rejeter les mauvais fichiers.
- **Prérequis :** phase 2.
- **Fichiers :** `text_extraction.py`, `utils.py`, `tests/test_text_extraction.py`, `tests/test_utils.py`.
- **Tâches :** limite binaire, validations, `pypdf` pages, texte TXT BOM/UTF-8/cp1252, CSV `csv.reader`, Excel `openpyxl` toutes feuilles non vides ; messages typés ; détecter PDF sans texte ; tester XLSX corrompu/ZIP suspect ; valider seuil de caractères.
- **Tests :** UT-03..UT-12 et SEC-03 ; fixtures synthétiques minimales sans données sensibles.
- **Acceptation :** quatre formats, erreurs vides et fichiers corrompus couverts ; `pytest` hors ligne vert.
- **Risques :** encodage ambigu, PDF image, énormes feuilles XLSX, formules Excel sans caches.
- **Passage :** tests de chaque format réussis ; pas de contournement par mock d'extraction réelle.

### Phase 4 — Traduction Gemini et mocks

- **Objectif :** service de traduction séparé, testé sans Internet.
- **Prérequis :** phase 3 ; accès à la doc SDK.
- **Fichiers :** `translation.py`, `tests/test_translation.py`, éventuellement `config.py`.
- **Tâches :** implémenter abstraction injectée, prompt défensif, `genai.Client`, `models.generate_content`, réponse `.text`, vérification non vide ; mapping erreurs ; maximum deux tentatives pour erreurs transitoires ; pas de contenu sensible dans logs ; laisser le modèle configurable.
- **Tests :** UT-15..UT-21, SEC-04 ; tester injection de faux client, réponses vides, auth, quotas, timeout, entrée toxique.
- **Acceptation :** tests tous hors ligne, aucun appel réel, retour de texte et exceptions prévisibles.
- **Risques :** SDK change, noms de classes d'erreurs, modèle indisponible selon clé.
- **Passage :** mocks passent ; noter intégration réelle comme non vérifiée en attendant phase 8.

### Phase 5 — Synthèse vocale

- **Objectif :** générer un MP3 en mémoire sans relancer Gemini.
- **Prérequis :** phase 4.
- **Fichiers :** `speech.py`, `languages.py`, `tests/test_speech.py`, `tests/test_languages.py`.
- **Tâches :** intersection libellés/codes `tts_langs()`, vérification de langue, limite texte audio, dépendance gTTS injectable, `BytesIO`, validation de bytes non vides, exceptions gTTS/réseau ; nom MP3 sûr.
- **Tests :** UT-13, UT-14, UT-22..UT-26 ; **sans** appeler le service Google ; tester plusieurs codes.
- **Acceptation :** génération factice de bytes et erreurs couvertes ; aucun fichier temporaire obligatoire.
- **Risques :** variabilité des langues et service gTTS non officiel avec disponibilité variable.
- **Passage :** suite hors ligne verte et contrat `bytes` respecté.

### Phase 6 — Interface Streamlit

- **Objectif :** intégrer les widgets et l'état sans appels automatiques.
- **Prérequis :** phase 5.
- **Fichiers :** `app.py`, `tests/test_app.py`.
- **Tâches :** titre, guide court, choix de mode, zone de saisie ou uploader, aperçu éditable, langue, boutons séparés, spinner, erreurs, traduction éditable, audio, téléchargement ; gérer reruns et invalidation ; injecter services/mock UI lorsque pertinent.
- **Tests :** UI-01..UI-04, UT-02 ; revue manuelle UX.
- **Acceptation :** contrôles visibles, pas d'appels externes au rerun, invalidation déterministe.
- **Risques :** collisions clés Streamlit, état du widget modifié après instanciation.
- **Passage :** smoke UI local avec mocks, bugs rerun corrigés.

### Phase 7 — Intégration locale entre modules

- **Objectif :** parcours bout en bout simulé reproductible.
- **Prérequis :** phase 6.
- **Fichiers :** `app.py`, services, tests d'intégration mockée nécessaires.
- **Tâches :** vérifier flux TXT/PDF/CSV/XLSX -> édition -> traduction factice -> audio factice -> téléchargement ; absence d'anciennes sorties ; isoler et catégoriser les exceptions.
- **Tests :** IT-01, IT-03 (version mockée), UT régression complète.
- **Acceptation :** parcours de chaque format et téléchargement avec données de test sans réseau.
- **Risques :** état Streamlit non déterministe, encodage/unicode et types de bytes.
- **Passage :** suite hors ligne verte et commandes consignées.

### Phase 8 — Intégration externe et corrections

- **Objectif :** vérifier fonctionnement véritable avec services Gemini/gTTS.
- **Prérequis :** phase 7 ; **clé fournie exclusivement dans secrets**, Internet et droits/quotas valides.
- **Fichiers :** code et tests si corrections ; `RAPPORT_FINAL.md` au fil de l'eau.
- **Tâches :** test réel court FR/EN puis autre langue, clé invalide, connexion indisponible, erreur quota si simulable sans consommation inutile, génération/audio MP3 réel ; vérifier modèle configuré dans compte et version SDK, puis fixes ciblés.
- **Tests :** IT-02, MAN-01..MAN-04 et régression hors ligne.
- **Acceptation :** résultats réels documentés ; si clé absente, noter **bloqué/non vérifié**, ne pas falsifier le succès.
- **Risques :** coûts, quota, restrictions régionales, gTTS indisponible.
- **Passage :** réussite réelle ou blocage explicite ; ne pas déclarer projet complètement validé sans essais externes.

### Phase 9 — Durcissement, documentation et recette

- **Objectif :** qualité de livraison et documentation fidèle au code.
- **Prérequis :** phases précédentes terminées ou blocages notés.
- **Fichiers :** tous les `.md`, `.gitignore`, `requirements.txt`, tests, `RAPPORT_FINAL.md`.
- **Tâches :** revue sécurité, cohérence commandes/imports, typage, nettoyage dépendances ; vérifier que README correspond au code ; remplir matrice et rapport avec commandes/résultats vrais ; aucun secret dans Git ; pas de fonctionnalités fictives.
- **Tests :** `python -m pytest -q`, `python -m ruff check .`, `python -m ruff format --check .`, SEC-01..04, QA-01..04.
- **Acceptation :** qualité verte, documentation exacte, limites et blocages indiqués, pas de secrets.
- **Risques :** documentation obsolète, dépendances non épinglées, logs trop bavards.
- **Passage :** audit local vérifié et rapport précis.

### Phase 10 — Déploiement et vérification finale

- **Objectif :** publier et éprouver Streamlit Community Cloud.
- **Prérequis :** phase 9, accès GitHub/Cloud autorisé, secret Gemini disponible.
- **Fichiers :** `DEPLOIEMENT.md`, `RAPPORT_FINAL.md`, éventuels ajustements config/requirements.
- **Tâches :** pousser dépôt sans secret (avec autorisation), déployer `app.py`, Python cohérent, renseigner secret côté Cloud, vérifier logs sans fuite, tester PDF/TXT/CSV/XLSX et téléchargement MP3 dans l'app publiée, sauvegarder preuve/lien si disponible.
- **Tests :** MAN-05..MAN-07, régression distante + contrôles de secrets.
- **Acceptation :** URL fonctionnelle et preuve des parcours réels ; sinon marquer déploiement non réalisé et expliquer blocage.
- **Risques :** limites CPU/mémoire/cloud, variables secrètes absentes, API quota, droits de dépôt.
- **Passage :** rapport final complété, checklist signée sur faits contrôlés.

## Rapport à produire après chaque phase

```text
Phase : [numéro / titre] — statut : FAIT / PARTIEL / BLOQUÉ
État du dépôt avant modification : [branche, fichiers, contraintes]
Fichiers créés/modifiés : [...]
Décisions/écarts : [...]
Commandes exécutées exactement : [...]
Résultats de tests : [succès/échec/non exécuté + motif]
Sécurité et secrets : [contrôles réels]
Critères d'acceptation : [preuves]
Blocages/risques restants : [...]
Prochaine phase autorisée : [oui/non + justification]
```

### Prompt de reprise

« Relis AGENTS.md, PLAN_IMPLEMENTATION.md et le rapport de phase précédent ; inspecte le dépôt réel ; exécute la prochaine phase autorisée, tests compris ; corrige les échecs et rédige le rapport de phase sans inventer de résultats. »
