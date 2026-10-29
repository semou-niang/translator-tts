"""Module de configuration et gestion sécurisée des secrets pour Translator TTS."""

import os
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from translator_tts.utils import ConfigurationError

DEFAULT_GEMINI_MODEL: str = "gemini-3.8-flash"
DEFAULT_MAX_FILE_BYTES: int = 5 * 1024 * 1024  # 5 Mio = 5 242 880 octets
DEFAULT_MAX_SOURCE_CHARS: int = 10_000
DEFAULT_MAX_TTS_CHARS: int = 5_000
DEFAULT_GEMINI_MAX_ATTEMPTS: int = 2


@dataclass(frozen=True)
class Settings:
    """Paramètres applicatifs non sensibles avec validation stricte."""

    gemini_model: str = DEFAULT_GEMINI_MODEL
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES
    max_source_chars: int = DEFAULT_MAX_SOURCE_CHARS
    max_tts_chars: int = DEFAULT_MAX_TTS_CHARS
    gemini_max_attempts: int = DEFAULT_GEMINI_MAX_ATTEMPTS

    def __post_init__(self) -> None:
        if not isinstance(self.gemini_model, str) or not self.gemini_model.strip():
            raise ConfigurationError("Le modèle Gemini configuré ne peut pas être vide.")
        for name in ("max_file_bytes", "max_source_chars", "max_tts_chars", "gemini_max_attempts"):
            if type(getattr(self, name)) is not int:
                raise ConfigurationError(f"Le paramètre '{name}' doit être un entier.")
        if self.max_file_bytes <= 0:
            raise ConfigurationError(
                "La taille maximale de fichier (max_file_bytes) doit être strictement positive."
            )
        if self.max_source_chars <= 0:
            raise ConfigurationError(
                "La limite de caractères source (max_source_chars) doit être strictement positive."
            )
        if self.max_tts_chars <= 0:
            raise ConfigurationError(
                "La limite de caractères TTS (max_tts_chars) doit être strictement positive."
            )
        if self.max_tts_chars > self.max_source_chars:
            raise ConfigurationError(
                "La limite TTS (max_tts_chars) ne peut pas excéder "
                "la limite source (max_source_chars)."
            )
        if self.gemini_max_attempts not in (1, 2):
            raise ConfigurationError(
                "Le nombre maximal de tentatives Gemini "
                "(gemini_max_attempts) doit être égal à 1 ou 2."
            )


def load_settings(env: Mapping[str, str] | None = None) -> Settings:
    """Charge et valide les paramètres depuis l'environnement ou les valeurs par défaut."""
    source_env = os.environ if env is None else env

    model = source_env.get("GEMINI_MODEL", DEFAULT_GEMINI_MODEL).strip()

    def _parse_int(key: str, default: int) -> int:
        val = source_env.get(key)
        if val is None or not val.strip():
            return default
        try:
            return int(val.strip())
        except ValueError:
            raise ConfigurationError(f"Le paramètre '{key}' doit être un entier valide.") from None

    max_file_bytes = _parse_int("MAX_FILE_BYTES", DEFAULT_MAX_FILE_BYTES)
    max_source_chars = _parse_int("MAX_SOURCE_CHARS", DEFAULT_MAX_SOURCE_CHARS)
    max_tts_chars = _parse_int("MAX_TTS_CHARS", DEFAULT_MAX_TTS_CHARS)
    gemini_max_attempts = _parse_int("GEMINI_MAX_ATTEMPTS", DEFAULT_GEMINI_MAX_ATTEMPTS)

    return Settings(
        gemini_model=model,
        max_file_bytes=max_file_bytes,
        max_source_chars=max_source_chars,
        max_tts_chars=max_tts_chars,
        gemini_max_attempts=gemini_max_attempts,
    )


def get_api_key(
    env: Mapping[str, str] | None = None,
    secrets: Mapping[str, Any] | None = None,
) -> str:
    """Récupère la clé API Gemini avec ordre de priorité et validation de non-vacuité.

    Ordre de chargement :
    1. Variable d'environnement GEMINI_API_KEY (si présente et non vide).
    2. Streamlit secrets via st.secrets ou mapping injecté (si présent et non vide).
    3. ConfigurationError si aucune clé valide n'est trouvée.

    Ne consigne ni ne divulgue jamais la valeur de la clé en cas d'erreur.
    """
    source_env = os.environ if env is None else env

    # 1. Vérification dans l'environnement
    env_key = source_env.get("GEMINI_API_KEY")
    if isinstance(env_key, str) and env_key.strip() and env_key.strip() != "REPLACE_ME_LOCALLY":
        return env_key.strip()

    # 2. Vérification dans les secrets injectés ou Streamlit
    if secrets is None:
        import streamlit as st

        secrets = st.secrets

    # Streamlit signale aussi un TOML absent/illisible par FileNotFoundError.
    try:
        secret_key = secrets.get("GEMINI_API_KEY")
    except (FileNotFoundError, KeyError, OSError):
        secret_key = None
    if (
        isinstance(secret_key, str)
        and secret_key.strip()
        and secret_key.strip() != "REPLACE_ME_LOCALLY"
    ):
        return secret_key.strip()

    raise ConfigurationError(
        "Service de traduction indisponible : clé API Gemini non configurée. "
        "Définissez GEMINI_API_KEY dans l'environnement ou dans .streamlit/secrets.toml."
    )
