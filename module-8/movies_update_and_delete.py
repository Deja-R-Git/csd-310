#Juedeja Richard - Module8.2 - 5/3/25
#keeping login information in env, reading that, connecting to movies database,
#creating queries and error exceptions, make show_films function to display results

#tkinter is library

import mysql.connector
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

def show_films(cursor, title):
    # Script cursor object to search through tables
    print("\n--{}--".format(title))
    cursor.execute("SELECT film_name as Name, film_director as Director, "
                   "genre_name as Genre, studio_name as 'Studio Name' "
                   "FROM film INNER JOIN genre On film.genre_id=genre.genre_id "
                   "INNER JOIN studio ON film.studio_id=studio.studio_id")
    films = cursor.fetchall()
    for film in films:
        print("Film Name: {}\nDirector: {}\nGenre Name ID: {}\nStudio Name: {}\n".format(film[0], film[1], film[2], film[3]))

try:
    """ try/catch block for handling potential MySQL database errors """

    db = mysql.connector.connect(**config)  # connect to the movies database
    cursor = db.cursor()

    # output connection status
    print("\n  Database user {} connected to MySQL on host {} with database {}".format(config["user"], config["host"],
                                                                                       config["database"]))
    # display original query results with film table and inner joins
    show_films(cursor,"DISPLAYING FILMS")

    #Insert new data row into films table
    cursor.execute("""
            INSERT INTO film (film_name,film_releaseDate, film_runtime,film_director, studio_id,genre_id)
            VALUES('Logan', '2017', 96, 'James Mangold', 1, 3)
            """)
    #saves changes to the database
    #db.commit()

    #Display new query results after insert new data
    show_films(cursor,"DISPLAYING FILMS AFTER INSERT")

    # Update Alien genre from Scifi to Horror in film table
    cursor.execute("UPDATE film SET genre_id = 1 WHERE film_name ='Alien'")

    #saves changes to database again
    #db.commit()

    show_films(cursor,"DISPLAYING FILMS AFTER UPDATE - CHANGED ALIEN TO HORROR")

        #Delete Gladiator movie from film table
    cursor.execute("DELETE FROM film WHERE film_name = 'Gladiator'")

        #save delete change to the database
    #db.commit()

    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")
        # Display new query results in film table after Delete Gladiator Movie

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