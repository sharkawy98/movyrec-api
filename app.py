from pathlib import Path
from os import environ
from sys import exit

from config import app_config_dict
from api import create_app, db, jwt
from api.users.routes import black_list


get_config_mode = environ.get('movyrek_CONFIG_MODE', 'Debug')
try:
    config_mode = app_config_dict[get_config_mode.capitalize()]
except:
    exit('Invalid Config Mode!')    

app = create_app(Path.cwd(), config_mode)
db.init_app(app)

jwt.init_app(app)
# error handling
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in black_list

if __name__ == '__main__':
    app.run()