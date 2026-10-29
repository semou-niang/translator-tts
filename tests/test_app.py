"""UI-01..04 : reruns Streamlit et appels strictement sur clic, services simulés."""

from pathlib import Path
from unittest.mock import Mock

import pytest
from streamlit.testing.v1 import AppTest

from translator_tts.translation import GeminiTranslationService as RealTranslationService


@pytest.fixture
def ui(monkeypatch):
    translation = Mock()
    translation.return_value.translate.return_value = "Hello world"
    audio = Mock()
    audio.return_value.synthesize.return_value = b"synthetic-audio"
    monkeypatch.setattr("translator_tts.translation.GeminiTranslationService", translation)
    monkeypatch.setattr("translator_tts.speech.GTTSSpeechService", audio)
    monkeypatch.setattr("translator_tts.config.get_api_key", lambda: "synthetic")
    app = AppTest.from_file(
        Path(__file__).resolve().parents[1] / "app.py", default_timeout=20
    ).run()
    assert not app.exception
    return app, translation, audio


def translate(app):
    app.text_area(key="manual_source").set_value("Bonjour").run()
    app.button[0].click().run()
    assert not app.exception


def test_clicks_reruns_and_edit(ui):
    app, translation, audio = ui
    assert app.button[0].disabled
    translation.assert_not_called()
    audio.assert_not_called()
    translate(app)
    assert app.text_area(key="translated_text").value == "Hello world"
    app.run()
    assert translation.return_value.translate.call_count == 1
    app.button[1].click().run()
    assert app.session_state["audio_bytes"] == b"synthetic-audio"
    app.run()
    assert audio.return_value.synthesize.call_count == 1
    app.text_area(key="translated_text").set_value("Edited").run()
    assert app.session_state["audio_bytes"] is None
    assert translation.return_value.translate.call_count == 1
    assert not app.exception


@pytest.mark.parametrize("change", ["source", "language", "mode"])
def test_invalidation(ui, change):
    app, translation, audio = ui
    translate(app)
    app.button[1].click().run()
    if change == "source":
        app.text_area(key="manual_source").set_value("Autre texte").run()
    elif change == "language":
        app.selectbox[0].set_value("Anglais").run()
    else:
        app.radio[0].set_value("Fichier").run()
    assert app.session_state["translated_text"] == ""
    assert app.session_state["audio_bytes"] is None
    assert translation.return_value.translate.call_count == 1
    assert audio.return_value.synthesize.call_count == 1
    assert not app.exception


def test_safe_error(ui):
    from translator_tts.utils import TranslationError

    app, translation, _ = ui
    translation.return_value.translate.side_effect = TranslationError("Service indisponible.")
    translate(app)
    assert app.error[0].value == "Service indisponible."
    assert app.session_state["translated_text"] == ""


def test_classified_failure_is_visible_without_stale_success(ui):
    from google.genai import errors

    from translator_tts.utils import TranslationError

    app, translation, _ = ui
    translate(app)
    app.button[1].click().run()
    # Utiliser le vrai service Python avec client simulé, sans aucun réseau.
    client = Mock()
    client.models.generate_content.side_effect = errors.APIError(
        400, {"message": "synthetic-secret-prompt-payload"}
    )
    with pytest.raises(TranslationError) as caught:
        RealTranslationService(client=client).translate("synthétique", "Français")
    translation.return_value.translate.side_effect = caught.value
    app.button[0].click().run()
    assert not app.exception
    assert "TR_REQUEST" in app.error[0].value
    assert "synthetic-secret-prompt-payload" not in app.error[0].value
    assert app.session_state["translated_text"] == ""
    assert app.session_state["audio_bytes"] is None
    assert not app.success


@pytest.mark.parametrize("extension", ["txt", "csv", "pdf", "xlsx"])
def test_file_to_download(ui, monkeypatch, extension):
    from types import SimpleNamespace

    from test_text_extraction import pdf_bytes, workbook_bytes

    app, translation, audio = ui
    fixtures = {
        "txt": "été".encode(),
        "csv": b"hello;world\nbonjour;monde",
        "pdf": pdf_bytes(("Hello",)),
        "xlsx": workbook_bytes(),
    }
    upload = SimpleNamespace(name=f"synthetic.{extension}", getvalue=lambda: fixtures[extension])
    monkeypatch.setattr("streamlit.file_uploader", lambda *args, **kwargs: upload)
    download = Mock(return_value=False)
    monkeypatch.setattr("streamlit.download_button", download)
    app.radio[0].set_value("Fichier").run()
    assert app.text_area(key="file_source").value.strip()
    translation.assert_not_called()
    app.text_area(key="file_source").set_value("Texte vérifié et corrigé").run()
    app.button[0].click().run()
    translation.return_value.translate.assert_called_once_with(
        "Texte vérifié et corrigé", "Français"
    )
    app.button[1].click().run()
    assert download.call_args.args[1] == b"synthetic-audio"
    assert download.call_args.kwargs["file_name"] == "traduction_fr.mp3"
    assert download.call_args.kwargs["mime"] == "audio/mpeg"
    app.run()
    assert translation.return_value.translate.call_count == 1
    assert audio.return_value.synthesize.call_count == 1
    assert not app.exception


def test_empty_translation_edit_clears_audio(ui):
    app, _, _ = ui
    translate(app)
    app.button[1].click().run()
    app.text_area(key="translated_text").set_value("").run()
    assert app.session_state["audio_bytes"] is None
    assert not app.exception


def test_initialization_failure_clears_outputs(ui):
    from translator_tts.utils import ConfigurationError

    app, translation, _ = ui
    translate(app)
    app.button[1].click().run()
    translation.side_effect = ConfigurationError("Vérifiez la configuration.")
    app.button[0].click().run()
    assert not app.exception
    assert app.error[0].value == "Vérifiez la configuration."
    assert app.session_state["audio_bytes"] is None
    assert app.session_state["translated_text"] == ""


def test_file_change_and_removal_clear_outputs(ui, monkeypatch):
    from types import SimpleNamespace

    app, translation, audio = ui
    upload = SimpleNamespace(name="source.txt", getvalue=lambda: b"First source")
    monkeypatch.setattr("streamlit.file_uploader", lambda *args, **kwargs: upload)
    app.radio[0].set_value("Fichier").run()
    app.button[0].click().run()
    app.button[1].click().run()
    upload = SimpleNamespace(name="source.txt", getvalue=lambda: b"Second source")
    app.run()
    assert app.text_area(key="file_source").value == "Second source"
    assert app.session_state["audio_bytes"] is None
    assert app.session_state["translated_text"] == ""
    upload = None
    app.run()
    assert app.button[0].disabled
    assert app.text_area(key="file_source").value == ""
    assert translation.return_value.translate.call_count == 1
    assert audio.return_value.synthesize.call_count == 1
    assert not app.exception
