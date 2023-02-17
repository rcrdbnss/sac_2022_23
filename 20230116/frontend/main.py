from datetime import datetime
from dateutil.relativedelta import relativedelta
from dao import DAO
from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__, static_url_path='/static', static_folder='static')

dao = DAO()

DATE_FMT = '%d-%m-%Y'


@app.route('/bollette', methods=['GET'])
def get_bills():
	bill_dates = np.sort(np.array(dao.get_bills()))[::-1]
	l = np.min([12, len(bill_dates)])
	bill_dates_str = []
	for i in range(l):
		# emit_date = datetime.strptime(bill_dates[i], DAO.IN_DATE_FMT)
		bill_dates_str.append(bill_dates[i].strftime(DAO.HR_DATE_FMT))
	return render_template("bills.html", bill_dates=bill_dates_str)

	# today = datetime.today()
	# last_bill = datetime(year=today.year, month=today.month, day=1)
	# bill_dates = [last_bill.strftime(DATE_FMT)]
	# for i in range(1, 12):
	# 	bill_dates.append((last_bill + relativedelta(months=-i)).strftime(DATE_FMT))
	# return render_template("bills.html", bill_dates=bill_dates)


@app.route('/bolletta/<emit_date>')
def get_bill_details(emit_date):
	emit_date_str = emit_date
	emit_date = datetime.strptime(emit_date, DAO.HR_DATE_FMT)
	bill = dao.get_bill_by_emit_date(emit_date)
	return render_template("bill_details.html", bill=bill, emit_date=emit_date_str)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html', path=request.path), 404


if __name__ == '__main__':
	app.run('127.0.0.1', port=8081, debug=True)
