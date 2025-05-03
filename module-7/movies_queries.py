#Juedeja Richard - Module7.2 - 4/30/25
#keeping login information in env, reading that, connecting to movies database,
#creating queries and error exceptions

from tkinter.tix import Select
#tkinter is library

import mysql.connector # to connect
from mysql.connector import errorcode
from dotenv import dotenv_values

secrets = dotenv_values(".env")

""" database config object """
config = {
    "user": secrets["USER"],
    "password":secrets["PASSWORD"],
    "host":secrets["HOST"],
    "database": secrets["DATABASE"],
    "raise_on_warnings": True #not in .env file
}

try:
    """ try/catch block for handling potential MySQL database errors """

    db = mysql.connector.connect(**config)  # connect to the movies database

    # output the connection status
    print("\n  Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"],
                                                                                       config["database"]))

    input("\n\n  Press any key to continue...")

    # Script cursor object to search through tables
    cursor = db.cursor()

    # create string to represent 1st query we want to execute with studio table
    print("-- Displaying Studio Records --")
    cursor.execute("SELECT * FROM studio")
    studios = cursor.fetchall()
    for studio in studios:
        print(f"Studio_ID: {studio[0]}")
        print(f"Studio Name: {studio[1]}\n")

    # create string to represent 2nd query we want to execute with genre table
    print("-- Displaying Genre Records --")
    cursor.execute("SELECT genre_id, genre_name FROM genre")
    genres = cursor.fetchall()
    for genre in genres:
        print(f"Genre ID: {genre[0]}")
        print(f"Genre Name: {genre[1]}\n")

    # create string to represent 3rd query we want to execute with film table
    print("-- Displaying Short Film Records --")
    cursor.execute(f"SELECT film_name, film_runtime FROM film WHERE film_runtime < 120")
    films = cursor.fetchall()
    for film in films:
        print(f"Film Name:{film[0]}")
        print(f"Film Runtime:{film[1]}\n")

    # create string to represent 4th query we want to execute with film table
    # group by director
    print("-- Displaying Director Records in Order --")
    cursor.execute(f"SELECT film_name, film_director FROM film ORDER BY film_director")
    directors = cursor.fetchall()
    for director in directors:
        print(f"Film Name: {director[0]}")
        print(f"Director: {director[1]}\n")

except mysql.connector.Error as err:
    """ on error code """

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("  The supplied username or password are invalid")

    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("  The specified database does not exist")

    else:
        print(err)

finally:
    """ close the connection to MySQL """
    db.close()
#Place queries before closing connection to the database