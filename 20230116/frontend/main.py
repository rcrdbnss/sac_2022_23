from datetime import datetime

import numpy as np
from flask import Flask, render_template, request

import common
from dao import DAO

app = Flask(__name__, static_url_path='/static', static_folder='static')

dao = DAO()


@app.route('/bollette', methods=['GET'])
def get_bills():
    emit_dates = np.sort(np.array(dao.get_bills()))[::-1]
    ln = np.min([12, len(emit_dates)])
    emit_dates_str = []
    for i in range(ln):
        # emit_dates_str.append(emit_dates[i].strftime(DAO.HR_DATE_FMT))
        emit_dates_str.append(common.str_from_date(emit_dates[i]))
    return render_template("bills.html", emit_dates=emit_dates_str)


@app.route('/bolletta/<emit_date>')
def get_bill_details(emit_date):
    emit_date_str = emit_date
    emit_date = common.date_from_str(emit_date_str)  # datetime.strptime(emit_date, DAO.HR_DATE_FMT)
    if not emit_date:
        return page_not_found(None)

    bill = dao.get_bill_by_emit_date(emit_date)
    if not bill:
        return page_not_found(None)

    for k in ['start_date', 'end_date', 'last_read_date']:
        bill[k] = common.str_from_date(bill[k])  # bill[k].strftime(DAO.HR_DATE_FMT)
    return render_template("bill_details.html", bill=bill, emit_date=emit_date_str)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', path=request.path), 404


if __name__ == '__main__':
    app.run('127.0.0.1', port=8081, debug=True)
