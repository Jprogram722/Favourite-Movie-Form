"""
Author: Jared Park
Description: This file will load up a dashboard where you can see statitics about what kinds of movies people like
"""

# import packages
import streamlit as st
from connectDB import connectDB
import plotly.express as px
import pandas as pd


def main() -> None:

    # get the connection and the cursor for the database
    conn, c = connectDB(
        st.secrets["DRIVER_NAME"], st.secrets["SERVER_NAME"], st.secrets["DATABASE"])

    st.header("Favourite Movie Dashboard")
    st.markdown("This project we collected data from various users to see what kinds of movies would be popular amoung certain groups of people.")

    # store which variable the user would like use in the analysis
    analysis_variable = st.selectbox(
        label="Which variable would you like to analyze:",
        options=(
            'age',
            'gender',
            'region'
        )
    )

    if (analysis_variable == "region"):
        st.subheader(f"Analyzing Data By region")
        st.markdown("First we have to pull the data from the SQL database")
        data = c.execute(
            f"""
            SELECT vr.region_name, mg.genre_name, COUNT(*) FROM (
            SELECT v.pk_viewer_Id, r.region_name, v.movie_Id_fk FROM viewer v
            INNER JOIN region r ON v.region_Id_fk = r.pk_region_Id
            ) vr
            INNER JOIN (SELECT m.pk_movie_Id, m.movie_title, g.genre_name FROM movie m
            INNER JOIN genre g ON m.genre_Id_fk = g.pk_genre_Id) mg 
            ON vr.movie_Id_fk = mg.pk_movie_Id
            GROUP BY vr.region_name, mg.genre_name
            """).fetchall()
    else:
        st.subheader(f"Analyzing Data By {analysis_variable}")
        st.markdown("First we have to pull the data from the SQL database")
        data = c.execute(
            f"""
            SELECT v.viewer_{analysis_variable}, mg.genre_name, COUNT(*) FROM viewer v
            INNER JOIN (SELECT m.pk_movie_Id, m.movie_title, g.genre_name FROM movie m
            INNER JOIN genre g ON m.genre_Id_fk = g.pk_genre_Id) mg 
            ON v.movie_Id_fk = mg.pk_movie_Id
            GROUP BY v.viewer_{analysis_variable}, mg.genre_name
            """).fetchall()

    # convert the fetched data into a dataframe using list comprihension
    df = pd.DataFrame([[ij for ij in i] for i in data],
                      columns=[analysis_variable, "Genre", "Count"])

    # show the dataframe
    st.dataframe(df)

    st.markdown(
        "We can then visualize the data using a bar chart, showing the distribution of user choices")

    # generate a bar chart using plotly
    plt = px.bar(
        df,
        x='Genre',
        y='Count',
        color=analysis_variable,
        barmode='group'
    )

    # plot the graph in the streamlit app
    st.plotly_chart(plt)


if __name__ == '__main__':
    main()
