"""gTTS vers bytes en mémoire, déclenché indépendamment de Gemini."""

import io
import logging
from typing import Protocol

from gtts import gTTS

from translator_tts.config import Settings
from translator_tts.languages import validate_language
from translator_tts.utils import SpeechError, validate_audio_text

logging.getLogger("gtts").setLevel(logging.CRITICAL)


class SpeechService(Protocol):
    def synthesize(self, text: str, language_code: str) -> bytes: ...


class GTTSSpeechService:
    def __init__(self, settings: Settings | None = None, factory=None):
        self.settings = settings or Settings()
        self.factory = factory if factory is not None else gTTS

    def synthesize(self, text: str, language_code: str) -> bytes:
        text = validate_audio_text(text, self.settings.max_tts_chars)
        validate_language(language_code)
        try:
            output = io.BytesIO()
            self.factory(
                text=text, lang=language_code, lang_check=True, timeout=(5, 20)
            ).write_to_fp(output)
            result = output.getvalue()
        except Exception:
            # Frontière fournisseur : pas d'exception brute ni audio partiel.
            raise SpeechError(
                "La génération audio a échoué. Vérifiez la connexion et réessayez."
            ) from None
        if not result:
            raise SpeechError("Le service audio a renvoyé une réponse vide.")
        return result
