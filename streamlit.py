import streamlit as st

st.set_page_config(
    page_title="Evalúa tu canción",
    page_icon="microphone",
)


# Definir los parámetros de la canción perfecta
perfect_song = {
    'album_type': True,  # Solo SINGLE es ideal
    'release_day': 17,
    'week_day': True,
    'num_artists': 6,
    'followers': 55000000,  # Promedio entre 10M y 100M
    'acousticness': 0.10,  # Promedio entre 0 y 0.20
    'danceability': 0.6,
    'energy': 0.675,  # Promedio entre 0.55 y 0.8
    'loudness': -4,
    'tempo': 120,
    'valence': 0.6,
    'explicit': False,
    'duration_sec': 215
}

def evaluate_song(song):
    differences = {}
    percentages = {}
    score = 100  # Comenzamos con 100, la puntuación perfecta

    # Calcular diferencias y porcentajes para cada parámetro
    for key, perfect_value in perfect_song.items():
        if key in song:
            current_value = song[key]
            if isinstance(perfect_value, (int, float)) and isinstance(current_value, (int, float)):
                # Calcular la diferencia y el porcentaje de desviación
                difference = abs(perfect_value - current_value)
                if perfect_value != 0:
                    percentage = (difference / perfect_value) * 100
                else:
                    percentage = 0 if difference == 0 else 100
                differences[key] = round(difference,2)
                percentages[key] = round(percentage,2)
                # Reducir el score según la desviación
                score -= percentage / len(perfect_song)

    # Normalizar el score para que esté entre 0 y 100
    score = max(0, score)

    return {
        'differences': differences,
        'percentages': percentages,
        'recommended_improvements': {k: v for k, v in sorted(percentages.items(), key=lambda item: item[1], reverse=True)},
        'popularity_score': score
}

def funcion_principal(album_type, release_day, week_day, num_artist, followers, acousticness, danceability, energy, loudness, tempo, valence, explicit, duration_sec):
    # Pedir los valores al usuario
    song_example = {
        'album_type': album_type.upper() == 'SINGLE',
        'release_day': release_day,
        'week_day': week_day == 'Friday',
        'num_artists': num_artist,
        'followers': followers,
        'acousticness': acousticness,
        'danceability': danceability,
        'energy': energy,
        'loudness': loudness,
        'tempo': tempo,
        'valence': valence,
        'explicit': explicit == 'True',
        'duration_sec': duration_sec
                }
    # Calcular evaluación para el ejemplo
    result = evaluate_song(song_example)
    st.info("**Diferencias:**")
    st.write(str(result['differences']))
    st.info("**Porcentajes:**")
    st.write(str(result['percentages']))
    st.success(f"**Popularidad esperada:** {round(result['popularity_score'], 3)}")

st.subheader("Evalúa tu canción", anchor=False)
with st.form("my_form"):
    album_type= st.selectbox("Tipo de album", ["Single","Album"])
    realease_day = st.number_input("Día de lanzamiento", min_value=1, max_value=31)
    week_day = st.selectbox("Día de la semana", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    num_artists = st.number_input("Número de artistas", min_value=1)
    followers = st.number_input("Número de seguidores", min_value=1)
    acousticness = st.number_input("Acústica", min_value=0.00, max_value=1.00)
    danceability = st.number_input("Bailabilidad", min_value=0.00, max_value=1.00)
    energy = st.number_input("Energía", min_value=0.00, max_value=1.00)
    loudness = st.number_input("Sonoridad")
    tempo = st.number_input("Tempo")
    valence = st.number_input("Pisitividad", min_value=0.0, max_value=1.0)
    explicit = st.selectbox("Explicit", [True, False])
    duration_sec = st.number_input("Duración en segundos")

    submit_button = st.form_submit_button("Submit", use_container_width=True)
    if submit_button:
        funcion_principal(album_type, realease_day, week_day, num_artists, followers, acousticness, danceability, energy, loudness, tempo, valence, explicit, duration_sec)