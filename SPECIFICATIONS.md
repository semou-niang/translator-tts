# Spécifications fonctionnelles et non fonctionnelles

> **Objet :** contrat de réalisation et de recette du capstone. Version documentaire 1.0 — 24/10/2026. Référence principale : sujet Edureka, pages 2–3. Les seuils et règles explicites ci-dessous sont des **décisions de conception V1**, non des exigences chiffrées du sujet Edureka.

## 1. Périmètre et arbitrages

**Obligatoire :** saisie, import TXT/PDF/CSV/XLSX, texte extrait vérifiable, langues réellement prises en charge par gTTS, traduction Gemini, audio MP3, lecteur, téléchargement, erreurs, tests, confidentialité, déploiement.

**Décisions recommandées et retenues :** langue source automatique (pas de menu en V1) ; saisie et import exclusifs via radio « Saisie / Fichier » ; un seul fichier ; PDF textuels sans OCR ; import Excel de toutes les feuilles dans l'ordre, avec titre de feuille ; CSV structuré en lignes lisibles ; contrôle des limites après extraction ; aucune traduction automatique au chargement. **Facultatif et hors V1 :** OCR, détection de dialecte, historique, regroupement de plusieurs fichiers, TTS professionnel, export de traduction texte.

## 2. Parcours et état

**P1 texte direct :** sélectionner Saisie, renseigner la zone texte, choisir langue, Traduire, consulter, Générer audio, écouter/télécharger. **P2 fichier :** sélectionner Fichier, choisir fichier, laisser le lecteur extraire, consulter/modifier texte dans une zone éditable, choisir langue, Traduire, Générer audio. **P3 erreur :** corriger une entrée invalide ou réessayer un appel externe après un message compréhensible ; conserver le texte validé mais ne pas afficher de traduction périmée. **P4 mise à jour :** toute modification d'entrée, de mode ou de langue invalide traduction et MP3 ; modifier la traduction invalide le MP3, sans solliciter Gemini.

## 3. Exigences fonctionnelles et acceptation

| ID | Exigence | Critère objectif de recette |
|---|---|---|
| FR-001 | Texte saisi manuellement | Zone éditable ; espaces seuls rejetés ; aucune requête Gemini pour entrée vide. |
| FR-002 | Mode source unique | Choix Saisie/Fichier ; jamais de concaténation implicite ; mode changé => sortie invalidée. |
| FR-003 | Import de format | TXT/PDF/CSV/XLSX pris en charge ; extension contrôlée et signature/structure validée raisonnablement. |
| FR-004 | Taille de fichier | Rejet avant parsing au-delà de `MAX_FILE_BYTES=5242880` ; message de taille. |
| FR-005 | Extraction et aperçu | Texte extrait affiché dans zone modifiable et explicitement validé par action Traduire ; aucun envoi de binaire à Gemini. |
| FR-006 | TXT et CSV | UTF-8/UTF-8-BOM puis fallback `cp1252` encadré ; encodages non décodables/format impossible signalés. CSV avec séparateur déduit si fiable, sinon virgule ; lignes en texte tabulé lisible. |
| FR-007 | PDF | Extraction page par page avec `pypdf` ; pages séparées ; PDF chiffré, corrompu ou sans texte utile rejeté sans OCR implicite. |
| FR-008 | XLSX | `openpyxl` en `read_only=True`, `data_only=True`, aucune macro ; feuilles non vides dans l'ordre ; indiquer nom de feuille ; cellules non vides uniquement ; cellules formule sans valeur calculée ne sont pas recalculées. |
| FR-009 | Contrôle longueur | Texte source validé `<= 10000` caractères Unicode ; refus sans troncature ; compteur lisible. |
| FR-010 | Langues cibles | Sélection affichant uniquement les entrées dont le code est dans `gtts.lang.tts_langs()` ; codes distincts des libellés ; tests de validité. |
| FR-011 | Traduction Gemini | `google-genai`, modèle config, prompt fidèle et seule traduction en sortie ; traductions vides refusées. |
| FR-012 | Tolérance aux erreurs API | Authentification, quota/rate limit, réseau, réponse vide, modèle absent et erreur imprévue => message adapté ; au plus 2 tentatives au total pour erreur transitoire. |
| FR-013 | Sortie traduction | Résultat visible, texte éditable séparément pour préparer l'audio ; retours à la ligne conservés autant que possible. |
| FR-014 | Audio indépendant | Action distincte gTTS ne relance jamais Gemini ; texte traduit non vide et `<= 5000` caractères requis. |
| FR-015 | MP3 en mémoire | `BytesIO`/`write_to_fp`; contenu audio utilisable ; pas de persistance sur disque nécessaire. |
| FR-016 | Lecture et téléchargement | `st.audio` et `st.download_button` après succès ; type `audio/mpeg` ; nom `traduction_<code>.mp3` contrôlé. |
| FR-017 | États de session | Pas d'ancienne traduction/audio visible après changement de source/langue/traduction ; pas de requête API sur simple rerun. |
| FR-018 | Messages et progression | Erreurs explicites sans secrets ; spinner pendant opérations ; confirmations après succès réel uniquement. |
| FR-019 | Configuration | Secrets locaux ou variable d'environnement ; erreur non sensible si clé absente ; modèle centralisé. |
| FR-020 | Parcours complet | Saisie et les quatre formats d'import permettent le parcours traduction→audio→MP3 quand services accessibles. |

