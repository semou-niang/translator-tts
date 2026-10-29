"""UT-13/14/22..26 : gTTS factice, aucune connexion Google."""

from unittest.mock import Mock

import pytest

from translator_tts.languages import available_languages
from translator_tts.speech import GTTSSpeechService
from translator_tts.utils import InputValidationError, SpeechError, audio_filename


def test_language_intersection(monkeypatch):
    monkeypatch.setattr("translator_tts.languages.tts_langs", lambda: {"fr": "French", "zz": "X"})
    assert available_languages() == {"Français": "fr"}
    monkeypatch.setattr("translator_tts.languages.tts_langs", lambda: {})
    with pytest.raises(InputValidationError):
        available_languages()


@pytest.mark.parametrize("text,code", [(" ", "fr"), ("x" * 5001, "fr"), ("ok", "../../bad")])
def test_invalid_input(text, code):
    factory = Mock()
    with pytest.raises(InputValidationError):
        GTTSSpeechService(factory=factory).synthesize(text, code)
    factory.assert_not_called()


@pytest.mark.parametrize("code", ["fr", "en", "ja"])
def test_audio_memory_and_filename(code):
    factory = Mock()
    factory.return_value.write_to_fp.side_effect = lambda stream: stream.write(b"synthetic-audio")
    assert GTTSSpeechService(factory=factory).synthesize("hello", code) == b"synthetic-audio"
    assert audio_filename(code) == f"traduction_{code}.mp3"
    assert factory.call_args.kwargs["timeout"] == (5, 20)


def test_no_partial_audio_or_error_leak(caplog):
    factory = Mock()

    def fail(stream):
        stream.write(b"partial")
        raise RuntimeError("synthetic-sensitive-payload")

    factory.return_value.write_to_fp.side_effect = fail
    with pytest.raises(SpeechError) as caught:
        GTTSSpeechService(factory=factory).synthesize("hello", "fr")
    assert "synthetic-sensitive-payload" not in str(caught.value) + caplog.text


def test_empty_audio():
    with pytest.raises(SpeechError):
        GTTSSpeechService(factory=Mock()).synthesize("hello", "fr")


def test_invalid_filename():
    with pytest.raises(InputValidationError):
        audio_filename("../../bad")
