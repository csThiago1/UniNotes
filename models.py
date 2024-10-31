from uninotes import db

class Users(db.Model):
    user_id = db.Column(db.String(20), primary_key=True)
    nickname = db.Column(db.String(20), nullable=False)
    user_password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.nickname}>'



class Notes(db.Model):
    note_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    color = db.Column(db.String(7), default='#ffeb3b')
    user_id = db.Column(db.String(20), db.ForeignKey('users.user_id'), nullable=False)

    def __repr__(self):
        return f'<Note {self.content[:20]}>'