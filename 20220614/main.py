from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html', path=request.path), 404


if __name__ == '__main__':
	app.run('127.0.0.1', port=8080, debug=True)
