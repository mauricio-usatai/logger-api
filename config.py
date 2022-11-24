import os

class Config:
  DATABASE_URL = os.environ.get('DATABASE_URL', '127.0.0.1')
  DATABASE_PORT = int(os.environ.get('DATABASE_PORT', 3306))
  DATABASE_USER = os.environ.get('DATABASE_USER','logger')
  DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD', 'logger')
  DATABASE = os.environ.get('DATABASE', 'logger')