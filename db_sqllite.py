import sqlite3
import os

def create_connection():
    try:   
        db_path = os.path.join(os.path.dirname(__file__), 'spesa.db')
        cnx = sqlite3.connect(db_path)
        cursor = cnx.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS spesa (
                id_utente INTEGER NOT NULL,
                oggetto TEXT NOT NULL,
                nome TEXT
            )
        ''')
        cnx.commit()

        return cnx
    except Exception as e:
        print(f"Errore di connessione al database: {e}")
        return None
    
def close_connection(cnx):
    if cnx:
        cnx.close()

def lista (cursor, id):
    cursor.execute("SELECT oggetto FROM spesa WHERE id_utente = ?", (id,))
    shop = cursor.fetchall()
    if not shop:
        return []
    return [item[0] for item in shop]

def add(cursor, id, product, nome):
    product = product.strip().lower()
    if not product:
        return "Input non valido."
    cursor.execute("SELECT oggetto FROM spesa WHERE id_utente = ? AND oggetto = ?", (id, product))
    exist = cursor.fetchone()
    if exist:
        return "Il prodotto è già presente nella lista."
    cursor.execute("INSERT INTO spesa (id_utente, oggetto, nome) VALUES (?, ?, ?)", (id, product, nome))
    return f"{product} aggiunto alla lista della spesa."

def remove(cursor, id, product):
    product = product.strip().lower()
    if not product:
        return "Input non valido."
    cursor.execute("SELECT oggetto FROM spesa WHERE id_utente = ? AND oggetto = ?", (id, product))
    exist = cursor.fetchone()
    if not exist:
        return "Il prodotto non è presente nella lista."
    cursor.execute("DELETE FROM spesa WHERE id_utente = ? AND oggetto = ?", (id, product))
    return f"{product} rimosso dalla lista della spesa."

def remove_all(cursor, id):
    cursor.execute("DELETE FROM spesa WHERE id_utente = ?", (id,))
    return "Tutti i prodotti sono stati rimossi dalla lista della spesa."