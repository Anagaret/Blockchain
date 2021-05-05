import sqlite3
global connexion  
connexion  = sqlite3.connect("./database.db")
global curseur 
curseur = connexion.cursor()


    
def create_table(): 
    try:
        with open('schema_table.sql', 'r') as sql_file:
            print(sql_file.read())
            curseur.executescript(sql_file.read())
            connexion.commit()
            connexion.close()
    except:
        raise ValueError('Problem creating tables')
    

create_table()

