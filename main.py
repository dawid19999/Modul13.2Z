

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        print(f"Połączono z bazą danych: {db_file}")
        return conn
    except Error as e:
        print(f"Błąd połączenia: {e}")
        return None


def create_table(conn):
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
        conn.commit()
        cur.close()
        print("Tabela 'contacts' utworzona lub już istnieje.")
    except Error as e:
        print(f"Błąd tworzenia tabeli: {e}")


def add_contact(conn, contact):
    try:
        sql = "INSERT INTO contacts(name, phone, email) VALUES(?,?,?)"
        cur = conn.cursor()
        cur.execute(sql, contact)
        conn.commit()
        contact_id = cur.lastrowid
        cur.close()
        print(f"Dodano kontakt ID: {contact_id}")
        return contact_id
    except Error as e:
        print(f"Błąd dodawania kontaktu: {e}")


def select_all(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM contacts")
        rows = cur.fetchall()
        cur.close()
        if rows:
            for row in rows:
                print(row)
        else:
            print("Brak kontaktów w bazie.")
    except Error as e:
        print(f"Błąd odczytu: {e}")


def select_where(conn, **kwargs):
    try:
        conditions = [f"{k}=?" for k in kwargs]
        sql = f"SELECT * FROM contacts WHERE {' AND '.join(conditions)}"
        values = tuple(kwargs.values())
        cur = conn.cursor()
        cur.execute(sql, values)
        rows = cur.fetchall()
        cur.close()
        if rows:
            for row in rows:
                print(row)
        else:
            print("Nie znaleziono kontaktu spełniającego podane warunki.")
    except Error as e:
        print(f"Błąd wyszukiwania: {e}")


def update(conn, id, **kwargs):
    try:
        parameters = [f"{k} = ?" for k in kwargs]
        sql = f"UPDATE contacts SET {', '.join(parameters)} WHERE id = ?"
        values = tuple(kwargs.values()) + (id,)
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        cur.close()
        print(f"Zaktualizowano rekord ID: {id}")
    except Error as e:
        print(f"Błąd aktualizacji: {e}")


def delete_where(conn, **kwargs):
    try:
        conditions = [f"{k}=?" for k in kwargs]
        sql = f"DELETE FROM contacts WHERE {' AND '.join(conditions)}"
        values = tuple(kwargs.values())
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        cur.close()
        print(f"Usunięto kontakty spełniające warunki: {kwargs}")
    except Error as e:
        print(f"Błąd usuwania: {e}")


def delete_all(conn):
    try:
        sql = "DELETE FROM contacts"
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        print("Wyczyszczono tabelę 'contacts'.")
    except Error as e:
        print(f"Błąd czyszczenia tabeli: {e}")


if __name__ == "__main__":
    conn = create_connection("my_contacts.db")
    if conn:
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

    

