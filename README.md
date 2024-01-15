# Favourite Movie Form

This form was built using a the [streamlit]{https://streamlit.io/} python framework to create a web application that allows users to fill out what their favourite movie is and store it in a MS SQL Server database. 

## This does require a MS SQL Server database to work

1. download MS SQL Server along SSMS from microsoft to set up a sql server. then run the finalProjectQuery.sql file using SSMS  to create the database.
2. if not installed download the python interpreter from [python official]{https://www.python.org/}. I've used version 3.10.6
3. create a virtual enviroment using `python -m venv venv` on windows or `python3 -m venv venv` on linux in the directory you want to use these files in any terminal
4. activate the virtual enviroment by `.\venv\Scripts\activate` on windows or `source venv/bin/activate` on linux
5. run `pip install -r ./requirements.txt` to downlaod all the packages to the virtual enviroment
6. create a .streamlit folder in the directory you are running the apps and make a secrets.toml file in the .streamlit folder. then type the driver name, server name, and database name into the file with this format
   `DRIVER_NAME = 'ODBC Driver 17 for SQL Server'
    SERVER_NAME = 'Your Server'
    DATABASE = 'FavMovie'`

7. the run `streamlit run Home.py` and it should work


