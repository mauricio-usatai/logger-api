from flask import jsonify, request
from app import app
from app.database import Database

@app.route('/logs/<service_name>')
def get_logs(service_name):
  date_ini = int(request.args.get('date_ini'))
  date_end = int(request.args.get('date_end'))
  
  db = Database()
  db.connect()

  logs = db.select_between_dates(service_name, date_ini, date_end)

  db.close()

  return jsonify({ 'logs': logs }), 200

@app.route('/services')
def get_services():
  db = Database()
  db.connect()

  services = db.list_tables()

  db.close()

  return jsonify({ 'services': services }), 200
  