import flask 
from flask import redirect, url_for, request, jsonify
import sqlite3
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/user/<int:user_id>/artwork', methods=['POST'])
def add_artwork(user_id):
    try:
        connect = sqlite3.connect('./database.db')
        f = request.files['picture']
c
        return {}
    except:
        raise ValueError('Probleme serveur')

    # sql = ''' ................ '''
    # cursor = connect.cursor()

    # body = request.get_json()
    # data = json.loads(json.dumps(body))

    # cursor.execute(sql, data)
    # connect.commit()

   


app.run()