from datetime import datetime, timedelta

from flask import Flask, render_template

from plants import Plants

app = Flask(__name__, static_url_path='/static', static_folder='static')

dao = Plants()


def parse_time_delta(strdelta: str):
	chunks = strdelta.split(" ")
	n = int(chunks[0])
	u = chunks[1].lower()
	if u in ['years', 'year']:
		return timedelta(days=n * 365)
	if u in ['months', 'month']:
		return timedelta(days=n * 30)
	if u in ['weeks', 'week']:
		return timedelta(weeks=n)
	# default, should never get here
	return timedelta(days=0)


def get_date_class(date: datetime) -> str:
	from_now = date - datetime.now()
	if from_now < timedelta(0):
		return 'past'
	elif from_now < timedelta(10):
		return 'incoming'
	else:
		return 'future'


@app.route('/garden/plants', methods=['GET'])
def get_plants():
	all = dao.get_all()
	plants = {}
	for dk in sorted(all.keys()):
		d = datetime.strptime(dk, '%Y-%m-%d')
		for pk in all[dk].keys():
			p = all[dk][pk]
			p['plant']['sowing-cls'] = get_date_class(d)
			for k in ['sprout-time', 'full-growth']:
				delta = parse_time_delta(p['plant'][k])
				p['plant'][k] = d + delta
				p['plant'][k + "-cls"] = get_date_class(d + delta)
		plants[dk] = all[dk]
	return render_template("plants.html", plants=plants)


if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8081, debug=True)
