import pandas as pd
from pathlib import Path

from .recommender import recommend
from .tmdb import get_movie_poster

DATA_DIR = Path(__file__).parent.parent / "data"

movies = pd.read_csv(DATA_DIR / "movies.csv")
ratings = pd.read_csv(DATA_DIR / "ratings.csv")


def hybrid_recommend(user_id, movie_name):

    content_recs = recommend(
        movie_name,
        top_n=20
    )

    if isinstance(content_recs, dict):
        return content_recs

    popularity = (
        ratings.groupby("movieId")["rating"]
        .mean()
        .reset_index()
    )

    popularity.columns = [
        "movieId",
        "avg_rating"
    ]

    results = []

    for movie in content_recs:

        movie_row = movies[
            movies["title"] == movie["title"]
        ]

        if movie_row.empty:
            continue

        movie_id = movie_row.iloc[0]["movieId"]

        score = popularity[
            popularity["movieId"] == movie_id
        ]

        avg = (
            float(score.iloc[0]["avg_rating"])
            if not score.empty
            else 0
        )

        results.append({
            "title": movie["title"],
            "genres": movie["genres"],
            "score": round(avg, 2),
            "poster": get_movie_poster(
                movie["title"]
            )
        })

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:10]