import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

def database_exists(cursor, db_name):
    cursor.execute("SHOW DATABASES;")
    databases = cursor.fetchall()
    return any(db[0] == db_name for db in databases)

db_name = 'uninotes'
print("Conectando...")

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Existe algo errado no nome de usuário ou senha')
    else:
        print(err)

cursor = conn.cursor()

# Verifica se o banco de dados existe e cria se não existir
if not database_exists(cursor, db_name):
    print(f"Criando banco de dados '{db_name}'...")
    cursor.execute(f"CREATE DATABASE {db_name};")
    cursor.execute(f"USE {db_name};")

    # Estrutura das tabelas
    TABLES = {
        'Users': '''
            CREATE TABLE users (
                user_id varchar(20) NOT NULL,
                nickname varchar(20) NOT NULL,
                user_password varchar(100) NOT NULL,
                PRIMARY KEY (user_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
        ''',
        'Notes': '''
            CREATE TABLE notes (
                note_id int(11) NOT NULL AUTO_INCREMENT,
                content text NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                color varchar(7) DEFAULT '#ffeb3b',
                user_id varchar(20) NOT NULL,
                PRIMARY KEY (note_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
        '''
    }

    # Criação das tabelas
    for table_name, table_sql in TABLES.items():
        try:
            print(f'Criando tabela {table_name}: ', end='')
            cursor.execute(table_sql)
            print('OK')
        except mysql.connector.Error as err:
            print(f"Erro ao criar tabela {table_name}: {err}")

    # Inserindo dados de exemplo
    users_sql = 'INSERT INTO users (user_id, nickname, user_password) VALUES (%s, %s, %s)'
    users = [
        ("csthiago", "Thiago Campos", generate_password_hash("1234")),
        ("maju", "Maria Julia", generate_password_hash("1234")),
        ("cachorro", "Jose Mamont", generate_password_hash("1234"))
    ]
    cursor.executemany(users_sql, users)

    notes_sql = 'INSERT INTO notes (content, color, user_id) VALUES (%s, %s, %s)'
    notes = [
        ('Conteúdo da Nota 01', '#ffeb3b', "csthiago"),
        ('Conteúdo da Nota 02', '#ff5722', "maju"),
        ('Conteúdo da Nota 03', '#4caf50', "cachorro"),
        ('Conteúdo da Nota 04', '#ffeb3b', "csthiago")
    ]
    cursor.executemany(notes_sql, notes)

    conn.commit()
    print("Banco de dados e tabelas criados com sucesso!")
else:
    print(f"O banco de dados '{db_name}' já existe. Nenhuma ação necessária.")

# Fechando a conexão
cursor.close()
conn.close()
