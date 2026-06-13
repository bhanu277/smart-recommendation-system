import os
import requests

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")


def get_movie_poster(movie_name):

    clean_name = movie_name.split("(")[0].strip()

    url = (
        f"https://api.themoviedb.org/3/search/movie"
        f"?api_key={API_KEY}"
        f"&query={clean_name}"
    )

    response = requests.get(url)

    data = response.json()

    if not data.get("results"):
        return None

    poster_path = data["results"][0].get("poster_path")

    if not poster_path:
        return None

    return (
        "https://image.tmdb.org/t/p/w500"
        + poster_path
    )