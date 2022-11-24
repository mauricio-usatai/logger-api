import os

bind = f"0.0.0.0:{os.environ.get('APP_PORT', '8087')}"
debug = True
# Certificate
enviroment = os.environ.get('ENV')
if enviroment == 'dev':
  certfile="./certs/dev_certificate.crt"
  keyfile="./certs/dev_private.key"
elif enviroment == 'prod':
  certfile="./certs/prod_certificate.crt"
  keyfile="./certs/prod_private.key"