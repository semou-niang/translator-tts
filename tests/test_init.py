"""Test initial pour vérifier le bon packaging et l'import de translator_tts."""

import translator_tts


def test_package_init() -> None:
    assert translator_tts.__version__ == "0.1.0"
