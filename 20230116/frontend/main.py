from datetime import datetime
from dateutil.relativedelta import relativedelta
from dao import DAO
from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__, static_url_path='/static', static_folder='static')

dao = DAO()


@app.route('/bollette', methods=['GET'])
def get_bills():
    emit_dates = np.sort(np.array(dao.get_bills()))[::-1]
    ln = np.min([12, len(emit_dates)])
    emit_dates_str = []
    for i in range(ln):
        emit_dates_str.append(emit_dates[i].strftime(DAO.HR_DATE_FMT))
    return render_template("bills.html", emit_dates=emit_dates_str)


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
