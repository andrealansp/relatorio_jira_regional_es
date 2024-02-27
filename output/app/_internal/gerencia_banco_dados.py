from app import app, db
from flask_bcrypt import generate_password_hash
from models import Usuarios


def inicializar_banco():
    with app.app_context():
        print('x')
        db.drop_all()
        db.create_all()
        usuario = Usuarios(usuario='andre', email="andrealansp@hotmail.com", senha=generate_password_hash("genesis11")
                           .decode('utf-8'))
        db.session.add(usuario)
        db.session.commit()


if __name__ == '__main__':
    inicializar_banco()
