# Stratégie de tests et plan de recette

> **Objet :** scénarios contrôlables avant code, permettant la traçabilité avec [SPECIFICATIONS.md](SPECIFICATIONS.md). Les tests unitaires et d'intégration simulée ne doivent demander **ni clé API ni réseau**.

## 1. Niveaux et commande

- **UT** : unitaires `pytest` et mock (`unittest.mock`/`monkeypatch`) ; testent fonctions/services isolés, aucune émission réseau.
- **IT (mockés)** : vérifient les interfaces et parcours avec Gemini et gTTS remplacés par objets factices ; hors ligne.
- **IT (réels)** : petit nombre de contrôles externes explicitement déclenchés, avec clé valide et réseau ; ne font pas partie de `pytest -q` par défaut.
- **UI** : interface Streamlit locale / `streamlit.testing` si version pertinente, sinon scénarios manuels ; mocker tous appels externes.
- **MAN** : vérifications humaines des textes, son MP3, affichage, cloud.
- **SEC** : confidentialité et invalidité de données.

Commandes prévues :

```bash
python -m pytest -q
python -m ruff check .
python -m ruff format --check .
# Intégration réelle uniquement après mise en place de tests dédiés explicitement opt-in
# Exemple, si de tels tests sont ajoutés et marqués :
python -m pytest -m external -q
```

Si des tests externes existent, configurer `pytest.ini` avec marqueur `external` et **les exclure de la collecte normale** via `addopts = -m 'not external'` ou dossiers distincts ; documenter la stratégie effectivement retenue. Bloquer le réseau dans la suite UT via mocks des clients/fonctions externes. Ne pas déclarer qu'une commande a été exécutée dans ce document.

## 2. Matrice de tests unitaires

| ID | Scénario / fixture | Attendu |
|---|---|---|
| UT-01 | `GEMINI_API_KEY` absente ou vide | `ConfigurationError`, aucun secret affiché |
| UT-02 | Variable d'env prioritaire, secrets factices, bornes config invalides | priorité et validation correctes |
| UT-03 | TXT UTF-8, UTF-8-BOM, cp1252, vide | texte exact ou erreur explicite |
| UT-04 | TXT encodage illisible/binaire et taille > 5 Mio | refus sans effet réseau |
| UT-05 | PDF texte une/deux pages | texte et ordre préservés |
| UT-06 | PDF scanné/texte absent/chiffré/tronqué | erreur extraction adaptée |
| UT-07 | CSV virgule, point-virgule, guillemets et caractères accentués | colonnes et lignes fidèles |
| UT-08 | CSV vide, mauvais encodage, structure aberrante | rejet/erreur documentée |
| UT-09 | XLSX une feuille / plusieurs feuilles | sections dans l'ordre, noms visibles |
| UT-10 | XLSX cellules vides, valeurs numériques, formule sans valeur calculée | pas de formule exécutée ; valeurs existantes lues |
| UT-11 | XLSX invalide/non ZIP/gonflé artificiellement | rejet sûr, erreur contrôlée |
| UT-12 | Fichier extension usurpée, autres formats, texte > 10000, espaces seuls | validation et limites correctes |
| UT-13 | Mapping langues et `tts_langs()` simulé | aucune langue absente de la liste de gTTS affichée |
| UT-14 | Libellés différents du code (`Français` -> `fr`), liste vide, code invalide | mapping stable et rejet déterministe |
| UT-15 | Gemini réponse simple/multiligne mockée | `.text` nettoyé légèrement et rendu |
| UT-16 | Gemini répond None, texte blanc, réponse inattendue | échec explicite sans résultat |
| UT-17 | Client Gemini exception auth/permissions | pas de retry ni fuite de clé |
| UT-18 | Quota épuisé / modèle non accessible | erreur de service présentée sans détails sensibles |
| UT-19 | Timeout/503/429 transitoire (mocks) | au plus 2 appels au total |
| UT-20 | Entrée contenant fausse instruction malveillante | prompt instruction/données séparé, aucune exécution locale |
| UT-21 | Modèle configurable, bon paramètre envoyé à `generate_content` | utilise `Settings.gemini_model` |
| UT-22 | Texte TTS vide, espaces, > 5000 | refus sans gTTS |
| UT-23 | Code langue hors `tts_langs()` | refus sans synthèse |
| UT-24 | gTTS mock écrit bytes dans `BytesIO` | sortie `bytes`, MP3 non vide |
| UT-25 | gTTS lève erreur réseau/langue | erreur applicative, pas de fichier partiel |
| UT-26 | Nom de fichier MP3 et indépendance audio/traduction | nom nettoyé, Gemini non appelé par synthèse |

