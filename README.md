# 🌍 Translator TTS — AI-Powered Translation & Text-to-Speech

### Generative AI & Machine Learning — Edureka Capstone Project

A web application built with **Python and Streamlit** that enables users to translate text into multiple languages using **Google Gemini AI**, convert translated text into speech using **Google Text-to-Speech (gTTS)**, and download the generated audio as an MP3 file.

The project combines generative artificial intelligence, text processing, API integration, and speech synthesis in an interactive, user-friendly interface.

---

## 📌 Project Overview

**Translator TTS** is a multilingual translation application with integrated text-to-speech capabilities.

Users can enter text directly or upload a document. After extracting the text, the application uses the Google Gemini API to generate a natural, context-aware translation.

The translated text can then be converted into an MP3 audio file, played directly in the browser, or downloaded.

This project was developed as part of the **Edureka Generative AI and Machine Learning Capstone Project**.

### Project Objectives

- Apply generative artificial intelligence concepts to a practical application.
- Integrate Google Gemini into a Python application.
- Develop an interactive web interface using Streamlit.
- Implement multilingual text translation.
- Integrate text-to-speech functionality using gTTS.
- Extract and process text from different document formats.
- Apply software engineering, security, and testing best practices.

---

## ✨ Features

### 1. Multilingual Translation with Google Gemini

- Translate text into multiple languages.
- Generate context-aware and natural translations.
- Select the desired target language.
- Display translated text.
- Allow users to edit the translation.
- Handle API errors, network issues, and invalid inputs.

### 2. Document Upload and Text Extraction

The application supports four document formats:

| Format | Extension | Functionality |
|---|---|---|
| Plain Text | `.txt` | Text reading and extraction |
| PDF | `.pdf` | Text extraction from text-based PDF documents |
| CSV | `.csv` | Tabular content extraction |
| Excel | `.xlsx` | Text extraction from Excel worksheets |

Extracted content is displayed in an editable text area before translation.

**Note:** Scanned PDFs requiring Optical Character Recognition (OCR) are not supported in the current version.

### 3. Text-to-Speech with gTTS

- Convert translated text into speech.
- Generate MP3 audio.
- Play audio directly in Streamlit.
- Download generated MP3 files.
- Validate supported language codes.
- Generate audio independently of translation.

### 4. Interactive User Interface

The application includes:

- A French-language interface.
- A text input area.
- A document upload component.
- An editable preview of extracted text.
- A target-language selection menu.
- A translation button.
- A separate audio generation button.
- An integrated audio player.
- An MP3 download button.
- Processing indicators.
- Clear confirmation and error messages.

### 5. Input Validation and Security

- Empty-input validation.
- Text length validation.
- File size restrictions.
- File format validation.
- External service error handling.
- Secure Gemini API key management.
- No persistent storage of user texts or generated audio.
- Automatic invalidation of outdated results when inputs change.

---

## 🌐 Supported Languages

The application provides a selection of languages compatible with Google Text-to-Speech.

| Language | Code |
|---|---|
| French | `fr` |
| English | `en` |
| Spanish | `es` |
| German | `de` |
| Italian | `it` |
| Portuguese | `pt` |
| Hindi | `hi` |
| Arabic | `ar` |
| Japanese | `ja` |
| Simplified Chinese | `zh-CN` |
| Korean | `ko` |

Actual language availability is validated against the installed gTTS library.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Main programming language |
| Streamlit | Web application framework |
| Google Gemini API | AI-powered translation |
| Google Gen AI SDK | Gemini API integration |
| gTTS | Text-to-speech synthesis |
| pypdf | PDF text extraction |
| openpyxl | Excel file processing |
| csv | CSV file processing |
| pytest | Automated testing |
| Ruff | Code linting and formatting |
| Git & GitHub | Version control |
| Streamlit Community Cloud | Planned cloud deployment |

### AI Model

The application uses the official `google-genai` Python SDK.

The Gemini model is configurable, allowing the application to adapt to models available through Google AI Studio.

The initially configured model is `gemini-3.8-flash`. Model availability, quotas, and billing conditions should be verified for the relevant Google project.

---

## 🏗️ Project Architecture

Translator TTS follows a modular architecture that separates the user interface from business logic and external services.

```text
translator-tts/
│
├── app.py
├── README.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
│
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
│
├── src/
│   └── translator_tts/
│       ├── __init__.py
│       ├── config.py
│       ├── languages.py
│       ├── translation.py
│       ├── text_extraction.py
│       ├── speech.py
│       └── utils.py
│
├── scripts/
│   └── verify_services.py
│
└── tests/
    ├── conftest.py
    ├── test_app.py
    ├── test_config.py
    ├── test_translation.py
    ├── test_text_extraction.py
    └── test_speech.py
```

### Module Responsibilities

