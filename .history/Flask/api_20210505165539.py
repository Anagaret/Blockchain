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
        return { 'error' : 'Le fichier transmit n\'est pas une image .'}
    price = request.form.get('price', None)
    if price is None:
        return { 'error' : 'Le prix n\'est pas present .'}
    try:
        price = float(price.replace(',','.'))
        f.save('./pictures/' + secure_filename(f.filename))
        try:
            sql_create_artwork = ''' INSERT INTO artwork VALUES(price, filename)
                                VALUES (?, ?) ''' 
            data = json.loads(json.dumps({'price': price, 'filename': f.filename}))

            cursor.execute(sql_create_artwork, data)
            connect.commit()
        except:
            return { 'error' :  'Probleme insertion artwork'}
    except:
        return { 'error' : 'Le prix n\'est pas au bon format .'}


   

    return {}

    # sql = ''' ................ '''
    # cursor = connect.cursor()


   


app.run()