import sqlite3
connexion  = sqlite3.connect("./database.db")
curseur = connexion.cursor()


    
def create_table(): 
    try:
        with open('schema_table.sql', 'r') as sql_file:
            curseur.executescript(sql_file.read())
            connexion.commit()
    except:
        raise ValueError('Problem creating tables')
    

create_table()
