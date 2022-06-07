from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import os
# import psycopg2

database_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'onegai.db')
#DATABASE_URL = os.environ['DATABASE_URL']
#conn = psycopg2.connect(DATABASE_URL, sslmode='require')
engine = create_engine('sqlite:///' + database_file, convert_unicode=True)
#engine = create_engine(conn)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import models.model
    Base.metadata.create_all(bind=engine)


# Heroku Postgresアドオンを追加した場合、環境変数DATABASE_URLに
# PostgreSQLデータベースの接続先URLがセットされるので、この値が
# セットされているとき(Heroku上で動作するとき)はそれを使い、
# セットされていないとき(ローカルでのデバッグなど)はローカルのSQLiteデータベースを使うようにする。
# ローカルでpostgreSQLを指定すれば良いのか。