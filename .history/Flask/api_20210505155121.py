import flask 
from flask import redirect, url_for, request, jsonify
import sqlite3
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/artwork', methods['POST'])
def add_book():
    connect = sqlite3.connect('./database.db')
    print('run ici')

    # sql = ''' ................ '''
    # cursor = connect.cursor()

    # body = request.get_json()
    # data = json.loads(json.dumps(body))

    # cursor.execute(sql, data)
    # connect.commit()

    # return ......


app.run()