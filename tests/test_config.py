"""UT-01/02 et SEC-01/02 : configuration sans réseau ni secret réel."""

from dataclasses import FrozenInstanceError
from unittest.mock import Mock

import pytest

from translator_tts.config import Settings, get_api_key, load_settings
from translator_tts.utils import ConfigurationError


def test_defaults_and_immutability():
    settings = load_settings({})
    assert settings.max_file_bytes == 5242880
    assert settings.max_source_chars == 10000
    assert settings.max_tts_chars == 5000
    assert settings.gemini_max_attempts == 2
    with pytest.raises(FrozenInstanceError):
        settings.gemini_model = "changed"


@pytest.mark.parametrize("value", [None, "", "   ", "REPLACE_ME_LOCALLY", 123, False])
def test_missing_or_invalid_secret(value):
    with pytest.raises(ConfigurationError):
        get_api_key(env={}, secrets={"GEMINI_API_KEY": value})


def test_environment_priority_without_secret_access():
    secrets = Mock()
    assert get_api_key({"GEMINI_API_KEY": " synthetic-env "}, secrets) == "synthetic-env"
    secrets.get.assert_not_called()


@pytest.mark.parametrize("value", ["", " ", "REPLACE_ME_LOCALLY"])
def test_secret_fallback(value):
    assert get_api_key({"GEMINI_API_KEY": value}, {"GEMINI_API_KEY": "synthetic"}) == "synthetic"


def test_actual_environment(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "synthetic-env")
    assert get_api_key(secrets={}) == "synthetic-env"
    monkeypatch.delenv("GEMINI_API_KEY")
    with pytest.raises(ConfigurationError):
        get_api_key(secrets={})


@pytest.mark.parametrize("error", [FileNotFoundError, PermissionError])
def test_inaccessible_streamlit_secrets(monkeypatch, error, caplog, capsys):
    import streamlit

    sentinel = "synthetic-sensitive-payload"
    secrets = Mock()
    secrets.get.side_effect = error(sentinel)
    monkeypatch.setattr(streamlit, "secrets", secrets)
    with pytest.raises(ConfigurationError) as caught:
        get_api_key(env={})
    assert sentinel not in str(caught.value)
    assert sentinel not in caplog.text
    assert sentinel not in str(capsys.readouterr())


@pytest.mark.parametrize("field", ["max_file_bytes", "max_source_chars", "max_tts_chars"])
@pytest.mark.parametrize("value", [0, -1, True, 1.5, "10", None])
def test_invalid_limits(field, value):
    with pytest.raises(ConfigurationError):
        Settings(**{field: value})


@pytest.mark.parametrize("value", [0, 3, -1, True, 1.0])
def test_retry_bound(value):
    with pytest.raises(ConfigurationError):
        Settings(gemini_max_attempts=value)


@pytest.mark.parametrize("value", ["", "  ", None, 123])
def test_invalid_model(value):
    with pytest.raises(ConfigurationError):
        Settings(gemini_model=value)


def test_audio_limit_convention():
    with pytest.raises(ConfigurationError):
        Settings(max_source_chars=10, max_tts_chars=11)


def test_environment_settings():
    settings = load_settings({"GEMINI_MODEL": " custom-model ", "GEMINI_MAX_ATTEMPTS": "1"})
    assert settings.gemini_model == "custom-model"
    assert settings.gemini_max_attempts == 1


@pytest.mark.parametrize("value", ["0", "-1", "1.5", "synthetic-sensitive-payload"])
def test_invalid_environment_limit(value):
    with pytest.raises(ConfigurationError) as caught:
        load_settings({"MAX_FILE_BYTES": value})
    assert "synthetic-sensitive-payload" not in str(caught.value)


def test_blank_environment_model_rejected():
    with pytest.raises(ConfigurationError):
        load_settings({"GEMINI_MODEL": " "})
