# this is the edit page of the streamlit app

# import packages
import streamlit as st
import pandas as pd
from connectDB import connectDB


def main() -> None:
    """
    This function will load the edit form to edit info in the database
    """

    # get the connect and cursor for the variable
    conn, c = connectDB(
        st.secrets["DRIVER_NAME"], st.secrets["SERVER_NAME"], st.secrets["DATABASE"])

    st.set_page_config(
        page_title="Favourite Movie Form (Edit)",
    )

    st.header("Edit Info In The Database")

    # store the table to be edited
    table_select = st.selectbox(
        label="Which table do you want to edit:",
        options=(
            'viewer',
            'movie',
            'lead_actor',
            'genre',
            'director',
            'region',
            'production'
        )
    )

    # get the headers of the table
    headers = c.execute(
        f"SELECT name FROM sys.columns WHERE object_id = OBJECT_ID('{table_select}')").fetchall()
    header_list = []
    for header in headers:
        header_list.append(header[0])

    # get all the data from the selected table
    data = c.execute(f"SELECT * FROM {table_select}").fetchall()
    dataPoints = []
    for i in range(len(data)):

        # init an enmpty dictionary
        dataObject = {}
        for j in range(len(header_list)):
            # fill the dictionary with data from the a row in the table
            dataObject[header_list[j]] = data[i][j]
        # a the row to a list
        dataPoints.append(dataObject)

    # convert the data into a dataframe
    df = pd.DataFrame.from_records(dataPoints)
    st.dataframe(df)

    # get the row number
    index = st.number_input(
        label="Which row would you like to edit",
        min_value=0,
        max_value=len(df) - 1,
        step=1
    )

    # get the selected row you want to edit
    selectedDict = dataPoints[index]

    with st.form(key='editForm'):
        # adds a input field for each value that could be edited
        for header, value in selectedDict.items():
            selectedDict[header] = st.text_input(label=header, value=value)
        submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        try:
            for header, value in selectedDict.items():
                # checks to see if header is not a primary key
                if 'pk_' not in header:
                    if (selectedDict[header].isnumeric() == True):

                        # update data in the database
                        c.execute(
                            f"""
                                UPDATE {table_select}
                                SET {header} = {int(selectedDict[header])}
                                WHERE pk_{table_select}_Id = {selectedDict[f"pk_{table_select}_Id"]}
                            """
                        )
                        conn.commit()
                    else:

                        # update data in the database
                        c.execute(
                            f"""
                                UPDATE {table_select}
                                SET {header} = '{selectedDict[header]}'
                                WHERE pk_{table_select}_Id = {selectedDict[f"pk_{table_select}_Id"]}
                            """
                        )
                        conn.commit()
            st.success("Row Has Benn Updated")
        except:
            st.error(
                "Somthing went wrong. check to see if the the foreign key exists for the table that you want to connect")


if __name__ == '__main__':
    main()
