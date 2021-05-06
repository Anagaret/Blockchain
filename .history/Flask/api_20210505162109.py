import flask 
from flask import redirect, url_for, request, jsonify
import sqlite3
import json
from werkzeug.utils import secure_filename

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/user/<int:user_id>/artwork', methods=['POST'])
def add_artwork(user_id):
    connect = sqlite3.connect('./database.db')
    f = request.files['picture']
    if "image" not in f.mimetype:
        return { 'error' : 'Le fichier transmit n`est pas une image .'}
    f.save('./pictures/' + secure_filename(f.filename))
    return {}

    # sql = ''' ................ '''
    # cursor = connect.cursor()

    # body = request.get_json()
    # data = json.loads(json.dumps(body))

    # cursor.execute(sql, data)
    # connect.commit()

   


app.run()