## 3. Intégration, UI et manuel

| ID | Test | Précondition et preuve attendue |
|---|---|---|
| IT-01 | Passage de chaque fichier par extraction→texte édité | Fixtures locales TXT/PDF/CSV/XLSX ; contenu extrait inspecté sans réseau |
| IT-02 | Traduction courte Gemini **réelle** | Clé et réseau autorisés ; modèle accessible ; enregistrer réponse et résultat sans texte privé dans logs ; commande opt-in |
| IT-03 | Flux traduction mock→audio mock→download | Aucun appel externe ; bytes fournis au bouton téléchargement |
| UI-01 | Mode Saisie/Fichier + édition | aucun mélange de sources, aide et erreurs visibles |
| UI-02 | Changement mode, source ou langue | anciennes traduction et audio invisibles, pas de requête automatique |
| UI-03 | Modification traduction puis synthèse | ancien audio effacé ; aucune nouvelle traduction Gemini |
| UI-04 | Boutons inactifs, spinner et messages erreurs | états cohérents selon validations |
| MAN-01 | Gemini traduction réelle | sens, accents, retours à la ligne et absence de commentaire sur phrase courte |
| MAN-02 | gTTS réel plusieurs langues | lecteur joue bien MP3, prononciation intelligible et limite reconnue |
| MAN-03 | Téléchargement | nom contrôlé, extension `.mp3`, ouverture dans lecteur local |
| MAN-04 | PDF scanné, corrompu, multifeuille Excel et CSV semi-colon | comportement UX conforme sans crash |
| MAN-05 | Community Cloud accessible | URL et capture datée, entrypoint `app.py`, Python attendu |
| MAN-06 | Cloud secret et réseau | traduction, audio et téléchargement réels, pas de secret dans logs |
| MAN-07 | Retest après déploiement | parcourir tous quatre formats + changement de langue, noter erreurs |

## 4. Tests sécurité et assurance qualité

| ID | Contrôle | Critère |
|---|---|---|
| SEC-01 | Scanner dépôt suivi et `.gitignore` | `.streamlit/secrets.toml`, `.env`, MP3 absents ; exemple présent |
| SEC-02 | Erreur clé absente/invalide | UI/logs sans valeur de clé |
| SEC-03 | Entrée hostile : nom de fichier traversal, faux PDF, ZIP suspect, source contenant `ignore previous...` | aucune exécution, sortie encadrée |
| SEC-04 | Logs API et erreurs | ni prompt source, ni texte traduit, ni jeton, ni corps d'exception brut |
| QA-01 | Ruff lint et format | sortie 0, ou déviation explicitement documentée |
| QA-02 | pytest hors ligne | suite réussie sans env clé ni Internet |
| QA-03 | Traçabilité | toutes FR/NFR représentées, preuve si réalisée |
| QA-04 | Documentation et rapport | commandes reproductibles, états non fictifs, rapport à jour |

## 5. Fixtures et outillage

Créer de petits exemples **synthétiques** : PDF textuel et PDF vide générés hors tests si possible, workbook XLSX en mémoire (`openpyxl`), CSV UTF-8-BOM/cp1252, TXT Unicode, fichier corrompu, fichier grande taille factice. Les tests ne doivent contenir aucune clé réelle. Pour TTS mocker `gtts.gTTS` et `write_to_fp`; pour Gemini injecter un faux client avec méthode `models.generate_content`. Utiliser `monkeypatch` pour variables env, `Mock` et `pytest.mark.parametrize` pour tables.

## 6. Conditions de validation et limites

Un « pass » signifie commande réellement exécutée avec sortie capturée dans `RAPPORT_FINAL.md` et rapport de phase. Sans clé/réseau, seule la suite hors ligne peut être verte ; tests externes = « non exécutés », jamais « réussis ». La qualité de traduction et la prononciation exigent revue humaine, non assertions caractère par caractère. Les bugs identifiés déclenchent tests de non-régression.

**Référence :** https://docs.pytest.org/en/stable/how-to/monkeypatch.html ; https://docs.streamlit.io/develop/api-reference/app-testing
