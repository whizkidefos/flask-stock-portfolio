from flask import Flask, render_template, request, redirect, url_for, flash, session
from markupsafe import escape
from pydantic import BaseModel, validator, ValidationError, field_validator


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


app = Flask(__name__)

app.secret_key = 'c\xe5\x05\xc0\xd8F\xf6f\xaf#\xd4\xfca\xf9*=p\xd8\xb1\xd8\xc4QO\x90\x1bn\\9\x90t\x01T'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html', title='About', developer_name='Sang min Lee', company_name='iefosa')


@app.route('/stocks/')
def stocks():
    return render_template('stocks.html')


@app.route('/greet/<name>')
def greet(name):
    return f'<h1>Hello {escape(name)}!</h1>'


@app.route('/add-stock', methods=['GET', 'POST'])
def add_stock():
    if request.method == 'POST':
        # print the form data to the console
        for key, value in request.form.items():
            print(f'{key}: {value}')
        # create a new StockModel instance
        try:
            stock_data = StockModel(
                stock_symbol=request.form['stock_symbol'],
                number_of_shares=request.form['number_of_shares'],
                purchase_price=request.form['purchase_price']
            )
            print(stock_data)

            # save the form data to the session object
            session['stock_symbol'] = stock_data.stock_symbol
            session['number_of_shares'] = stock_data.number_of_shares
            session['purchase_price'] = stock_data.purchase_price
            return redirect(url_for('stocks'))
        except ValidationError as e:
            print(e)
            # flash(e, 'error')
            # return redirect(url_for('add_stock'))
    return render_template('add_stock.html')
