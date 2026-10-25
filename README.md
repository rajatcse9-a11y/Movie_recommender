# 🎬 Movie Recommendation System

A content-based movie recommender built with **TF-IDF** and **cosine similarity**. Pick a movie and the app returns the 5 most similar ones, along with posters, IMDb ratings, year and genre fetched live from the OMDb API.

🔗 **Live Demo: https://movie-recommender-k80e.onrender.com
📦 **GitHub Repo: https://github.com/rajatcse9-a11y/Movie_recommender.git

> The demo runs on Render's free tier, so the first load after a period of inactivity can take 30–60 seconds while the app wakes up.


## Features

- Search any movie from the TMDB 5000 dataset using a dropdown
- Top 5 similar movies with similarity scores
- Posters, IMDb rating, release year and genres via the OMDb API
- Cached API responses to keep the app fast and stay within rate limits
- Dockerfile included for containerized deployment

## How It Works

1. **Data:** TMDB 5000 Movies and Credits datasets are merged on movie id.
2. **Feature engineering:** For each movie, the overview, genres, keywords, top 3 cast members and the director are combined into a single `tags` text field.
3. **Vectorization:** `TfidfVectorizer` (5000 features, English stop words removed) converts the tags into numerical vectors.
4. **Similarity:** Cosine similarity between the selected movie and every other movie ranks the closest matches.
5. **UI:** Streamlit displays the results, and the OMDb API adds posters and ratings.

## Tech Stack

| Area | Tools |
|---|---|
| Language | Python |
| ML | scikit-learn (TF-IDF, cosine similarity), pandas |
| Web app | Streamlit |
| External API | OMDb API |
| Deployment | Render, Docker |

## Project Structure

```
├── app.py                  # Streamlit UI
├── model1.py               # Data processing + recommendation logic
├── model.ipynb             # Notebook with exploration and model building
├── tmdb_5000_movies.csv
├── tmdb_5000_credits.csv
├── requirements.txt
├── Dockerfile
└── .gitignore
```

## Run Locally

```bash
# 1. Clone the repo 
git clone https://github.com/rajatcse9-a11y/Movie_recommender.git
cd Movie_recommender

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your OMDb API key (free key: https://www.omdbapi.com/apikey.aspx)
echo OMDB_API_KEY=your_key_here > .env

# 4. Run the app
streamlit run app.py
```

## Run With Docker

```bash
docker build -t movie-recommender .
docker run --rm -p 8501:8501 --env-file .env movie-recommender
```

Then open http://localhost:8501.

## Future Improvements

- Add Hindi / Bollywood movies using the TMDB API
- Serve the model through a FastAPI backend
- Hybrid ranking that also considers ratings and popularity
- Explain *why* a movie was recommended

## Credits

- Dataset: [TMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) on Kaggle
- Posters and ratings: [OMDb API](https://www.omdbapi.com/)
- This product uses the TMDB data but is not endorsed or certified by TMDB.
