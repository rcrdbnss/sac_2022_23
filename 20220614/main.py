from flask import Flask, render_template, request

from leagues import Leagues

app = Flask(__name__, static_url_path='/static', static_folder='static')

dao = Leagues()


@app.route('/leagues', methods=['GET'])
def get_leagues():
	leagues = dao.get_all_leagues()
	return render_template('leagues.html', leagues=leagues)


@app.route('/league/<name>', methods=['GET'])
def get_league(name):
	l = dao.get(name)
	return render_template('league.html', group_a=l['group_a'], group_b=l['group_b'], finals=l['finals'])


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html', path=request.path), 404


if __name__ == '__main__':
	app.run('127.0.0.1', port=8080, debug=True)
