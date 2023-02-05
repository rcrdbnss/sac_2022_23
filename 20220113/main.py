from flask import Flask, render_template, request

from slots import Slots

app = Flask(__name__,
						static_url_path='/static',
						static_folder='static')

dao = Slots()


@app.route('/wines/', methods=['GET'])
def get_wines():
	slots = dao.get_all()
	slots_dict = {
		'sparkling': [], 'white': [], 'red': [], 'sweet': []
	}
	for s in slots:
		slots_dict[s['label']['type']].append(s)
	return render_template('wines.html',
												 wines=slots_dict,
												 sparkling=slots_dict['sparkling'],
												 white=slots_dict['white'],
												 red=slots_dict['red'],
												 sweet=slots_dict['sweet'])

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html', path=request.path), 404


if __name__ == '__main__':
	app.run(host='127.0.0.1', port=8081, debug=True)
