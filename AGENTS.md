# AGENTS.md — Instructions permanentes à Codex

> **Objectif :** agent de développement autonome, discipliné, traçable pour Translator TTS. Ce fichier constitue le point d'entrée obligatoire et la référence des travaux futurs. **La présence des fichiers de spécifications ne signifie pas que le code existe.**

## 1. Lecture préalable obligatoire

Avant toute intervention : lire complètement et dans cet ordre `AGENTS.md`, `README.md`, `SPECIFICATIONS.md`, `ARCHITECTURE.md`, `PLAN_IMPLEMENTATION.md`, `TESTS.md`, `SECURITE_ET_CONFIG.md`, `DEPLOIEMENT.md`, `RAPPORT_FINAL.md`. En cas de contradiction, signaler précisément les passages ; appliquer les règles de sécurité et les exigences obligatoires avant les préférences d'implémentation ; demander clarification seulement si la contradiction empêche une décision raisonnable.

## 2. Inspecter le dépôt réel avant modification

Vérifier les fichiers, modifications non commitées, branche, environnement, dépendances et état des tests. Ne pas écraser de travail existant, effacer un secret, modifier des fichiers hors besoin ou supposer que la structure est déjà créée. Utiliser l'arborescence d'[ARCHITECTURE.md](ARCHITECTURE.md) ou documenter et justifier un changement minimal.

## 3. Processus par phases

Suivre les **10 phases** d'[PLAN_IMPLEMENTATION.md](PLAN_IMPLEMENTATION.md) dans l'ordre, sauf dépendance justifiant explicitement un ajustement. Pour chacune : état initial, plan bref, modifications, tests, revue sécurité, rapport de phase, décision objective sur passage. Ne pas demander confirmation pour chaque fichier ou micro-opération. Ne pas poursuivre en cas de test bloquant non corrigé ou secret/permission indispensable absent. Si des accès externes ne sont pas disponibles, faire les tests hors ligne et indiquer que les validations externes restent bloquées.

## 4. Exigences de qualité et de vérité

- Implémenter les fonctionnalités réelles ; **ne jamais** remplacer une exigence par une démo, mock, pseudo-audio ou retour simulé dans le produit livré sans le déclarer explicitement comme incomplet.
- Respecter les FR/NFR et la matrice de [SPECIFICATIONS.md](SPECIFICATIONS.md). Après chaque modification, exécuter les tests pertinents, puis la suite de régression à la fin de phase ; corriger les échecs avant d'avancer.
- Ne déclarer un test « réussi » que si la commande a été exécutée et observée. Rapporter échec, non-exécution, absence d'Internet/clé et résultats partiels honnêtement.
- **Aucune clé réelle** en source, fixture, Markdown, commande partagée ou log. Ne pas demander de publier sa clé. Utiliser `.streamlit/secrets.toml` ignoré par Git ou variable d'environnement ; respecter [SECURITE_ET_CONFIG.md](SECURITE_ET_CONFIG.md).
- Séparer UI, configuration, parsing, traduction, langues, audio, validation. Eviter suringénierie, dépendances superflues, accès réseau dans tests unitaires, persistence de texte et audio.
- Documenter les décisions importantes ; si le code diverge des documents, actualiser les documents concernés, en maintenant les identifiants/critères.
- En incertitude : consulter documentation officielle actuelle de Streamlit, Gemini SDK, gTTS, pytest, dépendances ; identifier dates/versions ; ne pas inventer des API ni supposer l'accès permanent à un modèle.
- Ne pas masquer un échec dans un `try/except` global ou faire passer une erreur de service pour une traduction réussie.
- Ne pas publier de données ou pousser un dépôt distant sans permission appropriée ; l'accès aux secrets et comptes Cloud appartient à l'utilisateur.

## 5. Invariants applicatifs à maintenir

- Seul texte extrait, prévisualisé et validé peut partir vers Gemini ; jamais le fichier binaire.
- Le texte traduit est envoyé au service gTTS **seulement** au clic audio et s'il respecte la limite.
- Langue choisie compatible avec `gtts.lang.tts_langs()` ; conserver mapping label/code.
- Changer source/mode/langue efface traduction+MP3 ; modifier traduction efface MP3 ; aucune réémission réseau sur rerun Streamlit.
- Gérer fichiers malveillants, réponses vides, quotas, auth, timeout et absence de réseau sans fuite de données.
- Aucun historique persistant ni base de données en V1.

## 6. Livraison et compte rendu

Après chaque phase, fournir : numéro, statut `FAIT/PARTIEL/BLOQUÉ`, état initial, fichiers modifiés, choix, commandes et résultats réels, critères satisfaits, risques, prochaine phase autorisée. Maintenir [RAPPORT_FINAL.md](RAPPORT_FINAL.md) progressivement ; ne jamais le remplir avec des succès fictifs. Pour le déploiement, URL et smoke test réels, sinon « non réalisé ».

**Critère de stop :** demande humaine indispensable si secret/permission indisponible, spécification fondamentale incohérente, échec de test bloquant non résoluble raisonnablement ou dépense/activité externe non autorisée. Dans les autres cas, avancer de façon autonome et prudente.
