from flask import Flask, redirect, render_template, request, session, url_for
from cars import Cars
from wtforms import Form, BooleanField, FloatField, IntegerField, RadioField, validators

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

dao = Cars()


class CarQueryForm(Form):
	make = RadioField('Maker', choices=dao.get_makers())
	max_cv = IntegerField('Max CV', validators=[validators.NumberRange(min=59)])
	max_price = FloatField('Max price')
	used = BooleanField('Used', default=True)


@app.route('/cars', methods=['GET', 'POST'])
def cars():
	if request.method == 'GET':
		return get_cars()
	if request.method == 'POST':
		return post_cars()


def get_cars():
	cars = session['cars'] if 'cars' in session.keys() else None
	form = CarQueryForm(**session['form']) if 'form' in session.keys() else CarQueryForm()
	return render_template('cars.html', cars=cars, form=form)


def post_cars():
	form = CarQueryForm(request.form)
	cars = dao.query(**form.data)
	session['cars'] = cars
	session['form'] = form.data
	return redirect(url_for('cars'))


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html', path=request.path), 404


if __name__ == '__main__':
	app.run('127.0.0.1', port=8080, debug=True)
