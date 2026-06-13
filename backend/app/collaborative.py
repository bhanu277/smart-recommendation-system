import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

movies = pd.read_csv(DATA_DIR / "movies.csv")
ratings = pd.read_csv(DATA_DIR / "ratings.csv")


def recommend_for_user(user_id, top_n=10):

    user_ratings = ratings[
        ratings["userId"] == user_id
    ]

    watched = set(
        user_ratings["movieId"]
    )

    movie_scores = (
        ratings.groupby("movieId")["rating"]
        .mean()
        .sort_values(ascending=False)
    )

    recommendations = []

    for movie_id in movie_scores.index:

        if movie_id not in watched:

            movie = movies[
                movies["movieId"] == movie_id
            ]

            if not movie.empty:

                recommendations.append({
                    "movieId": int(movie_id),
                    "title": movie.iloc[0]["title"]
                })

        if len(recommendations) >= top_n:
            break

    return recommendations