from dao import DAO
from flask import Flask, render_template, request, session
from wtforms import Form, StringField, validators

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

dao = DAO()


class EmailForm(Form):
	email = StringField('email')


@app.route('secret_santa', methods=['GET', 'POST'])
def secret_santa():
	if request.method == 'GET':
		return get_secret_santa()
	if request.method == 'POST':
		return post_secret_santa()


def get_secret_santa():
	form = EmailForm(**session['form']) if 'form' in session.keys() else EmailForm()
	return render_template("secret_santa_home.html", form=form)

def post_secret_santa():
	pass

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html', path=request.path), 404


if __name__ == '__main__':
	app.run('127.0.0.1', port=8081, debug=True)
