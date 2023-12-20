from flask import render_template, flash
from project import create_app
from datetime import date


# Call the application factory function to construct a Flask application
# instance using the development configuration
app = create_app()


@app.route('/about')
def about():
    get_current_year = date.today().year
    flash('Thanks for learning about this site!', 'info')
    return render_template('about.html', title='About', developer_name='Sang min Lee', company_name='iefosa', get_current_year=get_current_year)
