import streamlit as st
import pickle
import requests
import os

from dotenv import load_dotenv

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="CineMatch AI",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

/* -----------------------------
   Background
------------------------------*/

.stApp{
    background:
    radial-gradient(
        circle at 20% 20%,
        rgba(99,102,241,.12),
        transparent 25%
    ),

    radial-gradient(
        circle at 80% 10%,
        rgba(168,85,247,.10),
        transparent 25%
    ),

    radial-gradient(
        circle at 80% 80%,
        rgba(59,130,246,.10),
        transparent 25%
    ),

    #020617;

    color:white;
}

/* -----------------------------
   Hero Section
------------------------------*/

.hero-container{
    background:rgba(255,255,255,0.04);
    backdrop-filter:blur(12px);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:24px;
    padding:60px;
    margin-bottom:40px;
}

.hero-title{
    font-size:64px;
    font-weight:900;
    text-align:center;
    letter-spacing:-2px;
    margin-bottom:6px;
    line-height:1;
}

.hero-subtitle{
    text-align:center;
    color:#9CA3AF;
    font-size:24px;
    font-weight:500;
}

/* -----------------------------
   Search Box
------------------------------*/

div[data-baseweb="select"] > div{
    min-height:72px;
    font-size:20px;
    font-weight:600;
    border-radius:18px;
    border:1px solid rgba(255,255,255,0.08);
    background:rgba(255,255,255,0.04);
    transition:all .3s ease;
}

div[data-baseweb="select"] > div:hover{
    border:1px solid rgba(96,165,250,.5);
    box-shadow:0 0 20px rgba(96,165,250,.15);
}

/* -----------------------------
   Movie Details
------------------------------*/

.movie-title{
    font-size:64px;
    font-weight:900;
    line-height:1.1;
}

.movie-meta{
    font-size:22px;
    font-weight:600;
    color:#D1D5DB;
    margin-top:12px;
    margin-bottom:18px;
}

.genre-badge{
    display:inline-block;
    background:#1F2937;
    padding:8px 16px;
    border-radius:25px;
    margin-right:10px;
    margin-top:10px;
    color:white;
    font-size:15px;
    font-weight:600;
    transition:all .3s ease;
}

.genre-badge:hover{
    transform:scale(1.08);
    background:#374151;
}

/* -----------------------------
   Selected Movie Poster
------------------------------*/

.selected-poster img{
    border-radius:20px;
    transition:all .5s ease;
}

.selected-poster img:hover{
    transform:scale(1.03);
}

/* -----------------------------
   Recommended Posters
------------------------------*/

[data-testid="stImage"] img{
    border-radius:16px;
    transition:all .35s ease;
}

[data-testid="stImage"] img:hover{

    transform:translateY(-5px) scale(1.03);

    box-shadow:
        0 0 20px rgba(59,130,246,.4),
        0 0 40px rgba(59,130,246,.25),
        0 20px 40px rgba(0,0,0,.6);

}

/* -----------------------------
   Recommendation Text
------------------------------*/

.rec-title{
    text-align:center;
    font-weight:700;
    font-size:18px;
    margin-top:12px;
    min-height:55px;
    transition:all .3s ease;
}

.rec-title:hover{
    color:#60A5FA;
}

.rec-meta{
    text-align:center;
    color:#9CA3AF;
    font-size:15px;
    font-weight:500;
}

/* -----------------------------
   Headings
------------------------------*/

h1{
    font-weight:900 !important;
}

h2{
    font-weight:800 !important;
}

h3{
    font-weight:700 !important;
}

/* -----------------------------
   Smooth Page Animations
------------------------------*/

