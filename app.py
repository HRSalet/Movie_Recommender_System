import time
import streamlit as st
import pandas as pd
import pickle
import requests

session = requests.Session()
session.headers.update({"User-Agent": "MovieApp/1.0"})


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": "d47ebc3110af351efd65f415240c01ef",
        "language": "en-US"
    }
    for attempt in range(3):
        try:
            responce = session.get(url, params=params, timeout=10)
            responce.raise_for_status()
            data = responce.json()
            poster_path = data.get('poster_path', None)
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        except requests.exceptions.RequestException:
            if attempt < 2:
                time.sleep(1)
                continue
            raise


# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


with open('movie_dict.pkl', 'rb') as f:
    movies_dict = pickle.load(f)

movies = pd.DataFrame(movies_dict)

st.title('Movie Reccomender System')

with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

option = st.selectbox('Enter movie name?', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(option)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
