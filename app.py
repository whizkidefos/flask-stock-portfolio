from flask import Flask, render_template, flash
import logging
from flask.logging import default_handler
from logging.handlers import RotatingFileHandler
import os

# Import the Blueprint objects from the project's folder
from project.stocks import stocks_blueprint
from project.users import users_blueprint

app = Flask(__name__)

# Load the configuration from the config.py file
config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
app.config.from_object(config_type)


# Remove the default Flask logger
app.logger.removeHandler(default_handler)

# Logger configuration
file_handler = RotatingFileHandler('instance/flask-stock-portfolio.log', maxBytes=16384, backupCount=20)
file_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s [in %(pathname)s:%(lineno)d]')
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

# Set the log level to INFO
app.logger.info('Flask Stock Portfolio App Started')

# Register the Blueprints with the Flask application object
app.register_blueprint(stocks_blueprint)
app.register_blueprint(users_blueprint, url_prefix=str('/users'))


@app.route('/about')
def about():
    flash('Thanks for learning about this site!', 'info')
    return render_template('about.html', title='About', developer_name='Sang min Lee', company_name='iefosa')
