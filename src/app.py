import os
import streamlit as st
from dotenv import load_dotenv
import base64
from streamlit_extras.no_default_selectbox import selectbox
from streamlit_extras.add_vertical_space import add_vertical_space
from PIL import Image
from api.omdb import OMDBApi
from recsys import ContentBaseRecSys

TOP_K = 5
load_dotenv()

API_KEY = os.getenv("API_KEY")
MOVIES = os.getenv("MOVIES")
DISTANCE = os.getenv("DISTANCE")

omdbapi = OMDBApi(API_KEY)

recsys = ContentBaseRecSys(
    movies_dataset_filepath=MOVIES,
    distance_filepath=DISTANCE)

st.sidebar.title("Hi kinoMAN")
st.sidebar.info(
    """
    Ты зашел на сервис подбора фильмов. 
    Усаживайся поудобнее и подбирай себе фильм.
    Приятного вечера!!!
    """
)

st.markdown(
    """
    <style>
    body {background-color: #f7fafa;}
    h1 {color: #ff0000;text-align: center;}
    </style>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    add_vertical_space(10)

def sidebar_bg(side_bg):
    side_bg_ext = 'png'
    st.markdown(
        f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:assets/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
        unsafe_allow_html=True,
    )


side_bg = 'assets/cinema.png'
sidebar_bg(side_bg)

image = Image.open('assets/dog_pop_corn.png')
st.sidebar.image(image)


def set_bg_hack(main_bg):
    main_bg_ext = "png"

    st.markdown(
        f"""
         <style>
         .stApp {{
             background: url(data:assets/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )

main_bg = 'assets/fon.png'
set_bg_hack(main_bg)

st.markdown(
        "<h3 style='text-align: center; color: darkblue;'>Рекомендательный сервис по подбору фильмов</h3>",
        unsafe_allow_html=True)

selected_movie = st.selectbox("Выбери фильм который тебе нравится :", recsys.get_title())

if selected_movie:
    col1, col2 = st.columns([1, 4])
    film_id = recsys.get_film_id(selected_movie)
    with col1:
        poster = omdbapi.get_posters([selected_movie])
        st.image(poster[0], use_column_width=True)
    with col2:
        st.markdown("**Название фильма** : " + selected_movie + "<br>" +
                    "**Описание фильма** : " + recsys.get_film_overview(film_id),
                    unsafe_allow_html=True)

filter_col = st.columns([3, 3])
with filter_col[0]:
    selected_genre = st.selectbox("Выбери жанр : ", ['', *recsys.get_genres()])

with filter_col[1]:
    selected_rating = st.selectbox("Выбери рейтинг : ", ("Любой", "Низкий (меньше 5)", "Средний (от 5 до 7)", "Высокий (больше 7)"))

if st.button('Рекомендуем для просмотра'):
    recsys.set_filter(selected_genre, selected_rating)
    recommended_movie_names = recsys.recommendation(selected_movie, top_k=TOP_K)
    recommended_movie_posters = omdbapi.get_posters(recommended_movie_names)

    if len(recommended_movie_names) != 0:
        st.write("Варианты фильмов по запросу:")

        for index in range(1, len(recommended_movie_names) + 1):
            container = st.container()
            col1, col2 = container.columns(2)
            if index < len(recommended_movie_names):
                col1.subheader(recommended_movie_names[index])
                col1.image(recommended_movie_posters[index])
                col2.markdown("___ ")
                col2.markdown('Описание фильма: ' + str(recsys.get_field(recommended_movie_names[index], 'overview')))
                str_vote_average = 'Рейтинг фильма: ' + str(recsys.get_field(recommended_movie_names[index], 'vote_average'))
                col2.write(str_vote_average)

            else:
                col1.subheader(' ')
    else:
        st.markdown("Нет фильмов, подходящих Вашему запросу")
