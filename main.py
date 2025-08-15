

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """Tworzy połączenie z plikiem bazy danych SQLite"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Połączono z bazą:", db_file)
    except Error as e:
        print("Błąd połączenia:", e)
    return conn

def create_table(conn):
    """Tworzy tabelę contacts"""
    sql = """
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        email TEXT
    );
    """
    try:
        cur = conn.cursor()
        cur.execute(sql)
        print("Tabela utworzona lub już istnieje.")
    except Error as e:
        print("Błąd tworzenia tabeli:", e)


def add_contact(conn, contact):
    """Dodaje nowy kontakt"""
    sql = "INSERT INTO contacts(name, phone, email) VALUES(?,?,?)"
    cur = conn.cursor()
    cur.execute(sql, contact)
    conn.commit()
    return cur.lastrowid


def select_all(conn):
    """Pobiera i wyświetla wszystkie rekordy"""
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts")
    rows = cur.fetchall()
    for row in rows:
        print(row)


def select_where(conn, **kwargs):
    """Pobiera rekordy według warunków"""
    conditions = [f"{k}=?" for k in kwargs]
    sql = f"SELECT * FROM contacts WHERE {' AND '.join(conditions)}"
    values = tuple(kwargs.values())
    cur = conn.cursor()
    cur.execute(sql, values)
    rows = cur.fetchall()
    for row in rows:
        print(row)


def update(conn, id, **kwargs):
    """Aktualizuje rekord o podanym ID"""
    parameters = [f"{k} = ?" for k in kwargs]
    sql = f"UPDATE contacts SET {', '.join(parameters)} WHERE id = ?"
    values = tuple(kwargs.values()) + (id,)
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    print("Zaktualizowano rekord ID:", id)


def delete_where(conn, **kwargs):
    """Usuwa rekordy spełniające warunki"""
    conditions = [f"{k}=?" for k in kwargs]
    sql = f"DELETE FROM contacts WHERE {' AND '.join(conditions)}"
    values = tuple(kwargs.values())
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
    print("Usunięto rekordy spełniające warunki:", kwargs)


def delete_all(conn):
    """Usuwa wszystkie rekordy z tabeli"""
    sql = "DELETE FROM contacts"
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    print("Wyczyszczono tabelę contacts.")


if __name__ == "__main__":
    conn = create_connection("my_contacts.db")
    create_table(conn)

    
    add_contact(conn, ("Jan Kowalski", "123456789", "jan@example.com"))
    add_contact(conn, ("Anna Nowak", "987654321", "anna@example.com"))

    print("\nWszystkie kontakty:")
    select_all(conn)

    print("\nWyszukiwanie kontaktu o imieniu 'Anna Nowak':")
    select_where(conn, name="Anna Nowak")

    print("\nAktualizacja telefonu Jana Kowalskiego:")
    update(conn, 1, phone="111222333")

    print("\nWszystkie kontakty po aktualizacji:")
    select_all(conn)

    print("\nUsuwanie Anny Nowak:")
    delete_where(conn, name="Anna Nowak")
    select_all(conn)

    print("\nCzyszczenie tabeli:")
    delete_all(conn)
    select_all(conn)

    conn.close()
