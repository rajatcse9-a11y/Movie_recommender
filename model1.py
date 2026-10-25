import ast
import os

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ---------- Helper functions ----------
def convert_to_list(text):
    try:
        data = ast.literal_eval(text)
        return [item["name"] for item in data if "name" in item]
    except (ValueError, SyntaxError, TypeError):
        return []


def get_director(text):
    try:
        data = ast.literal_eval(text)
        for person in data:
            if person.get("job") == "Director":
                return [person["name"]]
    except (ValueError, SyntaxError, TypeError):
        pass
    return []


def get_top_cast(text):
    return convert_to_list(text)[:3]


# ---------- Load & merge data ----------
movies = pd.read_csv(os.path.join(BASE_DIR, "tmdb_5000_movies.csv"))
credits = pd.read_csv(os.path.join(BASE_DIR, "tmdb_5000_credits.csv"))

movies = movies.merge(
    credits,
    left_on="id",
    right_on="movie_id",
    how="inner",
    suffixes=("", "_credits"),
)

movies = movies[
    ["id", "title", "overview", "genres", "keywords", "cast", "crew",
     "vote_average", "vote_count", "popularity"]
].copy()

# ---------- Missing values & duplicates ----------
movies["overview"] = movies["overview"].fillna("")
movies["genres"] = movies["genres"].fillna("[]")
movies["keywords"] = movies["keywords"].fillna("[]")
movies["cast"] = movies["cast"].fillna("[]")
movies["crew"] = movies["crew"].fillna("[]")

movies.drop_duplicates(subset="id", inplace=True)
movies.reset_index(drop=True, inplace=True)

# ---------- Convert JSON-like columns to lists ----------
movies["genres"] = movies["genres"].apply(convert_to_list)
movies["keywords"] = movies["keywords"].apply(convert_to_list)
movies["cast"] = movies["cast"].apply(get_top_cast)
movies["crew"] = movies["crew"].apply(get_director)
movies["overview"] = movies["overview"].apply(lambda x: str(x).lower().split())

# ---------- Create tags ----------
movies["tags"] = (
    movies["overview"]
    + movies["genres"]
    + movies["keywords"]
    + movies["cast"]
    + movies["crew"]
)
movies["tags"] = movies["tags"].apply(lambda words: " ".join(words).lower())

movies_clean = movies[
    ["id", "title", "tags", "vote_average", "vote_count", "popularity"]
].copy()

movies_clean.dropna(subset=["title"], inplace=True)
movies_clean.drop_duplicates(subset=["title"], inplace=True)
movies_clean.reset_index(drop=True, inplace=True)

# ---------- TF-IDF model ----------
tfidf = TfidfVectorizer(max_features=5000, stop_words="english")
tfidf_matrix = tfidf.fit_transform(movies_clean["tags"].fillna(""))

# Title -> row index (case-insensitive lookup)
_title_to_idx = {
    title.strip().lower(): idx for idx, title in movies_clean["title"].items()
}


# ---------- Recommend function ----------
def recommend(movie_name, top_n=5):
    """Selected movie jaisi top_n movies return karta hai (DataFrame).
    Movie na mile toh None return karta hai."""
    movie_idx = _title_to_idx.get(str(movie_name).strip().lower())
    if movie_idx is None:
        return None

    # Sirf selected movie ki similarity sabhi movies ke saath
    scores = cosine_similarity(tfidf_matrix[movie_idx], tfidf_matrix).flatten()

    similar_indices = [i for i in scores.argsort()[::-1] if i != movie_idx][:top_n]

    result = movies_clean.iloc[similar_indices][
        ["title", "vote_average", "popularity"]
    ].copy()
    result.insert(
        1,
        "similarity_score",
        [round(float(scores[i]), 3) for i in similar_indices],
    )
    return result.reset_index(drop=True)


if __name__ == "__main__":
    # Sirf tab chalega jab `python model1.py` direct run karo
    print(recommend("Avatar"))