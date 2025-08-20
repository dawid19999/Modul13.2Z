


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


def create_tables(conn):
    sql_contacts = """
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        email TEXT
    );
    """
    sql_addresses = """
    CREATE TABLE IF NOT EXISTS addresses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contact_id INTEGER NOT NULL,
        city TEXT NOT NULL,
        street TEXT,
        FOREIGN KEY (contact_id) REFERENCES contacts (id)
    );
    """
    try:
        cur = conn.cursor()
        cur.execute(sql_contacts)
        cur.execute(sql_addresses)
        conn.commit()
        cur.close()
        print("Tabele 'contacts' i 'addresses' utworzone lub już istnieją.")
    except Error as e:
        print(f"Błąd tworzenia tabel: {e}")



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


def select_all_contacts(conn):
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


def update_contact(conn, contact_id, new_phone, new_email):
    try:
        sql = "UPDATE contacts SET phone=?, email=? WHERE id=?"
        cur = conn.cursor()
        cur.execute(sql, (new_phone, new_email, contact_id))
        conn.commit()
        cur.close()
        print(f"Zaktualizowano kontakt ID {contact_id}")
    except Error as e:
        print(f"Błąd aktualizacji kontaktu: {e}")


def delete_contact(conn, contact_id):
    try:
        sql = "DELETE FROM contacts WHERE id=?"
        cur = conn.cursor()
        cur.execute(sql, (contact_id,))
        conn.commit()
        cur.close()
        print(f"Usunięto kontakt ID {contact_id}")
    except Error as e:
        print(f"Błąd usuwania kontaktu: {e}")



def add_address(conn, address):
    try:
        sql = "INSERT INTO addresses(contact_id, city, street) VALUES(?,?,?)"
        cur = conn.cursor()
        cur.execute(sql, address)
        conn.commit()
        addr_id = cur.lastrowid
        cur.close()
        print(f"Dodano adres ID: {addr_id} dla kontaktu {address[0]}")
        return addr_id
    except Error as e:
        print(f"Błąd dodawania adresu: {e}")


def select_all_addresses(conn):
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT a.id, c.name, a.city, a.street
            FROM addresses a
            JOIN contacts c ON a.contact_id = c.id
        """)
        rows = cur.fetchall()
        cur.close()
        if rows:
            for row in rows:
                print(row)
        else:
            print("Brak adresów w bazie.")
    except Error as e:
        print(f"Błąd odczytu adresów: {e}")


def select_addresses_for_contact(conn, contact_id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM addresses WHERE contact_id=?", (contact_id,))
        rows = cur.fetchall()
        cur.close()
        if rows:
            for row in rows:
                print(row)
        else:
            print(f"Brak adresów dla kontaktu ID {contact_id}.")
    except Error as e:
        print(f"Błąd odczytu adresów: {e}")


def update_address(conn, addr_id, new_city, new_street):
    try:
        sql = "UPDATE addresses SET city=?, street=? WHERE id=?"
        cur = conn.cursor()
        cur.execute(sql, (new_city, new_street, addr_id))
        conn.commit()
        cur.close()
        print(f"Zaktualizowano adres ID {addr_id}")
    except Error as e:
        print(f"Błąd aktualizacji adresu: {e}")


def delete_address(conn, addr_id):
    try:
        sql = "DELETE FROM addresses WHERE id=?"
        cur = conn.cursor()
        cur.execute(sql, (addr_id,))
        conn.commit()
        cur.close()
        print(f"Usunięto adres ID {addr_id}")
    except Error as e:
        print(f"Błąd usuwania adresu: {e}")


def select_addresses_in_city(conn, city_name):
    """SELECT z WHERE (np. wszystkie adresy w Warszawie)"""
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT a.id, c.name, a.city, a.street
            FROM addresses a
            JOIN contacts c ON a.contact_id = c.id
            WHERE a.city=?
        """, (city_name,))
        rows = cur.fetchall()
        cur.close()
        if rows:
            print(f"Adresy w {city_name}:")
            for row in rows:
                print(row)
        else:
            print(f"Brak adresów w mieście {city_name}.")
    except Error as e:
        print(f"Błąd SELECT WHERE: {e}")


if __name__ == "__main__":
    conn = create_connection("my_contacts.db")
    if conn:
        create_tables(conn)

        
        jan_id = add_contact(conn, ("Jan Kowalski", "123456789", "jan@example.com"))
        anna_id = add_contact(conn, ("Anna Nowak", "987654321", "anna@example.com"))

        print("\nWszyscy kontakty:")
        select_all_contacts(conn)

        
        add_address(conn, (jan_id, "Warszawa", "ul. Mickiewicza 10"))
        add_address(conn, (jan_id, "Kraków", "ul. Długa 5"))
        add_address(conn, (anna_id, "Warszawa", "ul. Puławska 12"))
        add_address(conn, (anna_id, "Gdańsk", "ul. Grunwaldzka 20"))

        print("\nWszystkie adresy:")
        select_all_addresses(conn)

        print("\nAdresy Jana Kowalskiego:")
        select_addresses_for_contact(conn, jan_id)

        print("\nAdresy w Warszawie:")
        select_addresses_in_city(conn, "Warszawa")

        conn.close()

    



