from pathlib import Path
from os import environ
from sys import exit

from config import app_config_dict
from api import create_app, db, jwt, mail, cors
from api.base_models import TokenBlocklist


get_config_mode = environ.get('movyrek_CONFIG_MODE', 'Debug')
try:
    config_mode = app_config_dict[get_config_mode.capitalize()]
except:
    exit('Invalid Config Mode!')    

app = create_app(Path.cwd(), config_mode)
cors.init_app(app)
db.init_app(app)

jwt.init_app(app)
# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id)\
                .filter_by(jti=jti).scalar()
    return token is not None


mail.init_app(app)

if __name__ == '__main__':
    app.run()