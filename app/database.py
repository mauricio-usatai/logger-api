import sqlalchemy as db
import app as App

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
    
  def close(self):
    self.engine.dispose()