| Module | Responsibility |
|---|---|
| `app.py` | Streamlit user interface and interactions |
| `config.py` | Application configuration and settings |
| `languages.py` | Language selection and validation |
| `translation.py` | Google Gemini API integration |
| `text_extraction.py` | Document text extraction |
| `speech.py` | Text-to-speech and MP3 generation |
| `utils.py` | Input validation and utility functions |
| `tests/` | Automated tests |

This architecture improves maintainability, testability, and code organization.

---

## 🔄 Application Workflow

```text
                   USER
                    |
                    v
           STREAMLIT APPLICATION
                    |
          +---------+---------+
          |                   |
          v                   v
       TEXT INPUT         FILE UPLOAD
                              |
                              v
                       TEXT EXTRACTION
          |                   |
          +---------+---------+
                    |
                    v
             INPUT VALIDATION
                    |
                    v
          TARGET LANGUAGE SELECTION
                    |
                    v
              GOOGLE GEMINI API
                    |
                    v
              TRANSLATED TEXT
                    |
                    v
                gTTS SERVICE
                    |
                    v
                MP3 AUDIO
                    |
            +-------+-------+
            |               |
            v               v
       AUDIO PLAYBACK     MP3 DOWNLOAD
```

Translation and audio generation are separate actions, allowing users to review and edit the translated text before generating speech.

---

## 💻 Local Installation

### Prerequisites

Before installation, make sure you have:

- Python 3.12 or another version compatible with the project dependencies.
- Git installed.
- An Internet connection.
- A Google Gemini API key.
- PowerShell, Git Bash, or another supported terminal.

### 1. Clone the Repository

```bash
git clone https://github.com/semou-niang/translator-tts.git
cd translator-tts
```

### 2. Create a Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Linux or macOS:

```bash
python3 -m venv .venv
```

### 3. Activate the Virtual Environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Linux or macOS:

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e . --no-deps
```

The editable installation makes the `translator_tts` package located in the `src/` directory available to Python.

---

## 🔑 Google Gemini API Configuration

A Gemini API key is required to perform real translations.

### 1. Generate an API Key

1. Visit [Google AI Studio](https://aistudio.google.com/apikey).
2. Sign in with your Google account.
3. Create or select a Google project.
4. Generate an API key.
5. Review the applicable usage quotas and billing conditions.

### 2. Configure the API Key Locally

Inside the `.streamlit` directory, create a file named:

```text
secrets.toml
```

You can copy the example configuration:

```powershell
Copy-Item .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Then configure your API key:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

Replace the placeholder with your actual API key.

### ⚠️ Security Notice

**Never commit or publish your API key on GitHub.**

The `.streamlit/secrets.toml` file must remain private and excluded from Git tracking.

Never share API keys, passwords, or access tokens in commits, issues, logs, or screenshots.

The application also supports the `GEMINI_API_KEY` environment variable.

---

## ▶️ Running the Application

From the project root directory, with the virtual environment activated, run:

```bash
python -m streamlit run app.py
```

Streamlit will display a local address, typically:

```text
http://localhost:8501
```

Open the URL in your web browser to access Translator TTS.

---

## 📖 User Guide

### Step 1 — Enter Text or Upload a Document

Enter text directly into the application.

Example:

```text
Bonjour. Je suis heureux de découvrir cette application.
```

Alternatively, choose the file upload option and upload a TXT, PDF, CSV, or XLSX document.

### Step 2 — Review Extracted Text

When uploading a document, the application extracts and displays its text.

You can review and edit the extracted content before translation.

### Step 3 — Select the Target Language

Choose a target language from the dropdown menu.

Example: **English**.

### Step 4 — Translate the Text

Click the **Traduire (Translate)** button.

The application sends the validated input to Google Gemini.

A possible translation of the example is:

```text
Hello. I am happy to discover this application.
```

The exact output may vary depending on the Gemini model and context.

### Step 5 — Generate Speech

Click **Générer l'audio (Generate Audio)**.

The application converts the translated text into speech using gTTS and generates an MP3 file.

### Step 6 — Play or Download the Audio

Use the integrated audio player to listen to the result.

Click **Télécharger le MP3 (Download MP3)** to save the audio file to your device.

---

## 🧪 Testing and Code Quality

The project includes an automated test suite built with `pytest`.

Tests cover:

- Application configuration.
- Input validation.
- TXT, PDF, CSV, and XLSX extraction.
- Gemini translation using mocked clients.
- Speech synthesis using mocked services.
- Supported language validation.
- API and network error handling.
- Streamlit application interactions.
- Audio download behavior.
- Invalidation of outdated translation and audio results.

### Run Automated Tests

```bash
python -m pytest -p no:cacheprovider -o addopts= -q
```

### Run Ruff Linting

```bash
python -m ruff check .
```

### Check Code Formatting

