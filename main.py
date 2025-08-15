
import sqlite3

def create_db():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_data():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    # Dodajemy przykładowe książki
    cursor.execute('DELETE FROM books')  # czyszczenie tabeli na start
    cursor.execute('''
        INSERT INTO books (title, author, year, description) VALUES
        ('Wiedźmin', 'Andrzej Sapkowski', 1993, 'Saga fantasy o wiedźminie Geralcie'),
        ('1984', 'George Orwell', 1949, 'Dystopijna wizja totalitarnego państwa'),
        ('Duma i uprzedzenie', 'Jane Austen', 1813, 'Klasyczna powieść obyczajowa')
    ''')

    conn.commit()
    conn.close()

def show_data():
    conn = sqlite3.connect('books.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM books')
    rows = cursor.fetchall()

    print("Zawartość bazy danych books.db:")
    for row in rows:
        print(f"ID: {row[0]}, Tytuł: {row[1]}, Autor: {row[2]}, Rok: {row[3]}, Opis: {row[4]}")

    conn.close()

if __name__ == "__main__":
    create_db()
    insert_data()
    show_data()
