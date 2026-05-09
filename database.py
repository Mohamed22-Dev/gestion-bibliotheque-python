import sqlite3

DB_NAME = "bibliotheque.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS livres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titre TEXT NOT NULL,
        auteur TEXT NOT NULL,
        genre TEXT,
        annee INTEGER,
        quantite INTEGER DEFAULT 1
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS membres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        email TEXT,
        adhesion TEXT UNIQUE
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emprunts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        livre_id INTEGER,
        membre_id INTEGER,
        date_emprunt TEXT,
        date_retour_prevue TEXT,
        date_retour TEXT,
        FOREIGN KEY(livre_id) REFERENCES livres(id),
        FOREIGN KEY(membre_id) REFERENCES membres(id)
    )
    """)

    conn.commit()
    conn.close()