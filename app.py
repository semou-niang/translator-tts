"""Interface française : appels réseau uniquement sur actions explicites."""

import streamlit as st

from translator_tts.config import get_api_key, load_settings
from translator_tts.languages import available_languages
from translator_tts.speech import GTTSSpeechService
from translator_tts.text_extraction import extract_text
from translator_tts.translation import GeminiTranslationService
from translator_tts.utils import (
    TranslatorTTSError,
    audio_filename,
    validate_audio_text,
    validate_source_text,
)


def clear_results():
    st.session_state.translated_text = ""
    st.session_state.has_translation = False
    st.session_state.audio_bytes = None
    st.session_state.audio_text = ""


def main():
    st.set_page_config(page_title="Translator TTS", page_icon="🌐")
    st.title("Translator TTS")
    st.write("Saisissez un texte ou importez un fichier, vérifiez-le, puis choisissez une langue.")
    st.info(
        "Au clic Traduire, le texte validé est envoyé à Google Gemini. "
        "Au clic Générer l’audio, la traduction est envoyée au service Google utilisé par gTTS. "
        "L’application ne conserve aucun historique permanent. "
        "Les prestataires appliquent leurs propres politiques de conservation."
    )
    st.markdown(
        "[Confidentialité Gemini](https://ai.google.dev/gemini-api/terms) · "
        "[Confidentialité Google](https://policies.google.com/privacy)"
    )
    try:
        settings = load_settings()
        languages = available_languages()
    except TranslatorTTSError as error:
        st.error(str(error))
        return
    if "translated_text" not in st.session_state:
        clear_results()
    mode = st.radio("Source", ["Saisie", "Fichier"], key="source_mode")
    uploaded = None
    file_identity = None
    extraction_ok = True
    if mode == "Fichier":
        uploaded = st.file_uploader(
            "Fichier TXT, PDF, CSV ou XLSX (5 Mio maximum)", type=["txt", "pdf", "csv", "xlsx"]
        )
        if uploaded is not None:
            data = uploaded.getvalue()
            file_identity = (uploaded.name, data)
            if (
                file_identity != st.session_state.get("loaded_file")
                or "file_source" not in st.session_state
            ):
                # Réinitialiser avant le widget ; jamais de réextraction sur rerun identique.
                st.session_state.file_source = ""
                st.session_state.loaded_file = None
                clear_results()
                try:
                    st.session_state.file_source = extract_text(uploaded.name, data, settings)
                    st.session_state.loaded_file = file_identity
                except TranslatorTTSError as error:
                    st.error(str(error))
                    extraction_ok = False
        else:
            st.session_state.file_source = ""
            st.session_state.loaded_file = None
        source = st.text_area("Texte extrait à vérifier et modifier", key="file_source", height=200)
    else:
        source = st.text_area("Texte à traduire", key="manual_source", height=200)
    label = st.selectbox("Langue cible", list(languages), key="target_label")
    code = languages[label]
    signature = (mode, source, code, file_identity)
    if signature != st.session_state.get("source_signature"):
        clear_results()
        st.session_state.source_signature = signature
    st.caption(f"Source : {len(source)} / {settings.max_source_chars} caractères")
    source_valid = extraction_ok and (mode != "Fichier" or uploaded is not None)
    try:
        source = validate_source_text(source, settings.max_source_chars)
    except TranslatorTTSError as error:
        source_valid = False
        if source:
            st.warning(str(error))
    if st.button("Traduire", disabled=not source_valid):
        clear_results()
        try:
            key = get_api_key()
            with st.spinner("Traduction en cours…"):
                service = GeminiTranslationService(api_key=key, settings=settings)
                try:
                    st.session_state.translated_text = service.translate(source, label)
                finally:
                    service.close()
            st.success("Traduction reçue.")
            st.session_state.has_translation = True
        except TranslatorTTSError as error:
            clear_results()
            st.error(str(error))
    if st.session_state.translated_text != st.session_state.audio_text:
        st.session_state.audio_bytes = None
    if st.session_state.has_translation:
        translated = st.text_area(
            "Traduction modifiable pour l’audio", key="translated_text", height=200
        )
        if translated != st.session_state.audio_text:
            st.session_state.audio_bytes = None
        st.caption(f"Audio : {len(translated)} / {settings.max_tts_chars} caractères")
        audio_valid = True
        try:
            validate_audio_text(translated, settings.max_tts_chars)
        except TranslatorTTSError as error:
            audio_valid = False
            st.warning(str(error))
        if st.button("Générer l’audio", disabled=not audio_valid):
            st.session_state.audio_bytes = None
            try:
                with st.spinner("Génération audio en cours…"):
                    st.session_state.audio_bytes = GTTSSpeechService(settings).synthesize(
                        translated, code
                    )
                    st.session_state.audio_text = translated
                st.success("Audio généré.")
            except TranslatorTTSError as error:
                st.error(str(error))
        if st.session_state.audio_bytes:
            st.audio(st.session_state.audio_bytes, format="audio/mpeg")
            st.download_button(
                "Télécharger le MP3",
                st.session_state.audio_bytes,
                file_name=audio_filename(code),
                mime="audio/mpeg",
            )


if __name__ == "__main__":
    main()
