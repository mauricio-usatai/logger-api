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

@app.route('/log', methods=['POST'])
def log():
  data = request.json
  data['service_name'] = data['service_name'].replace('-', '_')
  db = Database()
  db.connect()
  db.create_table_if_not_exists(data['service_name'])
  db.insert(data)
  db.close()

  return jsonify({ 'status': 'created' }), 201
  