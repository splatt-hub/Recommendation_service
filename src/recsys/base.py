from typing import List, Set, Optional, AnyStr
import pandas as pd
#from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.metrics.pairwise import cosine_similarity
from .utils import parse


class ContentBaseRecSys:

    def __init__(self, movies_dataset_filepath: str, distance_filepath: str):
        self.distance = pd.read_csv(distance_filepath, index_col='movie_id')
        self.distance_all = self.distance
        self.distance.index = self.distance.index.astype(int)
        self.distance.columns = self.distance.columns.astype(int)
        self._init_movies(movies_dataset_filepath)

    def _init_movies(self, movies_dataset_filepath) -> None:
        self.movies = pd.read_csv(movies_dataset_filepath, index_col='id')
        self.movies_all = self.movies
        self.movies.index = self.movies.index.astype(int)
        self.movies['genres'] = self.movies['genres'].apply(parse)

    def get_title(self) -> List[str]:
        return self.movies['title'].values

    def get_genres(self) -> Set[str]:
        genres = [item for sublist in self.movies['genres'].values.tolist() for item in sublist]
        return set(genres)

    def get_film_id(self, title:str) -> List[str]:
        return self.movies.loc[self.movies.title == title].index[0]

    def get_film_overview(self, movie_id:str) -> AnyStr:
        return self.movies.loc[movie_id].overview

    def recommendation(self, title: str, top_k: int = 5) -> List[str]:
        index_movie = pd.Series(self.movies_all.index, index=self.movies_all['title'])
        index = index_movie[title]
        similar_m = list(enumerate(self.distance[index]))
        similar_m = sorted(similar_m, key=lambda x: x[1], reverse=True)
        movie_indx = [i[0] for i in similar_m[1: top_k + 2]]

        return list(self.movies['title'].iloc[movie_indx])

    def set_filter(self, genre: str, vote: str):

        self.movies = self.movies_all
        self.distance = self.distance_all

        if genre:
            self.movies = self.movies.loc[self.movies.genres.apply(lambda x: genre in x)]
        if vote == "Низкий (меньше 5)":
            self.movies = self.movies.query('`vote_average` <5')
        if vote == "Средний (от 5 до 7)":
           self.movies = self.movies.query('`vote_average` <=7 and  `vote_average` >=5')
        if vote == "Высокий (больше 7)":
            self.movies = self.movies.query('`vote_average` >7')
        self.distance = self.distance.loc[self.movies.index]

    def get_field(self, title: str, name_field: str):

        return self.movies_all[self.movies_all['title'] == title][name_field].values[0]

