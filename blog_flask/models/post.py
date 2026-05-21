from extensios import db
from datetime import datetime , timedelta

class Post(db.Model):

    id = db.Column(db.Integer , primary_key = True)
    titulo = db.Column(db.String(70) , nullable = False)
    conteudo = db.Column(db.String(1000) , nullable = False)
    dono = db.Column(db.Integer , nullable = False)
    nome_dono = db.Column(db.String(30) , nullable = False)
    estado = db.Column(db.Boolean , default = False)
    data_created = db.Column(db.DateTime, default = datetime.utcnow)
    def __repr__ (self):
        return f"<{self.titulo}>"