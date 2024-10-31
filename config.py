SECRET_KEY = 'admin'
SQLALCHEMY_DATABASE_URI= \
    "{SGBD}://{user}:{password}@{server}/{database}".format(
        SGBD = 'mysql+mysqlconnector',
        user = 'root',
        password = 'admin',
        server = 'localhost',
        database = 'uninotes'
    )