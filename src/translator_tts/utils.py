"""Utilitaires, exceptions et validations pour Translator TTS."""


class TranslatorTTSError(Exception):
    """Exception de base pour les erreurs applicatives."""


class ConfigurationError(TranslatorTTSError):
    """Erreur liée à la configuration ou à l'absence de secret."""


class InputValidationError(TranslatorTTSError):
    """Erreur de validation des entrées utilisateur ou fichiers."""


class ExtractionError(TranslatorTTSError):
    """Erreur lors de l'extraction de texte depuis un fichier."""


class TranslationError(TranslatorTTSError):
    """Erreur survenue lors du processus de traduction."""


class SpeechError(TranslatorTTSError):
    """Erreur survenue lors de la synthèse vocale."""


def sanitize_filename(name: str) -> str:
    """Nettoie une chaîne pour en faire un nom de fichier sûr."""
    return "".join(c for c in name if c.isalnum() or c in ("-", "_")).strip()


def validate_source_text(text: str, max_chars: int = 10000) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if not text.strip():
        raise InputValidationError("Saisissez du texte avant de traduire.")
    if len(text) > max_chars:
        raise InputValidationError(f"Le texte dépasse la limite de {max_chars} caractères.")
    return text


def validate_audio_text(text: str, max_chars: int = 5000) -> str:
    return validate_source_text(text, max_chars)


def audio_filename(language_code: str) -> str:
    from translator_tts.languages import validate_language

    validate_language(language_code)
    return f"traduction_{sanitize_filename(language_code)}.mp3"
