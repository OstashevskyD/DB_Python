import psycopg2


# Функция создания таблицы
def create_db(conn):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(40) NOT NULL,
        last_name VARCHAR(40) NOT NULL,
        email VARCHAR(80) UNIQUE
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS  data_clients(
        id SERIAL PRIMARY KEY,
        phone VARCHAR(40),
        clients_id INTEGER REFERENCES clients(id)
    );
    """)
    conn.commit()


# Функция добавления клиента
def add_client(conn, first_name, last_name, email, phones=None):
    cur.execute("""
    INSERT INTO clients(first_name, last_name, email) VALUES(%s, %s, %s);
    """, (first_name, last_name, email))
    conn.commit()
    print('Пользователь', f'{last_name}', 'добавлен в таблицу')


# Функция добавления телефона
def add_phone(conn, clients_id, phone):
    cur.execute("""
    INSERT INTO data_clients(clients_id, phone) VALUES(%s, %s);
    """, (clients_id, phone))
    conn.commit()
    print('Номер телефона добавлен')


# Функция изменения данных о клиенте
def change_client(conn, id, first_name=None, last_name=None, email=None, phones=None):
    cur.execute("""
    UPDATE clients SET first_name=%s, last_name=%s, email=%s WHERE id=%s;
    """, (first_name, last_name, email, id))
    cur.execute("""
            SELECT * FROM clients;
            """)
    print('Изменения сохранены:', cur.fetchall())


# Функция удаления телефона
def delete_phone(conn, clients_id, phone):
    cur.execute("""
    DELETE FROM data_clients WHERE clients_id=%s;
    """, (clients_id,))
    conn.commit()
    print('Номер телефона удален')


# Функция удаления клиента
def delete_client(conn, id):
    cur.execute("""
    DELETE FROM clients WHERE id=%s;
    """, (id,))
    conn.commit()
    print('Данные клиента удалены')


# Функции поиска клиента
def find_client_with_name(conn, first_name):
    cur.execute("""
    SELECT * FROM clients WHERE first_name=%s;
    """, (first_name,))
    print('Клиент найден:', cur.fetchall())


def find_client_with_last_name(conn, last_name):
    cur.execute("""
    SELECT * FROM clients WHERE last_name=%s;
    """, (last_name,))
    print('Клиент найден:', cur.fetchall())


def find_client_with_email(conn, email):
    cur.execute("""
    SELECT * FROM clients WHERE email=%s;
    """, (email,))
    print('Клиент найден:', cur.fetchall())


def find_client_with_phone(conn, phone):
    cur.execute("""
    SELECT * FROM data_clients WHERE phone=%s;
    """, (phone,))
    print('Клиент найден:', cur.fetchall())


# Вспомогательная функция извлечения данных
def get_all_info(conn):
    cur.execute("""
    SELECT * FROM clients;
    """)
    print('fetchall', cur.fetchall())


#Проверка работы кода
with psycopg2.connect(database='clients_db2', user='postgres', password='so4jcnAgH') as conn:
    with conn.cursor() as cur:
        cur.execute("""
                DROP TABLE data_clients;
                DROP TABLE clients
                CASCADE;
                """)
        conn.commit()

        create_db(conn)
        add_client(conn, 'Andrew', 'Popov', 'popov@mail.com')
        get_all_info(conn)
        add_phone(conn, 1, '89998887766')
        change_client(conn, 1, 'Andrey', 'Pupkin', 'pupkin@mail.com')
        find_client_with_name(conn, 'Andrey')
        find_client_with_last_name(conn, 'Pupkin')
        find_client_with_email(conn, 'pupkin@mail.com')
        find_client_with_phone(conn, '89998887766')
        delete_phone(conn, 1, '89998887766')
        delete_client(conn, 1)
