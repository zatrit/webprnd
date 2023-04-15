import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as dec
from os import pardir, makedirs, path

SqlAlchemyBase = dec.declarative_base()


__factory: ... = None


def global_init(db_file: str):
    global __factory

    if not db_file or not db_file.strip():
        raise IOError("Необходимо указать файл базы данных.")

    makedirs(path.abspath(path.join(db_file, pardir)), exist_ok=True)

    conn_str = f"sqlite:///{db_file.strip()}?check_same_thread=False"
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> orm.Session:
    return __factory()
