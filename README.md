# CineMatch AI

AI-Powered Movie Recommendation System built using Machine Learning, Scikit-Learn, Streamlit, and TMDB API.

CineMatch AI recommends similar movies based on content similarity by analyzing movie metadata such as genres, keywords, cast, and crew. The application provides an interactive user experience with real-time movie posters, ratings, release years, and detailed movie information.

---

## Live Demo

🔗 https://cinematch-ai-recommender.streamlit.app/

---

## Features

- Content-Based Movie Recommendation System
- Similar Movie Suggestions
- Real-Time Movie Data using TMDB API
- Movie Posters and Backdrops
- Ratings and Release Year Information
- Interactive Movie Search
- Modern Dark UI
- Responsive Streamlit Web Application
- Deployed on Streamlit Community Cloud

---

## Application Preview

### Home Page

<img src="assets/home-page.png" width="100%">

### Recommendations

<img src="assets/recommendations.png" width="100%">

---

## Tech Stack

### Programming Language

- Python

### Machine Learning

- Scikit-Learn
- Count Vectorizer
- Cosine Similarity

### Data Processing

- Pandas
- NumPy

### Frontend

- Streamlit

### API

- TMDB (The Movie Database)

### Deployment

- Streamlit Community Cloud

---

## How It Works

### 1. Data Preprocessing

Movie metadata including:

- Genres
- Keywords
- Cast
- Crew

is cleaned and combined into a single feature representation.

### 2. Feature Extraction

Count Vectorization converts textual movie information into numerical vectors.

### 3. Similarity Calculation

Cosine Similarity is used to calculate similarity scores between movies.

### 4. Recommendation Engine

When a user selects a movie:

- Similarity scores are retrieved
- Most similar movies are ranked
- Top recommendations are displayed

### 5. Real-Time Data Fetching

TMDB API is used to fetch:

- Posters
- Backdrops
- Ratings
- Release Dates
- Movie Overview

---

## Installation

Clone the repository:

```bash
git clone https://github.com/umairzahid-dev/CineMatch-AI.git
```

Navigate to the project directory:

```bash
cd CineMatch-AI
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
TMDB_API_KEY=YOUR_API_KEY
```

Run the application:

```bash
streamlit run app.py
```

---

## Machine Learning Concepts Used

- Content-Based Filtering
- Feature Engineering
- Natural Language Processing
- Vectorization
- Cosine Similarity
- Recommendation Systems

---

## Skills Demonstrated

- Python Development
- Machine Learning
- Recommendation Systems
- Data Preprocessing
- Feature Engineering
- API Integration
- Streamlit Development
- Model Deployment
- Git & GitHub

---

## Future Improvements

- Genre-Based Filtering
- Trending Movies Section
- Movie Trailer Integration
- Cast & Director Information
- Watchlist Functionality
- User Authentication
- Hybrid Recommendation System

---

## Author

### Umair Zahid

---

If you found this project useful, consider giving it a ⭐ on GitHub.
