import psycopg2

def create_db(conn, cur):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) ,
            last_name VARCHAR(50) ,
            email VARCHAR(60)         
        );
        """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phones(
            id SERIAL PRIMARY KEY,
            phone VARCHAR(60), 
            clients_id INTEGER NOT NULL REFERENCES clients(id)       
        );
        """)
    conn.commit()
def drop_table(cur):
    cur.execute("""
    DROP Table phones;
    DROP table clients
    """)


def get_phone(cur, client_id, phone):
    cur.execute("""
        SELECT phone FROM phones WHERE client_id=%s AND phone=%s;
        """, (client_id, phone))
    found_phone = cur.fetchall()
    return found_phone


def add_client(cur, first_name=None, last_name=None, email=None, phones=None):
    if first_name == None or last_name == None or email == None:
        print("Вы указали не все данные. Заполните все поля : name; surname; email")
        return
    cur.execute("""
        INSERT INTO clients(first_name, last_name, email) VALUES (%s, %s, %s) RETURNING id, first_name, last_name, email;
        """, (first_name, last_name, email))
    new_client = cur.fetchone()
    if phones != None:
        cur.execute("""
            INSERT INTO phones(clients_id, phone) VALUES(%s, %s);
             """, (new_client[0], phones))
    print(f'В базу добавлен новый клиент : {new_client}')


def add_phone(cur, clients_id, phone):
    cur.execute("""
    SELECT clients_id FROM phones
    """, (clients_id,))
    list_client_id = cur.fetchall()
    if clients_id in list_client_id:
        cur.execute("""
            INSERT INTO phones(phone, clients_id) VALUES (%s, %s) RETURNING clients_id;
            """, (phone, clients_id))
        print("Успешно добавили")
    else:
        print('Пользователя с данным id не существует')


def change_client(cur, client_id, first_name=None, last_name=None, email=None, phone=None):
    if first_name is not None:
        cur.execute("""
            UPDATE clients SET first_name=%s WHERE id=%s
            """, (first_name, client_id))
    if last_name is not None:
        cur.execute("""
            UPDATE clients SET last_name=%s WHERE id=%s
            """, (last_name, client_id))
    if email is not None:
        cur.execute("""
            UPDATE clients SET email=%s WHERE id=%s
            """, (email, client_id))
    if phone is not None:
        add_phone(conn, cur, client_id, phone)

    cur.execute("""
        SELECT * FROM clients;
        """)
    cur.fetchall()


def delete_phone(cur, clients_id, phone):
    cur.execute("""
        DELETE FROM phones WHERE clients_id=%s and phone=%s;
        """, (clients_id, phone))
    cur.execute("""
        SELECT * FROM phones WHERE clients_id=%s;
        """, (clients_id,))
    # print(f'удалён {cur.fetcall()}')


def delete_client(cur, clients_id):
    cur.execute("""
        SELECT clients_id FROM phones
        """, (clients_id,))
    list_client_id = cur.fetchall()
    if clients_id in list_client_id:
        cur.execute("""
            DELETE FROM phones WHERE clients_id=%;
            """, (clients_id,))
        cur.execute("""
            DELETE FROM clients WHERE client_id=%s;
            """, (clients_id,))


def find_client(cur, first_name=None, last_name=None, email=None, phone=None):
    if phone is not None:
        cur.execute("""
            SELECT cl.id FROM clients cl
            JOIN phones ph ON ph.clients_id = cl.id
            WHERE ph.phone=%s;
            """, (phone,))
    else:
        cur.execute("""
            SELECT id FROM clients 
            WHERE first_name=%s AND last_name=%s AND email=%s;
            """, (first_name, last_name, email))
    print(cur.fetchall())


def all_clients(cur):
    cur.execute("""
        SELECT * FROM clients;
        """)
    print(cur.fetchall())
    cur.execute("""
        SELECT * FROM phones;
        """)
    print(cur.fetchall())

if __name__ == '__main__':
    with psycopg2.connect(database="netology_db", user="postgres", password="Dedadeda") as conn:
        with conn.cursor() as cur:
            create_db(conn, cur)

            all_clients(cur)

            add_client(cur, 'Дмитрий', 'Планов', 'd_p@mail.com', '555421')
            add_client(cur, 'Петр', 'Масликов', 'p_m@mail.com')
            add_client(cur, 'Кристина', 'Снежинина', 'cristina@mail.com', '224124')
            add_client(cur, 'Вася', None, None)
            add_client(cur, 'Виктория', 'Медведева', None)
            add_client(cur, 'Глеб', 'Иванов', 'g_i@gmail.com')

            all_clients(cur)


            add_phone(cur, 2, 77789000)
            add_phone(cur, 1, 77703111)
            add_phone(cur, 3, 77700021)
            all_clients(cur)

            change_client(cur, 1, 'Артём')
            change_client(cur, 2, None, 'Гандебул')
            change_client(cur, 3, None, None, 'maber@mail.com')
            change_client(cur, 2, None,  '7-999-225-11-11')

            all_clients(cur)


            delete_phone(cur, 3, 77700021)

            all_clients(cur)

            find_client(cur, 'Пётр')
            find_client(cur, None, 'Масликов')
            find_client(cur, None, None, 'belozub@gmail.com')
            find_client(cur, None, None, None, '224124')

            delete_client(cur, 5)

            all_clients(cur)

conn.close()