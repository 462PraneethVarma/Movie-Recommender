import streamlit as st
import pickle
import pandas as pd
import requests
from streamlit_option_menu import option_menu

with st.sidebar:
    selected = option_menu(
        menu_title = "User Menu",
        options = ["Home","Login","Recommendation","Feedback"],
        icons = ["house","book","film","envelope","x"],
        menu_icon = "cast",
        default_index = 0,
    )


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        #now we are going to add pictures
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

def LBP_recommend():
    st.title('Movie Recommendation')
    selected_movie_name = st.selectbox('Please Enter the MOVIE name', movies['title'].values)
    if st.button('Recommend'):
        names, posters = recommend(selected_movie_name)

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(names[0])
            st.image(posters[0])
        with col2:
            st.text(names[1])
            st.image(posters[1])
        with col3:
            st.text(names[2])
            st.image(posters[2])
        with col4:
            st.text(names[3])
            st.image(posters[3])
        with col5:
            st.text(names[4])
            st.image(posters[4])

def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


if selected == "Home":
    st.title("LBP Movie's")
    st.text("We have over 4500 movies and we recommend good movies based on your interest.")
    st.image("Movies.jpg")
    st.header("How To Use")
    st.text("Enter the Recommendation block inorder to get similar movies.")
    st.text("After entering into Recommendation block enter a movie name and get some good recommendations")
if selected == "Login":
    st.title("Login Application")
    st.text("Login if you are interested or else skip this block")
    contact_form = """<form action="https://formsubmit.co/praneethvarma551@gmail.com" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your Name" required>
     <input type="email" name="email" placeholder="EMAIL" required>
     <button type="submit">Send</button>
     </form>
     """
    st.markdown(contact_form,unsafe_allow_html=True)

    local_css("style.css")

if selected == "Recommendation":
    LBP_recommend()
if selected =="Feedback":
    st.header("Please enter your feedback")
    contact_form1 = """
    <textarea name="message" placeholder="Enter your Valuable Feedback"></textarea>
    <button type="submit">Send</button>
    """
    local_css("style.css")
    st.markdown(contact_form1,unsafe_allow_html=True)
