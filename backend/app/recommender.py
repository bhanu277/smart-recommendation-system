import pandas as pd
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .tmdb import get_movie_poster

DATA_DIR = Path(__file__).parent.parent / "data"

movies = pd.read_csv(DATA_DIR / "movies.csv")

movies["genres"] = movies["genres"].fillna("")

vectorizer = TfidfVectorizer(
    stop_words="english"
)

tfidf_matrix = vectorizer.fit_transform(
    movies["genres"]
)

similarity = cosine_similarity(
    tfidf_matrix,
    tfidf_matrix
)


def recommend(movie_name, top_n=10):

    matches = movies[
        movies["title"].str.contains(
            movie_name,
            case=False,
            na=False
        )
    ]

    if matches.empty:
        return {
            "error": "Movie not found"
        }

    idx = matches.index[0]

    scores = list(
        enumerate(similarity[idx])
    )

    scores = sorted(
        scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for i in scores[1:top_n + 1]:

        title = movies.iloc[i[0]]["title"]

        recommendations.append({
            "title": title,
            "genres": movies.iloc[i[0]]["genres"],
            "poster": get_movie_poster(title)
        })

    return recommendations