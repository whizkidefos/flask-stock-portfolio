from flask import render_template, flash
from project import create_app
from datetime import date


# Call the application factory function to construct a Flask application
# instance using the development configuration
app = create_app()