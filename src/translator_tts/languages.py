"""Libellés UX en intersection avec les langues réellement annoncées par gTTS."""

from gtts.lang import tts_langs

from translator_tts.utils import InputValidationError

PREFERRED_LANGUAGES = {
    "Français": "fr",
    "Anglais": "en",
    "Espagnol": "es",
    "Allemand": "de",
    "Italien": "it",
    "Portugais": "pt",
    "Hindi": "hi",
    "Arabe": "ar",
    "Japonais": "ja",
    "Chinois (simplifié)": "zh-CN",
    "Coréen": "ko",
}


def available_languages() -> dict[str, str]:
    supported = tts_langs()
    languages = {label: code for label, code in PREFERRED_LANGUAGES.items() if code in supported}
    if not languages:
        raise InputValidationError("Aucune langue audio disponible dans la bibliothèque gTTS.")
    return languages


def validate_language(code: str) -> str:
    if code not in tts_langs():
        raise InputValidationError("Cette langue n'est pas disponible pour la synthèse vocale.")
    return code
