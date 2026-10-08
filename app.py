import streamlit as st
import numpy as np
import librosa
import tempfile
import os

# ============================================================
# AUDIO-BASED DEEPFAKE / SYNTHETIC VOICE SCREENER
# Frontend + Backend in one Streamlit file
# ============================================================

st.set_page_config(
    page_title="Audio Deepfake Screener",
    page_icon="🎙️",
    layout="wide"
)

# ------------------------- CSS -------------------------

st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 17px;
    margin-bottom: 30px;
}

.card {
    padding: 20px;
    border-radius: 15px;
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    margin-bottom: 20px;
}

.result {
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    margin-top: 20px;
}

.upload-box {
    padding: 20px;
    border-radius: 15px;
    border: 1px dashed #64748b;
}

.small-text {
    font-size: 14px;
    color: #94a3b8;
}

</style>
""", unsafe_allow_html=True)


# ------------------------- HEADER -------------------------

st.markdown(
    '<div class="title">🎙️ Audio-Based Deepfake / Synthetic Voice Screener</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Educational AI tool for analyzing acoustic characteristics of speech recordings'
    '</div>',
    unsafe_allow_html=True
)


# ------------------------- SIDEBAR -------------------------

with st.sidebar:

    st.header("⚙️ Settings")

    threshold = st.slider(
        "Synthetic Voice Threshold",
        min_value=0,
        max_value=100,
        value=60
    )

    st.divider()

    st.subheader("About")

    st.write(
        """
        This application analyzes acoustic features such as:

        • Spectral characteristics  
        • MFCC features  
        • Zero-crossing rate  
        • Spectral centroid  
        • Energy variation  

        The result is an educational screening score.
        """
    )


# ------------------------- UPLOAD -------------------------

st.markdown(
    '<div class="card"><h3>📂 Upload Audio</h3>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload a WAV or MP3 audio recording",
    type=["wav", "mp3"]
)

st.markdown("</div>", unsafe_allow_html=True)


# ------------------------- FUNCTIONS -------------------------

def load_audio(file):

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=os.path.splitext(file.name)[1]
    )

    temp_file.write(file.getbuffer())
    temp_file.close()

    audio, sample_rate = librosa.load(
        temp_file.name,
        sr=None,
        mono=True
    )

    os.unlink(temp_file.name)

    return audio, sample_rate


def extract_features(audio, sample_rate):

    features = {}

    # Duration
    duration = librosa.get_duration(
        y=audio,
        sr=sample_rate
    )

    features["Duration"] = duration

    # RMS Energy
    rms = librosa.feature.rms(y=audio)[0]

    features["Mean RMS Energy"] = float(np.mean(rms))
    features["RMS Variation"] = float(np.std(rms))

    # Zero Crossing Rate
    zcr = librosa.feature.zero_crossing_rate(audio)[0]

    features["Zero Crossing Rate"] = float(np.mean(zcr))

    # Spectral Centroid
    centroid = librosa.feature.spectral_centroid(
        y=audio,
        sr=sample_rate
    )[0]

    features["Spectral Centroid"] = float(np.mean(centroid))

    # Spectral Bandwidth
    bandwidth = librosa.feature.spectral_bandwidth(
        y=audio,
        sr=sample_rate
    )[0]

    features["Spectral Bandwidth"] = float(np.mean(bandwidth))

    # MFCC
    mfcc = librosa.feature.mfcc(
        y=audio,
        sr=sample_rate,
        n_mfcc=13
    )

    features["MFCC Mean"] = float(np.mean(mfcc))
    features["MFCC Variation"] = float(np.std(mfcc))

    # Pitch estimation
    try:

        f0, voiced_flag, voiced_probs = librosa.pyin(
            audio,
            fmin=librosa.note_to_hz("C2"),
            fmax=librosa.note_to_hz("C7")
        )

        valid_pitch = f0[~np.isnan(f0)]

        if len(valid_pitch) > 0:
            features["Mean Pitch"] = float(np.mean(valid_pitch))
            features["Pitch Variation"] = float(np.std(valid_pitch))
        else:
            features["Mean Pitch"] = 0
            features["Pitch Variation"] = 0

    except Exception:

        features["Mean Pitch"] = 0
        features["Pitch Variation"] = 0

    return features


# ------------------------- SCREENING MODEL -------------------------

def calculate_screening_score(features):

    score = 0

    # Very low variation can sometimes indicate synthetic processing.
    if features["RMS Variation"] < 0.015:
        score += 15

    if features["MFCC Variation"] < 15:
        score += 15

    if features["Pitch Variation"] < 8:
        score += 15

    if features["Zero Crossing Rate"] < 0.02:
        score += 10

    if features["Spectral Bandwidth"] < 1500:
        score += 10

    # Higher MFCC variation generally indicates richer acoustic variation.
    if features["MFCC Variation"] > 30:
        score -= 10

    # Natural pitch variation
    if features["Pitch Variation"] > 15:
        score -= 10

    score = max(0, min(100, score))

    return score


def get_result(score, threshold):

    if score >= threshold:

        return (
            "⚠️ Potentially Synthetic",
            "The recording shows acoustic characteristics "
            "that may be consistent with synthetic or processed speech."
        )

    else:

        return (
            "✅ Likely Natural",
            "The recording shows acoustic characteristics "
            "that are more consistent with natural speech."
        )


# ------------------------- ANALYSIS -------------------------

if uploaded_file is not None:

    st.markdown(
        '<div class="card"><h3>🎧 Audio Preview</h3>',
        unsafe_allow_html=True
    )

    st.audio(
        uploaded_file,
        format="audio/wav"
    )

    st.write(
        f"**File:** {uploaded_file.name}"
    )

    st.write(
        f"**Size:** {uploaded_file.size / 1024:.2f} KB"
    )

    st.markdown("</div>", unsafe_allow_html=True)


    if st.button(
        "🔍 Analyze Audio",
        type="primary",
        use_container_width=True
    ):

        try:

            with st.spinner("Analyzing acoustic features..."):

                audio, sample_rate = load_audio(
                    uploaded_file
                )

                features = extract_features(
                    audio,
                    sample_rate
                )

                score = calculate_screening_score(
                    features
                )

                label, explanation = get_result(
                    score,
                    threshold
                )


            # -------------------------
            # RESULT
            # -------------------------

            st.markdown(
                '<div class="card"><h2>📊 Screening Result</h2>',
                unsafe_allow_html=True
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Synthetic Score",
                    f"{score}%"
                )

            with col2:
                st.metric(
                    "Sample Rate",
                    f"{sample_rate} Hz"
                )

            with col3:
                st.metric(
                    "Duration",
                    f"{features['Duration']:.2f} sec"
                )

            st.progress(score / 100)

            if score >= threshold:

                st.warning(
                    f"### {label}\n\n{explanation}"
                )

            else:

                st.success(
                    f"### {label}\n\n{explanation}"
                )

            st.markdown("</div>", unsafe_allow_html=True)


            # -------------------------
            # FEATURES
            # -------------------------

            st.markdown(
                '<div class="card"><h2>🎵 Acoustic Features</h2>',
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write(
                    f"**Duration:** "
                    f"{features['Duration']:.2f} seconds"
                )

                st.write(
                    f"**Mean RMS Energy:** "
                    f"{features['Mean RMS Energy']:.5f}"
                )

                st.write(
                    f"**RMS Variation:** "
                    f"{features['RMS Variation']:.5f}"
                )

                st.write(
                    f"**Zero Crossing Rate:** "
                    f"{features['Zero Crossing Rate']:.5f}"
                )

                st.write(
                    f"**Spectral Centroid:** "
                    f"{features['Spectral Centroid']:.2f} Hz"
                )

            with col2:

                st.write(
                    f"**Spectral Bandwidth:** "
                    f"{features['Spectral Bandwidth']:.2f} Hz"
                )

                st.write(
                    f"**MFCC Mean:** "
                    f"{features['MFCC Mean']:.2f}"
                )

                st.write(
                    f"**MFCC Variation:** "
                    f"{features['MFCC Variation']:.2f}"
                )

                st.write(
                    f"**Mean Pitch:** "
                    f"{features['Mean Pitch']:.2f} Hz"
                )

                st.write(
                    f"**Pitch Variation:** "
                    f"{features['Pitch Variation']:.2f}"
                )

            st.markdown("</div>", unsafe_allow_html=True)


            # -------------------------
            # EXPLANATION
            # -------------------------

            st.markdown(
                '<div class="card"><h2>🧠 Analysis Explanation</h2>',
                unsafe_allow_html=True
            )

            st.write(
                """
                The screener evaluates several acoustic properties of
                the uploaded recording.

                **MFCC:** Represents characteristics of the voice spectrum.

                **Pitch Variation:** Measures changes in fundamental
                frequency across speech.

                **RMS Energy:** Represents the energy level of the signal.

                **Zero Crossing Rate:** Measures how frequently the audio
                waveform crosses zero.

                **Spectral Centroid:** Indicates where the energy of the
                spectrum is concentrated.
                """
            )

            st.markdown("</div>", unsafe_allow_html=True)


            # -------------------------
            # DISCLAIMER
            # -------------------------

            st.info(
                "⚠️ Educational use only. This score is NOT proof that "
                "a recording is genuine or synthetic. Real-world deepfake "
                "detection requires a properly trained and validated "
                "machine-learning model and representative labeled data."
            )


        except Exception as e:

            st.error(
                f"❌ Error while analyzing the audio: {str(e)}"
            )

else:

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.info(
        "Upload a WAV or MP3 recording above to begin analysis."
    )

    st.markdown(
        """
        ### 🔎 How it works

        **1. Upload Audio**  
        Upload a speech recording.

        **2. Feature Extraction**  
        The application extracts acoustic features.

        **3. Screening**  
        Features are evaluated using a simple educational
        screening model.

        **4. Result**  
        The application displays a screening score and
        acoustic analysis.stre

        """,
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True) 


# ------------------------- FOOTER -------------------------

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;">
    <p>🎙️ Audio-Based Deepfake / Synthetic Voice Screener</p>
    <p class="small-text">
    Educational AI/ML Project • Acoustic Feature Analysis
    </p>
    </div>
    """,
    unsafe_allow_html=True
)