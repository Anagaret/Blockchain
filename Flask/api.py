import flask
from flask import redirect, url_for, request, jsonify, flash, render_template, session
import sqlite3
import json
from werkzeug.utils import secure_filename
from classes.pictureblock import PictureBlock
import bcrypt
import os
import jwt
import re

cwd = os.getcwd()


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = 'your secret key'


@app.route("/user", methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        form = request.form
        if "email" not in form:
            flash("L'email utilisateur manquant.")
            return render_template('create_user.html')
        if "password" not in form:
            flash("Le mot de passe est manquant.")
            return render_template('create_user.html')
        if "tel" not in form:
            flash("Le telephone utilisateur est  manquant.")
            return render_template('create_user.html')
        if "nom" not in form:
            flash("Le nom est manquant.")
            return render_template('create_user.html')
        if "prenom" not in form:
            flash("Le prenom est manquant.")
            return render_template('create_user.html')
        if "paypal" not in form:
            flash("Le paypal est manquant.")
            return render_template('create_user.html')
        if "pseudo" not in form:
            flash("Le pseudo est manquant.")
            return render_template('create_user.html')
        if not re.search(r"\S+[@]\w+[.]+\w+",form['email']):
            flash("L'email n'est pas au bon format")
            return render_template('create_user.html')
        if not re.search(r"^[0][6-7]{1}[0-9]{8}$", form['tel']):
            flash("Le numéro n'est pas au bon format. Il doit etre un 06 ou 07.")
            return render_template('create_user.html')

        password = hash_password(form["password"])
    
        try:
            connect = sqlite3.connect('./database.db')
            sql_create_user = """INSERT INTO user(pseudo, email, tel, nom, prenom, paypal, password)
                    VALUES(:pseudo, :email, :tel, :nom, :prenom, :paypal, :password) """
            data = json.loads(
                json.dumps(
                    {
                        "pseudo": form['pseudo'],
                        "email": form['email'],
                        "tel": form['tel'],
                        "nom": form['nom'],
                        "prenom": form['prenom'],
                        "paypal": form['paypal'],
                        "password": password
                    }
                )
            )
            cursor = connect.cursor()
            cursor.execute(sql_create_user, data)
            connect.commit()
            id_user = cursor.lastrowid


            return index()

            connect.close()
        except sqlite3.Error as er:
            flash("Doublon d'information")
            return render_template('create_user.html')
    return render_template('create_user.html')


@app.route("/delete_user", methods=["GET"])
def delete_user():
    if not session.get('token'):
        return login()
    else:
        user_id = session.get('user')['id']
        try:
            connect = sqlite3.connect("./database.db")
            sql = """  UPDATE user SET disabled = ? WHERE id = ? """
            cursor = connect.cursor()
            cursor.execute(sql, [1,user_id])
            connect.commit()
            connect.close()
            return logout()
        except sqlite3.Error as er:
            print(er)
            flash("Probleme base de donne .")
            return user_profil()


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/')
def index():
    if not session.get('token'):
        return render_template('login.html')

    try:
        connect = sqlite3.connect("./database.db")
        connect.row_factory = dict_factory
        cursor = connect.cursor()
        artworks = cursor.execute(
            """ select * from artwork a INNER JOIN block b ON a.id = b.id_artwork 
         INNER JOIN user u ON b.id_user_creator = u.id 
         WHERE b.id_user_owner <> ? and a.available = 1""", [session.get('user')['id']]
        ).fetchall()
        if artworks:
            artworks={"first": artworks[0], 'rest': artworks[1:]}
        connect.close()
    except sqlite3.Error as er:
        flash("Probleme base de donne .")
        return index();
    return render_template('index.html', artworks=artworks)

@app.route("/artwork/new", methods=["GET","POST"])
def add_artwork():
    if request.method == "POST":
        if 'picture' not in request.files:
            flash("Aucun fichier")
            return redirect(request.url)
        f = request.files['picture']
        if f.filename == '':
            flash('Aucune fichier selectionné')
            return redirect(request.url)
        if "image" not in f.mimetype:
            flash("Le fichier transmit n'est pas une image .")
            return render_template('add_artwork.html')
        price = request.form.get("price", None)
        if price is None:
            flash("Le prix n'est pas present .")
            return render_template('add_artwork.html')
        try:
            price = float(price.replace(",", "."))
            f.save(cwd + "/static/pictures/" + secure_filename(f.filename))
            try:
                connect = sqlite3.connect("./database.db")
                user_id = session.get('user')['id']
                sql_create_artwork = """ INSERT INTO artwork(price, filename)
                                    VALUES (:price, :filename) """
                data = json.loads(json.dumps({"price": price, "filename": f.filename}))
                cursor = connect.cursor()
                cursor.execute(sql_create_artwork, data)
                id_artwork = cursor.lastrowid
                connect.commit()
                block = PictureBlock(f.filename)
                sql_create_block = """ INSERT INTO block("index", previous_hash, "timestamp", hash, nonce, id_artwork, id_user_creator, id_user_owner, data) 
                                    VALUES (:index, :previous_hash, :timestamp, :hash, :nonce, :id_artwork, :id_user_creator, :id_user_owner, :data) """

                data_block = {
                    "index": block.index,
                    "previous_hash": block.previous_hash,
                    "timestamp": block.timestamp,
                    "hash": block.hash,
                    "nonce": block.nonce,
                    "id_artwork": id_artwork,
                    "id_user_creator": user_id,
                    "id_user_owner": user_id,
                    "data": str(block.data),
                }
                json.loads(json.dumps(data_block))
                cursor.execute(sql_create_block, json.loads(json.dumps(data_block)))
                connect.commit()
                connect.close()
            except sqlite3.Error as er:
                flash("Probleme insertion artwork")
                return render_template('add_artwork.html')

        except sqlite3.Error as er:
            flash("Le prix n'est pas au bon format .")
            return render_template('add_artwork.html')
        return render_template('add_artwork.html', filename=f.filename)

    elif not session.get('token'):
        return render_template('login.html')
    else:
        return render_template('add_artwork.html')


@app.route("/artwork/<int:id_artwork>", methods=["GET"])
def get_artwork(id_artwork):
    try:
        connect = sqlite3.connect("./database.db")
        connect.row_factory = dict_factory
        cursor = connect.cursor()
        artwork = cursor.execute(
            """ select b.id_user_creator, b.id_artwork, b.id_user_owner, a.filename,
         a.price, a.available from artwork a INNER JOIN block b ON a.id = b.id_artwork WHERE b.id_artwork=?""",
            [id_artwork],
        ).fetchone()
        if not artwork:
            artwork = {}
        connect.close()
        return jsonify(artwork)
    except sqlite3.Error as er:
        return {"error": "Probleme base de donne ."}


@app.route("/artwork", methods=["GET"])
def get_all_artwork():
   
    try:
        connect = sqlite3.connect("./database.db")
        cursor = connect.cursor()
        connect.row_factory = dict_factory
        artworks = cursor.execute(
            """ select b.id_user_creator, b.id_artwork, b.id_user_owner, a.filename,
         a.price, a.available from artwork a INNER JOIN block b ON a.id = b.id_artwork """
        ).fetchall()
        connect.close()
        return jsonify(artworks)
    except sqlite3.Error as er:
        return {"error": "Probleme base de donne ."}


@app.route("/user/artwork/owner", methods=["GET"])
def get_all_artwork_by_owner():
    if not session.get('token'):
        return render_template('login.html')
    else:
        id_user_owner = session.get('user')['id']
        try:
            connect = sqlite3.connect("./database.db")
            connect.row_factory = dict_factory
            cursor = connect.cursor()
            artworks = cursor.execute(
                """ select * from artwork a INNER JOIN block b ON a.id = b.id_artwork 
                INNER JOIN user u ON u.id = b.id_user_creator
            WHERE b.id_user_owner = ? """,
                [id_user_owner],
            ).fetchall()
            connect.close()
            return render_template('user_artwork_owner.html', artworks=artworks)
        except sqlite3.Error as er:
            flash("Probleme base de donne .")
            return render_template('user_artwork_owner.html')


@app.route("/user/artwork/creator", methods=["GET"])
def get_all_artwork_by_creator():
    if not session.get('token'):
        return render_template('login.html')
    else:
        id_user_creator = session.get('user')['id']
        try:
            connect = sqlite3.connect("./database.db")
            connect.row_factory = dict_factory
            cursor = connect.cursor()
            artworks = cursor.execute(
                """ select * from artwork a INNER JOIN block b ON a.id = b.id_artwork 
                INNER JOIN user u ON u.id = b.id_user_owner
                WHERE b.id_user_creator = ? """,
                [id_user_creator],
            ).fetchall()
            connect.close()
            return render_template('user_artwork_creator.html', artworks=artworks)
        except sqlite3.Error as er:
            flash("Probleme base de donne .")
            return render_template('user_artwork_creator.html')

@app.route("/buy_artwork/<int:id_artwork>", methods=["GET"])
def buy_artwork(id_artwork):
    if not session.get('token'):
        return index()
    try:
        connect = sqlite3.connect("./database.db")
        connect.row_factory = dict_factory
        cursor = connect.cursor()
        cursor.execute(
            """ UPDATE artwork SET available = 0 WHERE id = ?""", [id_artwork]
        )
        connect.commit()
        cursor.execute(
            """ 
                UPDATE block SET id_user_owner = ? WHERE id_artwork = ?""",
            [session.get('user')['id'], id_artwork],
        )
        connect.commit()
        connect.close()
        return get_all_artwork_by_owner()
    except sqlite3.Error as er:
        flash("Probleme base de donne .")
        return index()

@app.route("/available_artwork/<int:id_artwork>/<int:available>", methods=["GET"])
def available_artwork(id_artwork,available):
    if available == 0:
        available = 1
    else:
        available = 0
    if not session.get('token'):
        return index()
   
    try:
        connect = sqlite3.connect("./database.db")
        connect.row_factory = dict_factory
        cursor = connect.cursor()
        cursor.execute(
            """ UPDATE artwork SET available = ? WHERE id = ?""", [available, id_artwork]
        )
        connect.commit()
        connect.close()
        return get_all_artwork_by_owner()
    except sqlite3.Error as er:
        flash("Probleme base de donne .")
        return index()



def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        
        form = request.form

        if "email" not in form:
            flash("L'email utilisateur manquant.")
            return index()

        if "password" not in form:
            flash("Le mot de passe est manquant.")
            return index()



        try:
            connect = sqlite3.connect("./database.db")
            connect.row_factory = dict_factory
            cursor = connect.cursor()
            user = cursor.execute(
                """ select * from user where email = ?  and disabled = 0""", [form["email"]]
            ).fetchone()
            if not user:
                flash("Utilisateur non trouvé")
                return index()
            if not bcrypt.checkpw(form['password'].encode("utf-8"), user["password"].encode("utf-8")):
                flash("Mot de passe incorrect")
                return index()


            token = jwt.encode({'id': user["id"]}, "123456789", algorithm="HS256")
            session['token'] = token
            session['user'] = user


        except sqlite3.Error as er:
            flash("Probleme base de donnée")
        connect.close()
        return index()
    return index()


@app.route("/user/<int:id_user_owner>/block", methods=["GET"])
def get_block_by_id_user_owner(id_user_owner):
    
    try:
        connect = sqlite3.connect("./database.db")
        connect.row_factory = dict_factory
        cursor = connect.cursor()
        blocks = cursor.execute(
            """ select "index", previous_hash, data, "timestamp", hash, nonce from block
            WHERE id_user_owner = ? """,
            [id_user_owner],
        ).fetchall()
        if not blocks:
            blocks = []
        connect.close()
        return jsonify(blocks)
    except sqlite3.Error as er:
        return {"error": "Probleme base de donne ."}


@app.route("/user/<int:id_user_owner>/block/<int:id_block>", methods=["GET"])
def get_block_by_id_user_owner_and_id_block(id_user_owner, id_block):
   
    try:
        connect = sqlite3.connect("./database.db")
        connect.row_factory = dict_factory
        cursor = connect.cursor()
        block = cursor.execute(
            """ select "index", previous_hash, data, "timestamp", hash, nonce from block
            WHERE id_user_owner = ? and id= ? """,
            [id_user_owner, id_block],
        ).fetchone()
        if not block:
            block = {}
        connect.close()
        return jsonify(block)
    except sqlite3.Error as er:
        return {"error": "Probleme base de donne ."}


@app.route("/creator", methods=["GET"])
def get_all_creator():
    try:
        connect = sqlite3.connect("./database.db")
        connect.row_factory = dict_factory
        cursor = connect.cursor()
        creators = cursor.execute(
            """ select DISTINCT (b.id_user_owner), pseudo from block b INNER JOIN user u  
            ON b.id_user_owner = u.id """,
        ).fetchall()
        if not creators:
            creators = []
        connect.close()
        return jsonify(creators)
    except sqlite3.Error as er:
        return {"error": "Probleme base de donne ."}

@app.route("/logout")
def logout():
    session['token'] = None
    session['user'] = None
    return index()


@app.route("/user_profil", methods=["GET"])
def user_profil():
    try:
        connect = sqlite3.connect("./database.db")
        connect.row_factory = dict_factory
        cursor = connect.cursor()
        data = cursor.execute(
            """ select (select count(DISTINCT(id))   from block WHERE id_user_owner = ?) as count_owner,
                 (select count(DISTINCT(id))   from block WHERE id_user_creator = ?) as count_creator""",
            [session.get('user')['id'], session.get('user')['id']]
        ).fetchone()
        connect.close()
        return render_template('user_profil.html', data={'user': session.get('user'),'count_owner':data['count_owner'], 'count_creator':data['count_creator'], })
    except sqlite3.Error as er:
        flash("Probleme base de donne .")
        return user_profil()


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>Erreur</h1><p>Page non trouvé !!!</p>", 404

app.run()