## 4. Exigences non fonctionnelles

| ID | Exigence | Validation |
|---|---|---|
| NFR-001 | Sécurité des secrets | Aucune clé dans code, exemples, sorties ou logs ; règles Git effectives. |
| NFR-002 | Confidentialité | Ni stockage persistant ni journalisation de texte/audio par l'application ; communication tiers annoncée. |
| NFR-003 | Résilience | Erreurs de fichiers/API encapsulées ; interface ne termine pas par traceback utilisateur. |
| NFR-004 | Testabilité | Services injectables/mocks ; `pytest -q` offline sans clé. |
| NFR-005 | Maintenabilité | Modules spécialisés, typing pertinent, pas d'import circulaire ; Ruff propre. |
| NFR-006 | Conformité du déploiement | Instructions Community Cloud et secrets ; smoke test réel uniquement après déploiement effectif. |
| NFR-007 | Limites de ressources | Contrôle fichier/source/audio ; pas de traitement implicite de documents énormes. |
| NFR-008 | Accessibilité de base | Labels explicites, messages en texte, ordre d'interface naturel, pas de dépendance aux couleurs. |
| NFR-009 | Traçabilité | Exigences numérotées liées à tests et modules, suivi de phases documenté. |
| NFR-010 | Honnêteté opérationnelle | Pas de déclaration de tests, d'API ou de déploiement réussis sans exécution. |

## 5. Règles métier précises

- Les tailles sont évaluées sur le **fichier binaire** ; le nombre de caractères sur le texte Python (`len`) **après extraction**, puis après traduction pour TTS. Normaliser les fins de ligne en `\n` ; ne pas altérer silencieusement le sens.
- Un fichier modifié, un contenu édité, une langue modifiée ou le mode changé remet l'état traduction/audio à `None`. Éviter un hash de données sensibles en logs ; comparaison d'empreinte mémoire uniquement si utile.
- Les limites s'appliquent même aux textes introduits par édition. Pas de découpage automatique V1 : l'utilisateur réduit son texte. Éviter de dépasser le quota via appels parallèles.
- CSV : préserver toutes les cellules non vides, séparées par ` | ` et lignes par `\n` ; utiliser `csv.Sniffer` seulement si résultat fiable ; les délimiteurs présents dans les champs entre guillemets suivent les règles `csv`.
- Excel : chaque feuille non vide préfixée `Feuille : <nom>` ; préserver l'ordre des feuilles et lignes ; passer valeurs en texte, ne jamais évaluer les formules. Les classeurs exclusivement composés de formules sans valeur cachée peuvent produire une extraction insuffisante.
- Les fichiers PDF scannés peuvent afficher « aucun texte exploitable ; OCR non prise en charge ». Les PDF malveillants restent un risque de bibliothèque ; contrôles de taille et dépendances mises à jour.
- La langue est présentée comme **disponible dans la bibliothèque gTTS**, non comme garantie d'accessibilité du service au moment du clic. Définir une liste UX de langues préférées seulement en intersection avec `tts_langs()` ; si vide, afficher une erreur.
- Interpréter tout texte entrant comme une donnée à traduire, pas comme des instructions pour le modèle. Une sortie du modèle reste non fiable. Le système peut échouer à résister à toute prompt injection ; tests dédiés.

