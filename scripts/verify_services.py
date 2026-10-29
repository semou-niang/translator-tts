"""Validation manuelle opt-in ; jamais collectée par pytest et jamais appelée par l'UI."""

import argparse
from pathlib import Path

from translator_tts.config import get_api_key, load_settings
from translator_tts.speech import GTTSSpeechService
from translator_tts.translation import GeminiTranslationService
from translator_tts.utils import TranslatorTTSError


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--allow-network", action="store_true", help="Autoriser les appels externes."
    )
    parser.add_argument("--audio", action="store_true", help="Tester gTTS sans clé Gemini.")
    parser.add_argument(
        "--gemini",
        action="store_true",
        help="Autoriser trois traductions Gemini synthétiques et leur consommation de quota.",
    )
    parser.add_argument(
        "--audio-output",
        type=Path,
        help="Enregistrer volontairement le MP3 de test sous .tmp/ pour écoute manuelle.",
    )
    args = parser.parse_args()
    if not args.allow_network or not (args.audio or args.gemini):
        parser.error("Choisissez --audio ou --gemini et confirmez avec --allow-network.")
    if args.audio_output and not args.audio:
        parser.error("--audio-output nécessite --audio.")
    output = None
    if args.audio_output:
        output = args.audio_output.resolve()
        root = (Path(__file__).resolve().parents[1] / ".tmp").resolve()
        if not output.is_relative_to(root) or output.suffix.lower() != ".mp3":
            parser.error("Le fichier audio doit se trouver sous .tmp/ et porter l'extension .mp3.")
        if output.exists():
            parser.error("Le fichier de sortie existe déjà ; choisissez un nouveau nom.")
    settings = load_settings()
    failed = False
    if args.audio:
        try:
            audio = GTTSSpeechService(settings).synthesize(
                "Bonjour, ceci est un test audio du projet Translator TTS.", "fr"
            )
            print(f"gTTS français : {len(audio)} octets reçus ; écoute humaine encore requise.")
            if output:
                output.parent.mkdir(parents=True, exist_ok=True)
                with output.open("xb") as stream:
                    stream.write(audio)
                print("MP3 de test enregistré sous .tmp/ (ignoré par Git).")
        except (TranslatorTTSError, OSError):
            print("ÉCHEC gTTS : service, connexion ou écriture indisponible ; aucun succès validé.")
            failed = True
    if args.gemini:
        service = None
        try:
            key = get_api_key()
            service = GeminiTranslationService(api_key=key, settings=settings)
            # La lecture de métadonnées ne prouve pas à elle seule le droit d'inférence.
            service.client.models.get(model=settings.gemini_model)
            print("Métadonnées du modèle configuré accessibles.")
            cases = (
                ("Bonjour. Le rendez-vous est prévu demain à dix heures.", "Anglais"),
                ("Hello. The meeting is scheduled for tomorrow at ten.", "Français"),
                ("Bonjour. Merci pour votre aide.", "Espagnol"),
            )
            for source, target in cases:
                translated = service.translate(source, target)
                print(f"Gemini vers {target} : réponse reçue ({len(translated)} caractères).")
            print("Sens et qualité à vérifier dans l'interface ; aucun texte ni secret journalisé.")
        except Exception:
            # Outil de diagnostic : ne pas imprimer de payload ou exception du compte.
            print("ÉCHEC Gemini : vérifier clé, accès au modèle, réseau et quota dans AI Studio.")
            failed = True
        finally:
            if service is not None:
                try:
                    service.close()
                except TranslatorTTSError:
                    print("ÉCHEC fermeture de la connexion Gemini.")
                    failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
