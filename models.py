from app import db
from sqlalchemy import event
from datetime import datetime
from flask_bcrypt import generate_password_hash


def gerar_hash_senha(senha):
    return generate_password_hash(senha).decode("utf-8")


class Usuarios(db.Model):
    __tablenane__ = 'tb_usuarios'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100),nullable=False)
    senha = db.Column(db.String(128), nullable=False)
    ultimo_acesso = db.Column(db.DateTime,default=datetime.utcnow())

    def __repr__(self):
        return f"<name> {self.usuario}, <Ultimo Acesso>{self.ultimo_acesso}"


@event.listens_for(Usuarios.__table__, 'after_create')
def create_users(*args, **kwargs):
    senha = gerar_hash_senha(senha='M@teus1128')
    user = Usuarios(usuario='a.alves', email='a.alves@perkons.com', senha=senha)
    db.session.add(user)
    db.session.commit()


