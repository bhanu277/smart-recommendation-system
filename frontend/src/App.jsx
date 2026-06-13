import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [movie, setMovie] = useState("");
  const [userId, setUserId] = useState("1");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const recommend = async () => {
    try {
      setLoading(true);
      setError("");

      const res = await axios.get(
        `http://127.0.0.1:8000/recommend/${movie}`
      );

      setResults(res.data);
    } catch (err) {
      setError("Unable to fetch recommendations");
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  const hybridRecommend = async () => {
    try {
      setLoading(true);
      setError("");

      const res = await axios.get(
        `http://127.0.0.1:8000/hybrid/${userId}/${movie}`
      );

      setResults(res.data);
    } catch (err) {
      setError("Unable to fetch recommendations");
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">

      <div className="hero">
        <h1>🎬 Smart Recommendation System</h1>

        <p className="subtitle">
          Discover movies you'll love using AI-powered recommendations
        </p>
      </div>

      <div className="search-box">

        <div className="input-group">
          <label>Movie Name</label>

          <input
            type="text"
            placeholder="Enter movie name"
            value={movie}
            onChange={(e) => setMovie(e.target.value)}
          />
        </div>

        <div className="input-group">
          <label>User ID</label>

          <input
            type="text"
            placeholder="Enter user id"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
          />
        </div>

        <div className="button-row">

          <button
            className="recommend-btn"
            onClick={recommend}
          >
            Recommend
          </button>

          <button
            className="hybrid-btn"
            onClick={hybridRecommend}
          >
            Hybrid Recommend
          </button>

        </div>

      </div>

      {loading && (
        <h2 className="loading">
          Loading Recommendations...
        </h2>
      )}

      {error && (
        <h2 className="error">
          {error}
        </h2>
      )}

      <h2 className="section-title">
        Top Recommendations
      </h2>

      <div className="cards">

        {results.map((item, index) => (

          <div
            key={index}
            className="card"
          >

            <img
              className="poster"
              src={
                item.poster ||
                "https://via.placeholder.com/300x450?text=No+Poster"
              }
              alt={item.title}
            />

            <h3>{item.title}</h3>

            {item.genres && (
              <p className="genres">
                {item.genres}
              </p>
            )}

            {item.score && (
              <p className="score">
                ⭐ {item.score}
              </p>
            )}

          </div>

        ))}

      </div>

    </div>
  );
}

export default App;