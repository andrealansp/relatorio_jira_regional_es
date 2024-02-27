from app import app, db


def inicializar_banco():
    with app.app_context():
        db.drop_all()
        db.create_all()


if __name__ == '__main__':
    inicializar_banco()