*{
    transition:
    color .2s ease,
    background-color .2s ease,
    border-color .2s ease;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# ENV VARIABLES
# --------------------------------------------------

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

# --------------------------------------------------
# TMDB DETAILS
# --------------------------------------------------

@st.cache_data
def fetch_movie_details(movie_id):

    url = (
        f"https://api.themoviedb.org/3/movie/"
        f"{movie_id}?api_key={API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    poster_url = None
    backdrop_url = None

    if data.get("poster_path"):
        poster_url = (
            f"https://image.tmdb.org/t/p/w500"
            f"{data['poster_path']}"
        )

    if data.get("backdrop_path"):
        backdrop_url = (
            f"https://image.tmdb.org/t/p/original"
            f"{data['backdrop_path']}"
        )

    genres = [
        genre["name"]
        for genre in data.get("genres", [])
    ]

    return {
        "title": data.get("title"),
        "rating": data.get("vote_average"),
        "release_date": data.get("release_date"),
        "overview": data.get("overview"),
        "poster": poster_url,
        "backdrop": backdrop_url,
        "genres": genres
    }

# --------------------------------------------------
# RECOMMENDATION FUNCTION
# --------------------------------------------------

@st.cache_data
def recommend(movie):

    movie_index = movies[
        movies["title"] == movie
    ].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []
    recommended_ratings = []
    recommended_years = []

    for i in movies_list:

        movie_id = movies.iloc[i[0]].movie_id

        details = fetch_movie_details(movie_id)

        recommended_movies.append(
            movies.iloc[i[0]].title
        )

        recommended_posters.append(
            details["poster"]
        )

        recommended_ratings.append(
            details["rating"]
        )

        year = "N/A"

        if details["release_date"]:
            year = details["release_date"][:4]

        recommended_years.append(year)

    return (
        recommended_movies,
        recommended_posters,
        recommended_ratings,
        recommended_years
    )

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="hero-title">CineMatch AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">Discover Movies You Will Love</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# SEARCH
# --------------------------------------------------

st.markdown("""
<div style="
font-size:32px;
font-weight:900;
margin-bottom:15px;
margin-top:25px;
">
Find Your Next Movie
</div>
""", unsafe_allow_html=True)

selected_movie = st.selectbox(
    "",
    movies["title"].values
)

# --------------------------------------------------
# MOVIE DETAILS
# --------------------------------------------------

selected_movie_id = movies[
    movies["title"] == selected_movie
].iloc[0].movie_id

movie_details = fetch_movie_details(
    selected_movie_id
)

rating = movie_details["rating"]

if rating is not None:
    rating = round(rating, 1)
else:
    rating = "N/A"

release_year = "N/A"

if movie_details["release_date"]:
    release_year = movie_details["release_date"][:4]

st.markdown("<div style='margin-top:25px'></div>", unsafe_allow_html=True)

# Backdrop Image

if movie_details["backdrop"]:

    col1, col2, col3 = st.columns([0.7, 8.7, 0.7])

    with col2:

        st.image(
            movie_details["backdrop"],
            use_container_width=True
        )

# Movie Title

st.markdown(
    f"""
    <div class="movie-title" 
        style="text-align:center;
        margin-top:8px;
        ">
        {movie_details['title']}
    </div>
    """,
    unsafe_allow_html=True
)

# Rating + Year

st.markdown(
    f"""
    <div style="
        text-align:center;
        color:#9CA3AF;
        font-size:18px;
        font-weight:600;
        margin-top:8px;
        margin-bottom:15px;
    ">
        ⭐ {rating} | {release_year}
    </div>
    """,
    unsafe_allow_html=True
)

# Genres

genre_html = ""

for genre in movie_details["genres"]:

    genre_html += (
        f'<span class="genre-badge">{genre}</span>'
    )

st.markdown(
    f"""
    <div style="text-align:center;">
        {genre_html}
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")

# Overview

overview = movie_details["overview"]

if overview:

    st.markdown(
        f"""
        <div style="
            font-size:18px;
            line-height:1.8;
            color:#E5E7EB;
            margin-top:20px;
            text-align:center;
            max-width:1000px;
            margin-left:auto;
            margin-right:auto;
        ">
            {overview}
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# --------------------------------------------------
# RECOMMENDATIONS
# --------------------------------------------------

with st.spinner("Generating recommendations..."):

    (
        recommended_movies,
        recommended_posters,
        recommended_ratings,
        recommended_years
    ) = recommend(selected_movie)

st.markdown("""
<h2 style="
font-size:34px;
font-weight:800;
margin-top:20px;
margin-bottom:20px;
">
Recommended Movies
</h2>
""",
unsafe_allow_html=True)

cols = st.columns(5)

for i in range(5):

    with cols[i]:

        if recommended_posters[i]:

            st.image(
                recommended_posters[i],
                use_container_width=True
            )

        rating = recommended_ratings[i]

        if rating:
            rating = round(rating,1)
        else:
            rating = "N/A"

        st.markdown(
            f"""
            <div class="rec-title">
                {recommended_movies[i]}
            </div>

            <div class="rec-meta">
                ⭐ {rating} | {recommended_years[i]}
            </div>
            """,
            unsafe_allow_html=True
        )