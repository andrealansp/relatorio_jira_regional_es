from app import db
from datetime import datetime


class Usuarios(db.Model):
    __tablenane__ = 'tb_usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100),nullable=False)
    senha = db.Column(db.String(16), nullable=False)
    ultimo_acesso = db.Column(db.DateTime,default=datetime.utcnow())

    def __repr__(self):
        return f"<name> {self.usuario}, <Ultimo Acesso>{self.ultimo_acesso}"




