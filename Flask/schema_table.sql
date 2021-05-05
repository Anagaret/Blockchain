DROP TABLE IF EXISTS user;
CREATE TABLE IF NOT EXISTS "user"(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    pseudo TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    tel TEXT UNIQUE NOT NULL,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    paypal TEXT UNIQUE NOT NULL,
    "password" TEXT NOT NULL
);
DROP TABLE IF EXISTS artwork;
CREATE table IF NOT EXISTS "artwork"(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    filename TEXT NOT NULL,
    price NUMERIC NOT NULL,
    available INTEGER DEFAULT 1
);
DROP TABLE IF EXISTS block;
CREATE table IF NOT EXISTS "block"(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    "index" INTEGER NOT NULL,
    previous_hash TEXT,
   	data TEXT NOT NULL,
    "timestamp" NUMERIC NOT NULL,
    hash TEXT NOT NULL,
    nonce NUMERIC NOT NULL,
    id_artwork NUMERIC NOT NULL,
    id_user_creator NUMERIC NOT NULL,
    id_user_owner NUMERIC NOT NULL
    -- FOREIGN KEY (id_artwork) REFERENCES artwork(id),
    -- FOREIGN KEY (id_user_creator) REFERENCES user(id),
    -- FOREIGN KEY (id_user_owner) REFERENCES user(id)
);
