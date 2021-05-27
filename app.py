from pathlib import Path
from os import environ
from sys import exit

from config import app_config_dict
from api import create_app, db, jwt


get_config_mode = environ.get('movyrek_CONFIG_MODE', 'Debug')
try:
    config_mode = app_config_dict[get_config_mode.capitalize()]
except:
    exit('Invalid Config Mode!')    

app = create_app(Path.cwd(), config_mode)
db.init_app(app)
jwt.init_app(app)

if __name__ == '__main__':
    app.run()