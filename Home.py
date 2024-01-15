"""
Author: Jared Park
Description: this is the main streamlit app. this will bring up a form that a user can fill out about their favourite movie
"""

# import the streamlit library
import streamlit as st

# import the functions to connect to the db and insert data into the db
from connectDB import connectDB, insertIntoDB


def setToNone(inputDict: dict) -> dict:
    """
    This function will set all emptry strings inputed by the user to None
    """
    for key in inputDict.keys():
        if (inputDict[key] == ''):
            return None
    return inputDict


def main() -> None:
    """
    This function will load the streamlit form which will allow users to input data into a form
    """
    try:
        # gets the connection and the cursor to db
        conn, c = connectDB(
            st.secrets["DRIVER_NAME"], st.secrets["SERVER_NAME"], st.secrets["DATABASE"])
        print("Connected to database")
    except:
        # raise an error
        raise Exception("Couldn't connect to database")

    st.set_page_config(
        page_title="Favourite Movie Form",
    )

    # title of the form
    st.title("Favourite Movie Form")
    st.subheader("By: Jared, Dexter, and Chenyoung")

    # form formatting
    with st.form(key="myForm"):
        st.subheader("About You")
        colf, coll = st.columns(2)
        with colf:
            # first name variable
            user_fname = st.text_input(
                label="Your First Name:"
            )
        with coll:
            # last name variable
            user_lname = st.text_input(
                label="Your Last Name:"
            )
        # age variable
        user_age = st.number_input(
            label="Your Age:",
            step=1
        )
        # gender variable
        user_gender = st.selectbox(
            label="Your gender:",
            options=("Male", "Female", "Other")
        )
        # region variable
        user_region = st.selectbox(
            label="Your Nationality:",
            options=(
                'north america',
                'south america',
                'europe',
                'asia',
                'africa',
                'austraila',
                'antarctica'
            )
        )
        st.subheader("About Your Favourite Movie")
        # movie variable
        movie_title = st.text_input(
            label="Movie Title"
        )

        # genre variable
        movie_genre = st.text_input(
            label="Movie Genre"
        )

        # movie year variable
        movie_year = st.number_input(
            label="Movie Release Year",
            step=1
        )

        # movie studio variable
        movie_studio = st.text_input(
            label="Who Produced The Movie"
        )

        # movie region variable
        movie_location = st.selectbox(
            label="Where was the movie produced:",
            options=(
                'north america',
                'south america',
                'europe',
                'asia',
                'africa',
                'australia',
                'antarctica'
            )
        )
        col_leadf, col_leadL = st.columns(2)

        with col_leadf:

            # director first name variable
            movie_leadf = st.text_input(
                label="Lead Actors First Name"
            )

            # director last name variable
            movie_directf = st.text_input(
                label="Directors First Name"
            )

        with col_leadL:

            # lead acter first name variable
            movie_leadL = st.text_input(
                label="Lead Actors Last Name"
            )

            # lead acter last name variable
            movie_directl = st.text_input(
                label="Directors Last Name"
            )

        # create submit button
        submit_button = st.form_submit_button(label="Submit")

        # run when the submit button is clicked
        if submit_button:

            # create movie dictionary
            movie = {
                "title": movie_title.lower(),
                "genre": movie_genre.lower(),
                "year": movie_year,
                "studio": movie_studio.lower(),
                "location": movie_location.lower(),
                "directorF": movie_directf.lower(),
                "directorL": movie_directl.lower(),
                "leadF": movie_leadf.lower(),
                "leadL": movie_leadL.lower()
            }

            # create user dictionary
            user = {
                "fname": user_fname,
                "lname": user_lname,
                "age": user_age,
                "gender": user_gender,
                "location": user_region.lower()
            }

            # turn all the empty strings in the dictionary to None
            movie = setToNone(movie)
            user = setToNone(user)

            if (movie != None and user != None):
                # insert the form into the database
                insertIntoDB(conn, c, movie, user)
                st.success("Form has been submitted")
            else:
                # throw an error
                st.error("The form was not filled out completly")


if __name__ == "__main__":
    main()
