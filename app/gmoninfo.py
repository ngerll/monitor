# -*- coding: utf-8 -*-

# hbchenyf

import requests
import re
from bs4 import BeautifulSoup
import tablib


def getidvalue(s_date, e_date):
    url = 'http://180.153.49.130:9000/From4A.jsp?loginName=hbchenyf&token=32|83|67|-114|103|89|74|81|96|30|-47|20|-63|-56|-12|28|107|-52|-19|-96|95|104|127|-62|-127|22|-49|50|-1.xls|-5|86|-64|89&appAcctId=2000388813&flag=1.xls'

    header = {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1.xls; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; Shuame; GWX:DOWNLOADED; GWX:RESERVED; GWX:QUALIFIED)'
    }

    cookie = requests.get(url, headers=header).cookies

    urlpage = 'http://180.153.49.130:9000/business/inspMge/plan/listMonPlan.xhtml?tabId=tab_E43EEB4585A869FECF540E47158A7CCB'

    header = {
        # 'Cookie': cookie,
        # 'Accept': '*/*',
        # 'Accept-Encoding': 'gzip, deflate',
        # 'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        # 'Connection': 'keep-alive',
        # 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Host': '180.153.49.130:9000',
        # 'Origin': 'http://180.153.49.130:9000',
        # 'Referer': 'http://180.153.49.130:9000/business/inspMge/plan/listMonPlan.xhtml?tabId=tab_E43EEB4585A869FECF540E47158A7CCB',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1.xls; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    }

    pageres = requests.get(urlpage, headers=header, cookies=cookie)

    idvalue = re.findall('id="javax.faces.ViewState" value="(.*?)"', pageres.content, re.S)[0]

    planinfos = []

    area_code = {
        "武汉": "0099906",
        "宜昌": "0099907",
        "襄阳": "0099908",
        "恩施": "0099909",
        "荆州": "0099910",
        "黄冈": "0099911",
        "十堰": "0099912",
        "孝感": "0099913",
        "荆门": "0099914",
        "江汉": "0099915",
        "咸宁": "0099916",
        "黄石": "0099917",
        "随州": "0099918",
        "鄂州": "0099919"
    }

    for area in area_code:
        planinfos.append(getinfo(idvalue, header, area, area_code[area], s_date, e_date, cookie))

    return planinfos


def getinfo(idvalue, header, area, area_code, s_date, e_date, cookie):
    url = 'http://180.153.49.130:9000/business/inspMge/plan/listMonPlan.xhtml'

    datast = {
        'AJAXREQUEST': '_viewRoot',
        'j_id114': 'j_id114',
        'autoScroll': '',
        'javax.faces.ViewState': idvalue,
        'unitid': area_code,
        'j_id114:j_id115': 'j_id114:j_id115',
        'queryMonPlanstate': 0,
        'AJAX:EVENTS_COUNT': 1,
        '': ''
    }

    requests.post(url, headers=header, data=datast, cookies=cookie)

    plan_contents = []

    dataquery = {
        'AJAXREQUEST': '_viewRoot',
        'queryForm': 'queryForm',
        'queryForm:unitHidden': area_code,
        'queryForm:statusHidden': 0,
        'queryForm:beginTimeInputDate': s_date,
        'queryForm:endTimeInputDate': e_date,
        'queryForm:queryFlag': '当前计划',
        'queryForm:currPageObjId': 1,
        'queryForm:pageSizeText': 1000,
        'javax.faces.ViewState': idvalue,
        'queryForm:j_id35': 'queryForm:j_id35',
        'AJAX:EVENTS_COUNT': 1
    }

    res = requests.post(url, data=dataquery, headers=header, cookies=cookie).content

    plans = re.findall('<tr class="rich-table-row(.*?)</tr>', res, re.S)

    i = 0

    for planinfo in plans:

        soup = BeautifulSoup(planinfo, 'lxml')
        if i < len(plans):
            plan_name = soup.find(id='listForm:list:' + str(i) + ':j_id52').get_text()
            plan_type = soup.find(id='listForm:list:' + str(i) + ':j_id57').get_text()
            plan_startdate = soup.find(id='listForm:list:' + str(i) + ':j_id62').get_text()
            plan_enddate = soup.find(id='listForm:list:' + str(i) + ':j_id67').get_text()
            sdate = soup.find(id='listForm:list:' + str(i) + ':j_id72').get_text()
            edate = soup.find(id='listForm:list:' + str(i) + ':j_id77').get_text()
            status = soup.find(id='listForm:list:' + str(i) + ':j_id82').get_text()
            typeinfo = soup.find(id='listForm:list:' + str(i) + ':j_id87').get_text()
            check_depict = soup.find(id='listForm:list:' + str(i) + ':j_id92').get_text()
            complent_rate = soup.find(id='listForm:list:' + str(i) + ':j_id97').get_text()

            plan_content = {
                'area_name': area,
                'plan_name': plan_name,
                'plan_type': plan_type,
                'plan_startdate': plan_startdate,
                'plan_enddate': plan_enddate,
                'sdate': sdate,
                'edate': edate,
                'status': status,
                'typeinfo': typeinfo,
                'check_depict': check_depict,
                'complent_rate': str(complent_rate).split('/')[0],
                'plan_rate': str(complent_rate).split('/')[1]
            }

            plan_contents.append(plan_content)

        i = i + 1

    return plan_contents


def toexcel(s_date, e_date):
    data = tablib.Dataset()

    data.headers = ('地区', '计划名称', '计划类型', '计划开始时间', '计划结束时间', '实际开始时间', '实际结束时间',
                    '状态', '巡检对象', '追加描述', '完成数量', '计划数量')

    resdatas = getidvalue(s_date, e_date)

    if len(resdatas) > 0:
        for resdata in resdatas:
                for res in resdata:
                    data.append((res['area_name'],
                                 res['plan_name'],
                                 res['plan_type'],
                                 res['plan_startdate'],
                                 res['plan_enddate'],
                                 res['sdate'],
                                 res['edate'],
                                 res['status'],
                                 res['typeinfo'],
                                 res['check_depict'],
                                 res['complent_rate'],
                                 res['plan_rate']))

        resxlsdata = data.xlsx

        # filename = s_date + 'to' + e_date + 'report.xls'
        #
        # with open(filename, 'wb') as file:
        #     file.write(resxlsdata)
        #
        # return filename

        return resxlsdata
    else:
        return 'err'


if __name__ == '__main__':
    s_date = '2016-07-01'
    e_date = '2016-07-02'
    # print getidvalue(s_date, e_date)
    toexcel(s_date, e_date)
