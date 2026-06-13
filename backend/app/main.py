from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .hybrid import hybrid_recommend

from .recommender import recommend
from .collaborative import recommend_for_user
from .tmdb import get_movie_poster

app = FastAPI(
    title="Smart Recommendation System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "Smart Recommendation System Running"
    }

@app.get("/recommend/{movie}")
def get_recommendations(movie: str):
    return recommend(movie)

@app.get("/user/{user_id}")
def user_recommendations(user_id: int):
    return recommend_for_user(user_id)
@app.get("/hybrid/{user_id}/{movie}")
def hybrid(user_id: int, movie: str):
    return hybrid_recommend(user_id, movie)
@app.get("/poster/{movie}")
def poster(movie: str):
    return {
        "poster": get_movie_poster(movie)
    }
