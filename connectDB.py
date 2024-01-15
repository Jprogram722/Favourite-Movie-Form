"""
Author: Jared Park
Description: This file would handle the connection to the favourite movie database and handle any data being inserted into the database
"""

# import pyodbc to connect to the MS SQL Server database
import pyodbc as odbc


def getID(cursor: odbc.Cursor, movies: dict, user: dict) -> dict:
    """
    This function will check and see if the movie info that is being submitted is already an entry
    the database by getting its id (primary key). if the data is not in the database then the id
    for the corresponding table will be null
    """

    # get the directors id
    director_id = cursor.execute(
        f"""
        SELECT pk_director_Id FROM director 
        WHERE director_firstname = '{movies["directorF"]}' 
        AND director_lastname = '{movies["directorL"]}'
    """).fetchone()

    # get the production studios id
    production_id = cursor.execute(
        f"""
        SELECT pk_production_Id FROM production 
        WHERE production_name = '{movies["studio"]}' 
    """).fetchone()

    # get the movie regions id
    movie_region_id = cursor.execute(
        f"""
        SELECT pk_region_Id FROM region 
        WHERE region_name = '{movies["location"]}' 
    """).fetchone()

    # get the movie genre id
    genre_id = cursor.execute(
        f"""
        SELECT pk_genre_Id FROM genre
        WHERE genre_name = '{movies["genre"]}' 
    """).fetchone()

    # get the lead actor id
    lead_actor_id = cursor.execute(
        f"""
        SELECT pk_lead_actor_Id FROM lead_actor
        WHERE lead_actor_firstname = '{movies["leadF"]}' 
        AND lead_actor_lastname = '{movies["leadL"]}'
    """).fetchone()

    # get the movies id
    movie_id = cursor.execute(
        f"""
        SELECT pk_movie_Id FROM movie
        WHERE movie_title = '{movies["title"]}' 
        AND movie_release_year = {int(movies["year"])}
    """).fetchone()

    # get the users region id
    user_region_id = cursor.execute(
        f"""
        SELECT pk_region_Id FROM region
        WHERE region_name = '{user["location"]}' 
    """).fetchone()

    # combine all the ids into a dictionary
    idDictionary = {
        "director_id": director_id,
        "movie_contenint":  movie_region_id,
        "user_continent": user_region_id,
        "production_id": production_id,
        "genre_id": genre_id,
        "lead_actor_id": lead_actor_id,
        "movie_id": movie_id
    }

    return idDictionary


def connectDB(driver: str, server: str, database: str):
    """
    This function will allow users to connect to the MS SQL server database.
    The driver, server, and database name will be store in a .streamlit folder
    with secrets.toml file containing the infor
    """

    # this is a connection string
    conn_string = f"""
        Driver={{{driver}}};
        SERVER={{{server}}};
        DATABASE={{{database}}};
        Trusted_Connection=yes;
    """

    # create a connection
    conn = odbc.connect(conn_string)

    # create a cursor for the connection
    c = conn.cursor()

    return conn, c


def insertIntoDB(conn: odbc.Connection, cursor: odbc.Cursor, movies: dict, user: dict):
    """
    This function will evalute the info submitted by the user to see how much of the data is already in the database.
    Whatever is not in the database will be inserted into the database
    """

    # get the dictionary of ids
    ids = getID(cursor, movies, user)

    # see if the region has already been enter
    if (ids["movie_contenint"] == None):
        cursor.execute(
            """
            INSERT INTO continent
            VALUES (?)
            """, (movies["location"])
        )

        # commit the inserted data to the database
        conn.commit()

        # update the ids
        ids = getID(cursor, movies, user)

    if (ids["user_continent"] == None):
        cursor.execute(
            """
            INSERT INTO continent
            VALUES (?)
            """, (user["location"])
        )

        # commit the inserted data to the database
        conn.commit()

        # update the ids
        ids = getID(cursor, movies, user)

    if (ids["genre_id"] == None):
        cursor.execute(
            """
            INSERT INTO genre
            VALUES (?)
            """, (movies["genre"])
        )

        # commit the inserted data to the database
        conn.commit()

        # update the ids
        ids = getID(cursor, movies, user)

    if (ids["production_id"] == None):
        cursor.execute(
            """
            INSERT INTO production
            VALUES (?, ?)
            """, (movies["studio"], ids["movie_contenint"][0])
        )

        # commit the inserted data to the database
        conn.commit()

        # update the ids
        ids = getID(cursor, movies, user)

    if (ids["director_id"] == None):
        cursor.execute(
            """
            INSERT INTO director
            VALUES (?, ?)
            """, (movies["directorF"], movies["directorL"])
        )

        # commit the inserted data to the database
        conn.commit()

        # update the ids
        ids = getID(cursor, movies, user)

    if (ids["lead_actor_id"] == None):
        cursor.execute(
            """
            INSERT INTO lead_actor
            VALUES (?, ?)
            """, (movies["leadF"], movies["leadL"])
        )

        # commit the inserted data to the database
        conn.commit()

        # update the ids
        ids = getID(cursor, movies, user)

    if (ids["movie_id"] == None):
        cursor.execute(
            """
            INSERT INTO movie
            VALUES (?, ?, ?, ?, ?, ?)
            """, (movies["title"], movies["year"], ids["genre_id"][0], ids["director_id"][0], ids["production_id"][0], ids["lead_actor_id"][0])
        )

        # commit the inserted data to the database
        conn.commit()

        # update the ids
        ids = getID(cursor, movies, user)

    cursor.execute(
        """
            INSERT INTO viewer
            VALUES (?, ?, ?, ?, ?, ?)
            """, (user["fname"], user["lname"], user["age"], user["gender"], ids["user_continent"][0], ids["movie_id"][0])
    )

    # commit the inserted data to the database
    conn.commit()
    conn.close()
