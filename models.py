from uninotes import db

class Notes(db.Model):
    note_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(5000), nullable=False)

    def __repr__(self):
        return f'<Note {self.title}>'

class Users(db.Model):
    name_id = db.Column(db.String(20), primary_key=True)
    nickname = db.Column(db.String(20), nullable=False)
    user_password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.nickname}>'
