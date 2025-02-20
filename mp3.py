import streamlit as st
from gtts import gTTS
import tempfile

# Diccionario con palabras a traducir
diccionario = {
    # Agrega aquí tus traducciones
    # 'a': 'uno ',
    # 'b': 'dos ',
    # 'c': 'tres ',
    # 'd': 'cuatro ',
    # 'e': 'cinco ',
    # 'f': 'seis ',
    # 'g': 'siete ',
    # 'mi': 'ri ',
    # 'tuyo': 'tu ',
    # 'mío': 'mi ',
}

def traducir_oracion(oracion):
    palabras = oracion.split()
    oracion_traducida = " ".join([diccionario.get(palabra.lower(), palabra) for palabra in palabras])
    return oracion_traducida

def reproducir_audio(texto, lang):
    tts = gTTS(text=texto, lang=lang, slow=False)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
        tts.save(tmp.name)
        return tmp.name  # Retorna la ruta del archivo temporal

st.title("Texto a Voz")

# Estado de la sesión para la traducción
if 'oracion_traducida' not in st.session_state:
    st.session_state.oracion_traducida = ""
if 'audio_file_path' not in st.session_state:
    st.session_state.audio_file_path = ""

# Opción para introducir texto
oracion_usuario = st.text_area("Introduce una oración :", height=200)

# Botón para ejecutar la traducción
if st.button("ir"):
    if oracion_usuario:
        oracion_traducida = traducir_oracion(oracion_usuario)
        st.session_state.oracion_traducida = oracion_traducida
        st.session_state.audio_file_path = reproducir_audio(oracion_traducida, 'es')  # Usando español por defecto

# Reproducir el audio si existe
if st.session_state.audio_file_path:
    st.audio(st.session_state.audio_file_path, format='audio/mp3')

    # Botón para descargar el archivo de audio
    with open(st.session_state.audio_file_path, 'rb') as audio_file:
        st.download_button(
            label="Descargar audio en MP3",
            data=audio_file,
            file_name="audio.mp3",
            mime="audio/mp3"
        )
