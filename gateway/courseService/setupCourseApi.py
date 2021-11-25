from sqlalchemy.orm import sessionmaker

URL_API = 'https://api-cursos-fiubademy.herokuapp.com/courses'
session = None
engine = None


def set_engine(engine_rcvd):
    global engine
    global session
    engine = engine_rcvd
    session = sessionmaker(bind=engine)()

