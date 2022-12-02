import sqlalchemy as db
import app as App
import warnings
from sqlalchemy import exc as sa_exc

from sqlalchemy.orm import sessionmaker

from app.model import Log

class Database:
  def __init__(self):
    self.db = App.Config.DATABASE
    self.url = App.Config.DATABASE_URL
    self.port = App.Config.DATABASE_PORT

    self.user = App.Config.DATABASE_USER
    self.password = App.Config.DATABASE_PASSWORD

    self.engine = None

  def connect(self):
    self.engine = db.create_engine(
      f'mysql://{self.user}:{self.password}@{self.url}:{self.port}/{self.db}'
    )

  def list_tables(self):
    table_names = self.engine.table_names()
    return [table for table in table_names]

  def select_between_dates(self, service_name, date_ini, date_end):
    service_name = service_name.replace('-', '_')
    metadata = db.MetaData()
    table = db.Table(
      service_name,
      metadata,
      autoload=True,
      autoload_with=self.engine,
    )
  
    stmt = db.select([
      table.columns.date,
      table.columns.level,
      table.columns.log_message,
    ]).where(db.and_(
      table.columns.date >= date_ini,
      table.columns.date <= date_end,
    ))

    conn = self.engine.connect()
    results = conn.execute(stmt).fetchall()
    conn.close()

    return [{
      'date': log[0],
      'level': log[1],
      'log_message': log[2],
    } for log in results]

  def create_table_if_not_exists(self, service_name):
    LogModel = self.get_log_model(service_name)
    LogModel.__table__.create(bind=self.engine, checkfirst=True)

  def insert(self, data):
    LogModel = self.get_log_model(data['service_name'])
    del data['service_name']
    Session = sessionmaker(bind=self.engine)
    with Session() as session:
      session.add(LogModel(**data))
      session.commit()
  
  def get_log_model(self, service_name):
    with warnings.catch_warnings():
      warnings.simplefilter('ignore', category=sa_exc.SAWarning)
      class_name = f'Log_{service_name}'
      Model = type(class_name, (Log,), {
        '__tablename__': service_name
      })
    return Model
    
  def close(self):
    self.engine.dispose()
