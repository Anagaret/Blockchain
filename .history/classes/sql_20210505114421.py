import sqlite3
connexion  = sqlite3.connect("./sql.db")
curseur = connexion.cursor()



def create_table(): 
    try:
        with open('schema_table.sql', 'r') as sql_file:
            cursor.executescript(sql_file.read())
            connexion.commit()
    except:
        raise ValueError('Problem creating tables')
    

create_table()

