from sqlalchemy.orm import sessionmaker

URL_API = 'https://api-consultas-fiubademy.herokuapp.com'
session = None
engine = None


def set_engine(engine_rcvd):
    global engine
    global session
    engine = engine_rcvd
    session = sessionmaker(bind=engine)()

