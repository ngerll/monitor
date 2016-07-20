# -*- coding: utf-8 -*-

import sys

from flask import Flask, request, render_template, make_response
import gmoninfo

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)


@app.route('/monitor')
def index():
    return render_template('index.html')


@app.route('/monitor/getinfo')
def getrateinfo():
    s_date = request.args.get('s_date')
    e_date = request.args.get('e_date')

    result = gmoninfo.toexcel(s_date, e_date)
    filename = s_date + 'to' + e_date + '巡检计划明细'

    response = make_response(result)
    # response.headers["Content-Disposition"] = "attachment; filename={0}.csv".format(filename)

    response.headers['Content-Type'] = 'application/vnd.ms-excel'
    response.headers['Content-Disposition'] = 'attachment; filename={0}.xlsx'.format(filename)

    return response

# if __name__ == '__main__':
#     app.run(debug=True)
