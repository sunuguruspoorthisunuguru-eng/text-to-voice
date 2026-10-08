# 🔊 Text to Voice Converter

A simple and user-friendly **Text to Voice Converter** built using **Python, Streamlit, and gTTS**.
The application converts written text into speech and allows users to listen to and download the generated audio.

## 🚀 Features

* 📝 Convert text into speech
* 🔊 Play generated voice directly in the application
* ⬇️ Download the generated voice as an MP3 file
* 🌐 Supports multiple languages
* 🎨 Simple and clean Streamlit interface
* ⚡ Easy to run locally
* 🔑 No API key required

## 🌐 Supported Languages

The application supports:

* English
* Hindi
* Telugu
* Tamil
* Kannada
* Malayalam
* French
* German
* Spanish

## 🛠️ Technologies Used

* **Python**
* **Streamlit**
* **gTTS (Google Text-to-Speech)**

## 📁 Project Structure

```text
chat-to-voice/
│
├── app.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project folder

```bash
cd chat-to-voice
```

### 3. Install required packages

```bash
python -m pip install -r requirements.txt
```

## ▶️ Run the Application

Start the Streamlit application using:

```bash
python -m streamlit run app.py
```

The application will open in your web browser.

## 🔐 API Key

**No API key is required.**

The application uses the `gTTS` library for text-to-speech conversion.

> Note: An internet connection is required because gTTS uses an online text-to-speech service.

## 💡 How to Use

1. Open the application.
2. Enter your text in the text box.
3. Select your preferred language.
4. Click **Convert to Voice**.
5. Listen to the generated audio.
6. Click **Download Voice** to save the MP3 file.

## 📦 Requirements

The project requires:

```text
streamlit>=1.40,<2
gTTS>=2.5,<3
```

These dependencies are listed in `requirements.txt`.

## 🎯 Use Cases

* Learning and education
* Listening to written content
* Language learning
* Accessibility support
* Creating simple voice content
* Converting notes into speech

## ⚠️ Note

This project requires an active internet connection for voice generation through gTTS.

## 👩‍💻 Author

**Spoorthi**

B.Tech – Artificial Intelligence and Machine Learning

---

⭐ If you find this project useful, consider giving the repository a star!
