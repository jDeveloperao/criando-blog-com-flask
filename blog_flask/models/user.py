from extensios import db
from flask_login import UserMixin

class User(db.Model, UserMixin):

    id = db.Column(db.Integer , primary_key = True)
    nome = db.Column(db.String(30) , nullable = False)
    email = db.Column(db.String(150), unique = True , nullable = False)
    senha = db.Column(db.String(200) , nullable = False)
    is_admin = db.Column(db.Boolean , default = False)


    def __repr__(self):
        return f"<{self.nome}>"