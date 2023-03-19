import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as dec

from os import pardir, makedirs, path

SqlAlchemyBase = dec.declarative_base()


def global_init(db_file):
    global create_session
    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    makedirs(path.abspath(path.join(db_file, pardir)), exist_ok=True)

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)

    create_session = orm.sessionmaker(bind=engine)