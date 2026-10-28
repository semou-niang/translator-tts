# Rapport final — modèle à compléter pendant le développement

> **Objet :** documenter exclusivement les réalisations **effectives**. **État initial au 24/10/2026 : documentation de spécifications préparée ; aucun code applicatif, test réel ou déploiement déclaré.** Ne pas modifier cet avertissement avant d'avoir les preuves adéquates.

## 1. Identification

- Projet : Translator TTS — Capstone Generative AI & ML
- Date du rapport final : En cours (28/10/2026)
- Commit / branche / environnement : Branche master (non encore commitée) / Windows / venv .venv
- Python / versions des bibliothèques : Python 3.12.10 ; streamlit==1.66.1, google-genai==2.33.0, gTTS==2.5.4, pypdf==6.21.4, openpyxl==3.1.5, pytest==9.2.0, ruff==0.17.3
- Modèle Gemini réellement utilisé : À tester (prévu : `gemini-3.8-flash`)
- URL Streamlit Cloud : NON DÉPLOYÉ

## 2. Résumé exécutif

**À RENSEIGNER selon code et essais observés.** Indiquer ce qui marche, ce qui manque et les principaux risques, sans confondre documentation et réalisation.

## 3. Fonctionnalités réalisées

| Fonctionnalité | État réel | Preuve / test / problème |
|---|---|---|
| Saisie texte et validations | NON IMPLÉMENTÉ | à renseigner |
| TXT | NON IMPLÉMENTÉ | à renseigner |
| PDF texte | NON IMPLÉMENTÉ | à renseigner |
| CSV | NON IMPLÉMENTÉ | à renseigner |
| XLSX / multiples feuilles | NON IMPLÉMENTÉ | à renseigner |
| Langues gTTS | NON IMPLÉMENTÉ | à renseigner |
| Traduction Gemini | NON IMPLÉMENTÉ | à renseigner |
| Génération MP3 gTTS | NON IMPLÉMENTÉ | à renseigner |
| Lecteur/téléchargement | NON IMPLÉMENTÉ | à renseigner |
| Confidentialité/état de session | NON IMPLÉMENTÉ | à renseigner |
| Déploiement cloud | NON RÉALISÉ | à renseigner |

## 4. Architecture finale

**À COMPLÉTER :** lien au diagramme et inventaire effectif des modules ; divergences justifiées vis-à-vis d'[ARCHITECTURE.md](ARCHITECTURE.md). Ne pas présenter l'architecture *cible* comme architecture déjà livrée.

## 5. Installation et exploitation réellement vérifiées

```text
Commandes d'installation exécutées :
- python -m venv .venv
- .venv\Scripts\python.exe -m pip install streamlit google-genai gTTS pypdf openpyxl pytest ruff
- .venv\Scripts\python.exe -m pip install -e . --no-deps
Commande de démarrage local : NON EXÉCUTÉE (Phase 6)
Version Python vérifiée : Python 3.12.10 (AMD64 sur Windows)
Gestion de secrets : NON VÉRIFIÉE (Phase 2)
```

Mettre ensuite les **commandes exactes** exécutées, OS, versions et dates, conformément à [README.md](README.md).

## 6. Tests réellement exécutés

| Date | Phase | Commande / scénario | Résultat exact | Preuve |
|---|---|---|---|---|
| 28/10/2026 | 1 | Import des packages (`streamlit`, `google.genai`, `gtts`, `pypdf`, `openpyxl`, `pytest`, `translator_tts`) | Succès | Sortie console sans erreur, versions résolues |
| 28/10/2026 | 1 | `python -m pytest -q` | 1 passed in 0.03s | Sortie pytest avec `test_init.py` (vérification version) |
| 28/10/2026 | 1 | `python -m ruff check .` | All checks passed! | Code de retour 0 |
| 28/10/2026 | 1 | `python -m ruff format --check .` | 3 files already formatted | Code de retour 0 |
| — | — | Gemini réel | NON EXÉCUTÉ | — |
| — | — | gTTS réel | NON EXÉCUTÉ | — |
| — | — | Community Cloud smoke test | NON EXÉCUTÉ | — |

Pour chaque test : numéro dans [TESTS.md](TESTS.md), statut PASSED/FAILED/SKIPPED/NOT RUN, sortie ou résumé fidèle, correctif et retest. **Ne pas inventer de couverture ni nombre de tests.**

## 7. Difficultés, écarts et risques

- Difficultés concrètes : **À RENSEIGNER**.
- Décisions d'architecture modifiées et justification : **À RENSEIGNER**.
- Limites connues : PDF scannés hors OCR V1 ; fidélité de traduction non garantie ; gTTS requiert Internet ; autres limites observées : **À RENSEIGNER**.
- Problèmes ouverts / tâches non réalisées : **À RENSEIGNER**.
- Considérations confidentialité, coût/quota et clé : **À VÉRIFIER**.

## 8. Améliorations futures (non obligatoires)

OCR opt-in pour PDF image ; choix optionnel de langue source ; traitement de gros documents par lots sous validation ; optimisation d'UX/accessibilité ; TTS professionnel seulement si besoin validé. Ne pas les attribuer à la V1.

## 9. Checklist de livraison à mettre à jour

- [ ] Code présent et exécutable localement
- [ ] Fonctionnalités FR-001..020 implémentées et vérifiées
- [ ] NFR-001..010 satisfaites ou limitations documentées
- [ ] Entrées TXT/PDF/CSV/XLSX et erreurs testées
- [ ] Suite pytest **hors ligne** exécutée et verte
- [ ] Ruff lint/format vérifiés
- [ ] Gemini réel testé avec clé autorisée
- [ ] gTTS réel et MP3 joué/téléchargé
- [ ] Secrets absents de Git et des logs
- [ ] Documentation à jour et matrice de traçabilité contrôlée
- [ ] URL cloud réellement testée (ou blocage consigné)
- [ ] Rapport final validé par preuves

## 10. Historique des phases

| Phase | Statut réel | Date | Résultat des tests | Blocage | Rapport de phase |
|---|---|---|---|---|---|
| 1 | FAIT | 28/10/2026 | Imports OK, pytest 1 passed, ruff check/format OK | Aucun | Phase 1 complétée avec succès |
| 2–10 | À FAIRE | — | NON EXÉCUTÉS | — | — |

**État initial documenté uniquement.** La conclusion finale sera rédigée après travaux et contrôle des preuves.
