import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Function to fetch movie details from TMDb
def fetch_movie_details_tmdb(title):
    api_key = "0a7a42d3e393653ba495817fab7e4201"  # Replace with your TMDb API key
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}"

    try:
        response = requests.get(search_url)
        response.raise_for_status()
        data = response.json()
        if data["results"]:
            movie = data["results"][0]
            movie_id = movie["id"]
            poster_path = movie.get("poster_path", None)
            details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&append_to_response=credits"
            details_response = requests.get(details_url)
            details_response.raise_for_status()
            details_data = details_response.json()

            movie_details = {
                "title": details_data.get("title", "N/A"),
                "imdb_rating": details_data.get("vote_average", "N/A"),
                "storyline": details_data.get("overview", "N/A"),
                "cast": ", ".join([cast["name"] for cast in details_data.get("credits", {}).get("cast", [])[:5]]),
                "poster_url": f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
            }
            return movie_details
        else:
            return {"error": "Movie not found."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {e}"}

# Streamlit UI
st.set_page_config(page_title="Movie Database Management System", layout="centered")
st.title("🎬 Movie Database Management System")

# Input for movie title
movie_title = st.text_input("Enter Movie Title:")

if st.button("Search"):
    if not movie_title.strip():
        st.warning("Please enter a movie title.")
    else:
        movie_details = fetch_movie_details_tmdb(movie_title)

        if "error" in movie_details:
            st.error(movie_details["error"])
        else:
            col1, col2 = st.columns([1, 2])

            if movie_details["poster_url"]:
                response = requests.get(movie_details["poster_url"])
                poster_image = Image.open(BytesIO(response.content))
                col1.image(poster_image, use_column_width=True)

            with col2:
                st.subheader(movie_details["title"])
                st.markdown(f"**IMDb Rating:** {movie_details['imdb_rating']}")
                st.markdown(f"**Storyline:** {movie_details['storyline']}")
                st.markdown(f"**Top Cast:** {movie_details['cast']}")
