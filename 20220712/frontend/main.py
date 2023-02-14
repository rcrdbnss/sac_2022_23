from dao import DAO
from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/static', static_folder='static')

dao = DAO()
@app.route('/pool/<date>/<time>')
def get_pool_state(date, time):
	data_ = dao.get_dt_rsvs(date, time)
	data = {}
	for d_ in data_:
		data[d_['lane']] = d_['n_users']
	return render_template('pool_state.html', data=data, date=date, time=time)


@app.route('/pool/<date>/<time>/<lane>')
def get_lane_state(date, time, lane):
	lane = int(lane)
	users = dao.get_users(date, time, lane)
	users_time = {}
	for u in users:
		users_time[u] = []
		y = dao.get_ud_rsvs(u, date)
		for x in y:
			users_time[u].append(x['time'])
		if time not in users_time[u]:
			del users_time[u]
	return render_template('lane_state.html', date=date, time=time, users_time=users_time)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html', path=request.path), 404


if __name__ == '__main__':
	app.run('127.0.0.1', port=8080, debug=True)