```bash
python -m ruff format --check .
```

### Documented Test Results

During the local technical audit on October 28, 2026:

- **116 automated tests passed.**
- Ruff linting and formatting checks passed.
- The local Streamlit server passed its availability check.

Subsequent manual tests confirmed successful Gemini translation, real gTTS audio generation, audio playback, and MP3 downloads.

However, an intermittent translation error was also observed during file-upload testing. Therefore, successful short-text translation does not establish that every translation scenario is fully validated.

Automated tests use mocks for external services and can run without a real API key.

---

## 🔒 Security and Privacy

Translator TTS follows several security practices:

- No hardcoded API keys in Python source code.
- Environment-based and Streamlit secrets configuration.
- Input validation before processing.
- File format and size restrictions.
- Rejection of invalid input.
- Controlled error messages.
- No user database.
- No persistent application history.
- In-memory MP3 generation.
- Automatic invalidation of outdated results.

### External Services and Data Processing

Text submitted for translation is transmitted to Google Gemini.

Translated text submitted for speech synthesis is transmitted to the service used by gTTS.

Both services require network communication and may be subject to their respective privacy policies, usage restrictions, and retention practices.

Users should avoid uploading confidential or sensitive information without first reviewing the applicable provider policies.

---

## ☁️ Deployment on Streamlit Community Cloud

Translator TTS is designed for deployment on **Streamlit Community Cloud**.

### Requirements

- A GitHub repository containing the application source code.
- A Streamlit Community Cloud account.
- A valid Gemini API key.

### Deployment Steps

1. Push the application source code to GitHub without including secrets.
2. Visit [Streamlit Community Cloud](https://share.streamlit.io/).
3. Sign in using GitHub.
4. Create a new application.
5. Select the `semou-niang/translator-tts` repository.
6. Choose the published branch (`main` or `master`).
7. Set `app.py` as the application entry point.
8. Configure `GEMINI_API_KEY` using Streamlit Community Cloud's secrets management interface.
9. Deploy the application.
10. Test translation, audio generation, playback, and MP3 downloads using the public URL.

**Deployment status:** Public deployment should be considered unverified until the application is accessible through a working Streamlit Cloud URL and its essential features have been tested.

---

## ⚠️ Known Limitations

### Scanned PDF Documents

PDF documents containing only scanned images require OCR, which is not included in the current version.

### Internet Connectivity

Google Gemini and gTTS rely on external services.

Network failures, proxy restrictions, or service unavailability can prevent successful translation or speech generation.

### API Quotas and Usage Costs

Gemini usage is subject to the quotas, rate limits, and possible charges associated with the configured Google project.

### Document Size Limits

The application restricts input sizes to prevent excessive processing.

The initial configuration includes:

- Maximum uploaded file size: 5 MiB.
- Maximum translation input length: 10,000 characters.
- Maximum text-to-speech input length: 5,000 characters.

### Translation Accuracy

AI-generated translations may contain linguistic inaccuracies or lose contextual nuances.

Users should review translations when accuracy is important.

### Voice Customization

gTTS provides basic speech synthesis and does not offer the advanced voice customization available in professional text-to-speech platforms.

---

## 🚀 Future Improvements

Potential enhancements include:

- OCR support for scanned PDF files.
- Automatic source-language detection.
- Optional source-language selection.
- Batch processing for larger documents.
- Support for additional languages.
- Integration with advanced speech synthesis providers.
- Multiple voice options where supported.
- Accessibility improvements.
- Enhanced diagnostics for external service failures.

These improvements are not part of the guaranteed functionality of the current version.

---

## 📚 Official Documentation and Resources

- [Python](https://www.python.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Google Gen AI Python SDK](https://googleapis.github.io/python-genai/)
- [Google AI Studio](https://aistudio.google.com/)
- [gTTS Documentation](https://gtts.readthedocs.io/)
- [pypdf Documentation](https://pypdf.readthedocs.io/)
- [openpyxl Documentation](https://openpyxl.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Streamlit Community Cloud](https://docs.streamlit.io/deploy/streamlit-community-cloud)

---

## 👨‍💻 Author

**Semou Niang**

Generative AI and Machine Learning — Capstone Project

**Edureka**

GitHub: [semou-niang/translator-tts](https://github.com/semou-niang/translator-tts)

---

## 🎯 Conclusion

Translator TTS demonstrates how generative artificial intelligence technologies can be integrated into a practical Python web application.

By combining Google Gemini, Streamlit, and gTTS, the project provides a straightforward workflow:

**Enter or Upload Text → Translate → Generate Speech → Listen → Download MP3**

The application demonstrates key skills in Python programming, generative AI integration, document processing, API communication, automated testing, application security, and web deployment.

---

*Educational project developed as part of the Edureka Generative AI & Machine Learning Capstone Program.*
