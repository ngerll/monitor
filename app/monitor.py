# -*- coding: utf-8 -*-

import sys

from flask import Flask, request, render_template, make_response
import gmoninfo
import requests

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

@app.route('/sp')
def sp():
    headers = {'Authorization': 'zdio4dzwyth4gxdx0vn27ftxutz6lqhhgbh8tyti'}
    res = requests.get('https://openapi.daocloud.io/v1/apps', headers=headers).json()

    for rapp in res['app']:
        if rapp['name'] == 'wx_auto':
            if rapp['state'] == 'stopped':
                appid = rapp['id']

                surl = 'https://openapi.daocloud.io/v1/apps/%s/actions/start' % appid

                sapp = requests.post(surl, headers=headers).json()

                return render_template('sp.html', resinfo='启动命令生效')

            else:
                return render_template('sp.html', resinfo='已启动')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
