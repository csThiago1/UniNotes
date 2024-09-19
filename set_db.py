import mysql.connector
from mysql.connector import errorcode

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

cursor.execute("DROP DATABASE IF EXISTS `uninotes`;")

cursor.execute("CREATE DATABASE `uninotes`;")

cursor.execute("USE `uninotes`;")

# criando tabelas
TABLES = {}
TABLES['Notes'] = ('''
      CREATE TABLE `notes` (
      `note_id` int(11) NOT NULL AUTO_INCREMENT,
      `title` varchar(50) NOT NULL,
      `content` varchar(5000) NOT NULL,
      PRIMARY KEY (`note_id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Users'] = ('''
      CREATE TABLE `users` (
      `name_id` varchar(20) NOT NULL,
      `nickname` varchar(8) NOT NULL,
      `user_password` varchar(100) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for table_name in TABLES:
      table_sql = TABLES[table_name]
      try:
            print('Criando tabela {}:'.format(table_name), end=' ')
            cursor.execute(table_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

# inserindo usuarios
users_sql = 'INSERT INTO users(name_id, nickname, user_password) VALUES (%s, %s, %s)'
users = [
      ("Thiago Campos", "csthiago", "1234"),
      ("Maria Julia", "maju", "1234"),
      ("Jose Mamont", "cachorro", "1234")
]
cursor.executemany(users_sql, users)

cursor.execute('select * from uninotes.users')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo notas
notes_sql = 'INSERT INTO notes (note_id, title, content) VALUES (%s, %s, %s)'
notes = [
      ('1', 'Nota 01', 'Conteudo da Nota 01'),
      ('2', 'Nota 02', 'Conteudo da Nota 02'),
      ('3', 'Nota 03', 'Conteudo da Nota 03'),
      ('4', 'Nota 04', 'Conteudo da Nota 04')
]
cursor.executemany(notes_sql, notes)

cursor.execute('select * from uninotes.notes')
print(' -------------  Suas UniNotes:  -------------')
for notes in cursor.fetchall():
    print(notes[1])

# commitando se não nada tem efeito
conn.commit()

cursor.close()
conn.close()