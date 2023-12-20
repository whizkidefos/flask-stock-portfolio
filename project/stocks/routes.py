from flask import render_template, current_app as app, request, session, flash, redirect, url_for
from pydantic import BaseModel, ValidationError, field_validator
from . import stocks_blueprint
from datetime import date


# -----------------
# Request Callbacks
# -----------------

@stocks_blueprint.before_request
def stocks_before_request():
    current_app.logger.info('Calling before_request() for the stocks blueprint...')


@stocks_blueprint.after_request
def stocks_after_request(response):
    current_app.logger.info('Calling after_request() for the stocks blueprint...')
    return response


@stocks_blueprint.teardown_request
def stocks_teardown_request(error=None):
    current_app.logger.info('Calling teardown_request() for the stocks blueprint...')


# --------------
# Helper Classes
#
from . import stocks_blueprint


class StockModel(BaseModel):
    # Class for parsing new stock data from the form
    stock_symbol: str
    number_of_shares: int
    purchase_price: float

    @field_validator('stock_symbol')
    def stock_symbol_must_be_valid(cls, value):
        if not value.isalpha() or len(value) > 5:
            raise ValueError('stock_symbol must contain only alphabetic characters and be 1-5 characters long')
        return value.upper()


# ------
# Routes
#
@stocks_blueprint.route('/')
def index():
    get_current_year = date.today().year
    app.logger.info('Calling the index() function.')
    return render_template('stocks/index.html', get_current_year=get_current_year)


@stocks_blueprint.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        try:
            stock_data = StockModel(
                stock_symbol=request.form['stock_symbol'],
                number_of_shares=request.form['number_of_shares'],
                purchase_price=request.form['purchase_price']
            )
            print(stock_data)

            # Save the form data to the session object
            session['stock_symbol'] = stock_data.stock_symbol
            session['number_of_shares'] = stock_data.number_of_shares
            session['purchase_price'] = stock_data.purchase_price

            flash(f"Added new stock ({stock_data.stock_symbol})!", 'success')
            app.logger.info(f"Added new stock ({request.form['stock_symbol']})!")

            return redirect(url_for('stocks.list_stocks'))
        except ValidationError as e:
            print(e)

    return render_template('stocks/add_stock.html')


@stocks_blueprint.route('/stocks/')
def list_stocks():
    return render_template('stocks/list_stocks.html')