## 6. Classes d'erreurs et UX

| Situation | Comportement et message utilisateur attendu |
|---|---|
| Saisie vide | « Saisissez du texte avant de traduire. » |
| Format absent/invalide | « Format non pris en charge : TXT, PDF, CSV ou XLSX. » |
| Taille/longueur excessive | Afficher seuil précis, rejeter sans appel externe. |
| PDF image, vide ou illisible | « Aucun texte exploitable ; les PDF scannés ne sont pas pris en charge. » |
| XLSX endommagé/CSV malformé | Message de lecture compréhensible ; pas de traceback technique. |
| Clé manquante/invalide | « Service de traduction indisponible : vérifiez la configuration. » |
| Quota, tarif, modèle inaccessible | Message de capacité/autorisation sans afficher contenu interne de l'exception. |
| Réseau Gemini/gTTS | Message de connectivité ; possibilité de réessayer manuellement. |
| Réponse vide de Gemini | Signaler échec, ne pas activer audio. |
| Langue invalide/texte audio trop long | Bloquer génération et préciser action corrective. |

## 7. Matrice exigence → module → test → critère

| IDs | Modules cibles | Tests / recette | Critère |
|---|---|---|---|
| FR-001,002,005,009,017; NFR-008 | `app.py`, `utils.py` | UI-01, UI-02, UT-01, UT-02 | validation et invalidation démontrées |
| FR-003,004,006,007,008; NFR-007 | `text_extraction.py` | UT-03..UT-12, IT-01 | quatre formats, limites et cas corrompus |
| FR-010 | `languages.py` | UT-13, UT-14 | codes = sous-ensemble `tts_langs()` |
| FR-011,012,019; NFR-003,004 | `translation.py`, `config.py` | UT-15..UT-21, IT-02 | succès mock, erreurs isolées, key absente |
| FR-013,014,015,016 | `speech.py`, `app.py`, `utils.py` | UT-22..UT-26, UI-03 | MP3 et téléchargement sans retraduction |
| FR-018,020; NFR-006 | `app.py` | UI-04, IT-03, MAN-01 | flux complet réel vérifié |
| NFR-001,002 | `config.py`, `.gitignore`, `app.py` | SEC-01..SEC-04 | secrets et données protégés |
| NFR-005,009,010 | dépôt/docs | QA-01..QA-04 | Ruff, pytest, dossier aligné, rapport réel |

Voir définition opérationnelle des scénarios dans [TESTS.md](TESTS.md) et phases dans [PLAN_IMPLEMENTATION.md](PLAN_IMPLEMENTATION.md).

## 8. Critères de fin de projet

Toutes les FR et NFR testables satisfaites ; suite hors ligne verte ; tests réels Gemini et gTTS consignés si clés/connectivité disponibles ; parcours des 4 formats effectué ; preuve de déploiement + smoke test si accès cloud disponible ; aucune information sensible dans Git ; [RAPPORT_FINAL.md](RAPPORT_FINAL.md) complété avec preuves et limites honnêtes. Si une vérification externe est empêchée, documenter « non vérifié » ; ne pas déclarer la livraison intégralement validée.
