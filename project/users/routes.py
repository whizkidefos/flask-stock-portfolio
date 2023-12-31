from . import users_blueprint
from flask import render_template, current_app as app, request, session, flash, redirect, url_for, abort


# ------
# Routes
#
@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Save the form data to the session object
        session['first_name'] = request.form['first_name']
        session['last_name'] = request.form['last_name']
        session['email_address'] = request.form['email_address']
        session['password'] = request.form['password']

        flash(f"Added new user ({request.form['email_address']})!", 'success')
        app.logger.info(f"Added new user ({request.form['email_address']})!")

        return redirect(url_for('users.login'))

    return render_template('users/register.html')


@users_blueprint.errorhandler(403)
def page_forbidden(e):
    return render_template('users/403.html'), 403

@users_blueprint.route('/admin')
def admin():
    abort(403)