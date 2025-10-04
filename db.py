from mysql.connector import (connection)


def create_connection():
    cnx = connection.MySQLConnection(user='root', password='',
                                     host='127.0.0.1',
                                     database='spesa')
    if not cnx.is_connected():
        print("Errore di connessione al database.")
        return None
    return cnx

def close_connection(cnx):
    if cnx and cnx.is_connected():
        cnx.close()

def lista (cursor, id):
    cursor.execute("SELECT oggetto,nome FROM spesa WHERE id_utente = %s", (id,))
    shop = cursor.fetchall()
    if not shop:
        return []
    return [item[0] for item in shop]

def add(cursor, id, product, nome):
    product = product.strip().lower()
    if not product:
        return "Input non valido."
    cursor.execute("SELECT oggetto FROM spesa WHERE id_utente = %s AND oggetto = %s", (id, product))
    exist = cursor.fetchone()
    if exist:
        return "Il prodotto è già presente nella lista."
    cursor.execute("INSERT INTO spesa (id_utente, oggetto,nome) VALUES (%s, %s,%s)", (id, product, nome))
    return f"{product} aggiunto alla lista della spesa."

def remove(cursor, id, product):
    product = product.strip().lower()
    if not product:
        return "Input non valido."
    cursor.execute("SELECT oggetto FROM spesa WHERE id_utente = %s AND oggetto = %s", (id, product))
    exist = cursor.fetchone()
    if not exist:
        return "Il prodotto non è presente nella lista."
    cursor.execute("DELETE FROM spesa WHERE id_utente = %s AND oggetto = %s", (id, product))
    return f"{product} rimosso dalla lista della spesa."

def remove_all(cursor, id):

    cursor.execute("DELETE FROM spesa WHERE id_utente = %s", (id,))
    return "Tutti i prodotti sono stati rimossi dalla lista della spesa."

