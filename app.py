import streamlit as st
import requests
from model1 import recommend, movies_clean

import os
from dotenv import load_dotenv

load_dotenv()
OMDB_API_KEY = os.environ.get("OMDB_API_KEY", "")

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Movie Recommendation System")
st.write("Discover movies similar to your favourite movie.")

# Movie selection
movie_list = sorted(movies_clean["title"].dropna().unique())

selected_movie = st.selectbox(
    "Choose a movie",
    movie_list
)


@st.cache_data(ttl=3600)
def fetch_movie_details(movie_name):
    url = "https://www.omdbapi.com/"

    params = {
        "apikey": OMDB_API_KEY,
        "t": movie_name,
        "type": "movie"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("Response") == "True":
            return data

        return None

    except (requests.RequestException, ValueError):
        return None


if st.button("Recommend Movies", type="primary"):
    recommendations = recommend(selected_movie, top_n=5)

    if recommendations is None or recommendations.empty:
        st.warning("No recommendations found.")

    else:
        st.subheader(f"Movies similar to {selected_movie}")

        cols = st.columns(5)

        for idx, (_, row) in enumerate(recommendations.iterrows()):
            movie_name = row["title"]
            details = fetch_movie_details(movie_name)

            with cols[idx]:
                if details:
                    poster = details.get("Poster", "N/A")

                    if poster != "N/A":
                        st.image(poster, use_container_width=True)
                    else:
                        st.info("Poster unavailable")

                    st.markdown(f"### {details.get('Title', movie_name)}")
                    st.write(f"⭐ IMDb: {details.get('imdbRating', 'N/A')}")
                    st.write(f"📅 Year: {details.get('Year', 'N/A')}")
                    st.write(f"🎭 Genre: {details.get('Genre', 'N/A')}")
                    st.write(f"🎯 Similarity: {row['similarity_score']}")

                else:
                    st.markdown(f"### {movie_name}")
                    st.caption("OMDb details unavailable")

                st.divider()