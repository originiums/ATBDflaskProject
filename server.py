# -*- codeing = utf-8 -*-
# @Time :2023/7/19 10:49
# @Author:X
# @File : server.py
# @Software: PyCharm
import decimal
import json

from flask import Flask, render_template, jsonify, request, url_for, redirect
import pymysql

app = Flask(__name__)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return int(o)
        super(DecimalEncoder, self).default(o)

hosturl = '127.0.0.1'
sqldb = 'atbd'

@app.route("/")
def my_echart():
    return render_template('login.html')
    # conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='buggerexe')  # 建立数据库连接
    # cur = conn.cursor()
    # sqlmale = ' SELECT count(*) FROM  greatri where zl >= 1000 '
    # sqlfemale = ' SELECT count(*) FROM  greatri where zl < 1000'
    # sqls = ' SELECT zl FROM  greatri '
    # cur.execute(sqlmale)  # 执行单条sql语句
    # maleresult = cur.fetchall()  # 接收全部的返回结果行
    # cur.execute(sqlfemale)
    # femaleresult = cur.fetchall()
    # cur.execute(sqls)
    # results = cur.fetchall()
    # male_num = maleresult[0][0]
    # female_num = femaleresult[0][0]
    # num1 = []
    # for result in results:
    #     num1.append(result[0])
    # cur.close()  # 关闭指针对象
    # conn.close()  # 关闭连接对象
    # # print(male_num)#测试
    # # print(female_num)
    # # print(num1)
    # return render_template('bar.html', male_num=male_num, female_num=female_num,
    #                        num1=num1)  # 先引入bar.html，同时根据后面传入的参数，对html进行修改渲染


@app.route("/planeMap")
def show_da1():
    return redirect(url_for('show_datas', start='%', date='2023-08-04', end='%'))


@app.route("/planeMap/<start>/<end>/<date>")
def show_datas(start='%', date='2023-08-04', end='%'):
    # print(start, date, end)
    return render_template('index.html', start=start, end=end, date=date)


@app.route("/planeMap/trd", methods=['POST'])
def time_range_data():
    data = json.loads(request.form.get('data'))
    start_area = data['start_area']
    end_area = data['end_area']
    act_date = data['act_date']
    # print(start_area, end_area, act_date)

    conn = pymysql.connect(host=hosturl, user='root', password='', db=sqldb)  # 建立数据库连接
    cur = conn.cursor()
    xdays = ['00~03', '03~06','06~09','09~12','12~15','15~18','18~21', '21~24']
    jsonData = {}
    yvalues = []
    for i in range(0, 21, 3):
        sql = "SELECT count(1) FROM airline " \
              "WHERE start_area like '%s' and end_area like '%s' and act_date like '%s' " \
              "and takeoff_time > time(date_add('%s',interval %d hour)) " \
              "and takeoff_time <= time(date_add('%s',interval %d hour)); " % (start_area, end_area, act_date, act_date + ' 00:00:00', i, act_date + ' 00:00:00', i+3)  # sql语句
        # print(sql)
        cur.execute(sql)  # execute(query, args):执行单条sql语句。
        see1 = cur.fetchall()  # 使结果全部可看
        for data1 in see1:
            yvalues.append(data1[0])

    jsonData['xdays'] = xdays
    jsonData['yvalues'] = yvalues
    # print(jsonData)
    # 将json格式转成str，因为如果直接将dict类型的数据写入json会发生报错，因此将数据写入时需要用到该函数。
    j = json.dumps(jsonData, cls=DecimalEncoder, ensure_ascii=False)
    # print(j)
    cur.close()
    conn.close()
    # 渲染html模板
    return (j)

@app.route("/planeMap/map", methods=['POST'])
def map_line_data():
    data = json.loads(request.form.get('data'))
    start_area = data['start_area']
    end_area = data['end_area']
    act_date = data['act_date']
    # print(start_area, end_area, act_date)

    conn = pymysql.connect(host=hosturl, user='root', password='', db=sqldb)  # 建立数据库连接
    cur = conn.cursor()
    sql = "SELECT start_area, end_area FROM airline " \
          "WHERE start_area like '%s' and end_area like '%s' and act_date like '%s' " \
          "GROUP BY start_area, end_area" % (start_area, end_area, act_date)  # sql语句
    # print(sql)
    cur.execute(sql)  # execute(query, args):执行单条sql语句。
    see = cur.fetchall()  # 使结果全部可看
    sta = []
    jsonData = {}
    eda = []

    for data in see:
        sta.append(data[0])
        eda.append(data[1])

    jsonData['sta'] = sta
    jsonData['eda'] = eda
    # print(jsonData)
    # 将json格式转成str，因为如果直接将dict类型的数据写入json会发生报错，因此将数据写入时需要用到该函数。
    j = json.dumps(jsonData, cls=DecimalEncoder, ensure_ascii=False)
    # print(j)
    cur.close()
    conn.close()
    # 渲染html模板
    return (j)



@app.route("/planeMap/prd", methods=['POST'])
def price_range_data():
    data = json.loads(request.form.get('data'))
    start_area = data['start_area']
    end_area = data['end_area']
    act_date = data['act_date']
    # print(start_area, end_area, act_date)
    xaxis = ['600以下', '600~800', '800~1000', '1000~1200', '1200~1400', '1400~1600', '1600以上']
    jsonData = {}
    yvalues1 = []
    yvalues2 = []

    conn = pymysql.connect(host=hosturl, user='root', password='', db=sqldb)  # 建立数据库连接
    cur = conn.cursor()
    sql = "SELECT count(1) FROM airline " \
          "WHERE start_area like '%s' and end_area like '%s' and act_date like '%s' " \
          "and price <= 600" % (start_area, end_area, act_date)  # sql语句
    # print(sql)
    cur.execute(sql)  # execute(query, args):执行单条sql语句。
    see1 = cur.fetchall()  # 使结果全部可看
    for data1 in see1:
        yvalues1.append(data1[0])
    sql = "SELECT count(1) FROM airline " \
          "WHERE start_area like '%s' and end_area like '%s' and act_date like date_add('%s', interval 1 day) " \
          "and price <= 600" % (start_area, end_area, act_date)  # sql语句
    # print(sql)
    cur.execute(sql)  # execute(query, args):执行单条sql语句。
    see2 = cur.fetchall()  # 使结果全部可看
    for data2 in see2:
        yvalues2.append(data2[0])

    for i in range(600,1401,200):
        sql = "SELECT count(1) FROM airline " \
              "WHERE start_area like '%s' and end_area like '%s' and act_date like '%s' " \
              "and price > %d and price <= %d " % (start_area, end_area, act_date, i, i+200)  # sql语句
        # print(sql)
        cur.execute(sql)  # execute(query, args):执行单条sql语句。
        see1 = cur.fetchall()  # 使结果全部可看
        for data1 in see1:
            yvalues1.append(data1[0])
        sql = "SELECT count(1) FROM airline " \
              "WHERE start_area like '%s' and end_area like '%s' and act_date like date_add('%s', interval 1 day) " \
              "and price > %d and price <= %d " % (start_area, end_area, act_date, i, i+200)  # sql语句
        # print(sql)
        cur.execute(sql)  # execute(query, args):执行单条sql语句。
        see2 = cur.fetchall()  # 使结果全部可看
        for data2 in see2:
            yvalues2.append(data2[0])

    sql = "SELECT count(1) FROM airline " \
          "WHERE start_area like '%s' and end_area like '%s' and act_date like '%s' " \
          "and price > 1600" % (start_area, end_area, act_date)  # sql语句
    # print(sql)
    cur.execute(sql)  # execute(query, args):执行单条sql语句。
    see1 = cur.fetchall()  # 使结果全部可看
    for data1 in see1:
        yvalues1.append(data1[0])
    sql = "SELECT count(1) FROM airline " \
          "WHERE start_area like '%s' and end_area like '%s' and act_date like date_add('%s', interval 1 day) " \
          "and price > 1600" % (start_area, end_area, act_date)  # sql语句
    # print(sql)
    cur.execute(sql)  # execute(query, args):执行单条sql语句。
    see2 = cur.fetchall()  # 使结果全部可看
    for data2 in see2:
        yvalues2.append(data2[0])

    jsonData['xaxis'] = xaxis
    jsonData['yvalues1'] = yvalues1
    jsonData['yvalues2'] = yvalues2
    # print(jsonData)
    # 将json格式转成str，因为如果直接将dict类型的数据写入json会发生报错，因此将数据写入时需要用到该函数。
    j = json.dumps(jsonData, cls=DecimalEncoder, ensure_ascii=False)
    # print(j)
    cur.close()
    conn.close()
    # 渲染html模板
    return (j)

@app.route("/planeMap/lrd", methods=['POST'])
def lose_rate_data():
    data = json.loads(request.form.get('data'))
    start_area = data['start_area']
    end_area = data['end_area']
    act_date = data['act_date']
    # print(start_area, end_area, act_date)
    conn = pymysql.connect(host=hosturl, user='root', password='', db=sqldb)  # 建立数据库连接
    cur = conn.cursor()
    sql = "SELECT air_id, round(AVG(late_rate),2) as lr FROM airline " \
          "WHERE start_area like '%s' and end_area like '%s' and act_date like '%s' " \
          "group by air_id " \
          "order by lr desc limit 20" % (start_area, end_area, act_date)  # sql语句
    # print(sql)
    cur.execute(sql)  # execute(query, args):执行单条sql语句。
    see = cur.fetchall()  # 使结果全部可看
    xaxis = []
    jsonData = {}
    yvalues1 = []
    for data in see:
        xaxis.append(data[0])
        yvalues1.append(data[1])
    jsonData['xaxis'] = xaxis
    jsonData['yvalues1'] = yvalues1
    # print(jsonData)
    # 将json格式转成str，因为如果直接将dict类型的数据写入json会发生报错，因此将数据写入时需要用到该函数。
    j = json.dumps(jsonData, cls=DecimalEncoder, ensure_ascii=False)
    cur.close()
    conn.close()
    return (j)

@app.route("/planeMap/acomd", methods=['POST'])
def air_com_data():
    data = json.loads(request.form.get('data'))
    start_area = data['start_area']
    end_area = data['end_area']
    act_date = data['act_date']
    # print(start_area, end_area, act_date)

    conn = pymysql.connect(host=hosturl, user='root', password='', db=sqldb)  # 建立数据库连接
    cur = conn.cursor()
    sql = "SELECT name, count(1) as acc FROM airline " \
          "WHERE start_area like '%s' and end_area like '%s' and act_date like '%s' " \
          "group by name " \
          "order by acc desc limit 6" % (start_area, end_area, act_date)  # sql语句
    # sql = "SELECT cabin, count(1) as acc FROM airline " \
    #       "WHERE start_area like '%s' and end_area like '%s' and act_date like '%s' " \
    #       "group by cabin " \
    #       "order by acc limit 15" % (start_area, end_area, act_date)  # sql语句
    # print(sql)
    cur.execute(sql)  # execute(query, args):执行单条sql语句。
    see = cur.fetchall()  # 使结果全部可看
    xaxis = []
    jsonData = {}
    yvalues1 = []

    for data in see:
        xaxis.append(data[0])
        yvalues1.append(data[1])

    jsonData['xaxis'] = xaxis
    jsonData['yvalues1'] = yvalues1
    # print(jsonData)
    # 将json格式转成str，因为如果直接将dict类型的数据写入json会发生报错，因此将数据写入时需要用到该函数。
    j = json.dumps(jsonData, cls=DecimalEncoder, ensure_ascii=False)
    # print(j)
    cur.close()
    conn.close()
    # 渲染html模板
    return (j)

@app.route("/planeMap/ptd", methods=['POST'])
def plane_type_data():
    data = json.loads(request.form.get('data'))
    start_area = data['start_area']
    end_area = data['end_area']
    act_date = data['act_date']
    # print(start_area, end_area, act_date)

    conn = pymysql.connect(host=hosturl, user='root', password='', db=sqldb)  # 建立数据库连接
    cur = conn.cursor()
    sql = "SELECT type, count(1) as acc FROM airline " \
          "WHERE start_area like '%s' and end_area like '%s' and act_date like '%s' " \
          "group by type " \
          "order by acc desc limit 5" % (start_area, end_area, act_date)  # sql语句
    # print(sql)
    cur.execute(sql)  # execute(query, args):执行单条sql语句。
    see = cur.fetchall()  # 使结果全部可看
    xaxis = []
    jsonData = {}
    yvalues1 = []


    for data in see:
        xaxis.append(data[0])
        yvalues1.append(data[1])

    sum = 0
    sql = "SELECT sum(1) FROM airline " \
          "WHERE start_area like '%s' and end_area like '%s' and act_date like '%s' " % (start_area, end_area, act_date)  # sql语句
    # print(sql)
    cur.execute(sql)  # execute(query, args):执行单条sql语句。
    see1 = cur.fetchall()
    for data in see1:
        sum = data[0]


    jsonData['xaxis'] = xaxis
    jsonData['yvalues1'] = yvalues1
    jsonData['sum'] = sum
    # print(jsonData)
    # 将json格式转成str，因为如果直接将dict类型的数据写入json会发生报错，因此将数据写入时需要用到该函数。
    j = json.dumps(jsonData, cls=DecimalEncoder, ensure_ascii=False)
    # print(j)
    cur.close()
    conn.close()
    # 渲染html模板
    return (j)

@app.route("/planeMap/apd", methods=['POST'])
def around_price_data():
    data = json.loads(request.form.get('data'))
    start_area = data['start_area']
    end_area = data['end_area']
    act_date = data['act_date']
    # print(start_area, end_area, act_date)
    xaxis = []
    jsonData = {}
    yvalues1 = []
    yvalues2 = []

    conn = pymysql.connect(host=hosturl, user='root', password='', db=sqldb)  # 建立数据库连接
    cur = conn.cursor()

    for i in range(0,7,1):
        sql = "SELECT day(act_date), price FROM airline " \
              "WHERE start_area like '%s' and end_area like '%s' and act_date like date_add('%s', interval %d day) " \
              "order by price limit 1;" % (start_area, end_area, act_date, i)  # sql语句
        # print(sql)
        cur.execute(sql)  # execute(query, args):执行单条sql语句。
        see1 = cur.fetchall()  # 使结果全部可看
        for data1 in see1:
            xaxis.append(data1[0])
            yvalues1.append(data1[1])
        sql = "SELECT avg(price) FROM airline " \
              "WHERE start_area like '%s' and end_area like '%s' and act_date like date_add('%s', interval %d day) " % (start_area, end_area, act_date, i)  # sql语句
        print(sql)
        cur.execute(sql)  # execute(query, args):执行单条sql语句。
        see2 = cur.fetchall()  # 使结果全部可看
        for data2 in see2:
            yvalues2.append(data2[0])


    jsonData['xaxis'] = xaxis
    jsonData['yvalues1'] = yvalues1
    jsonData['yvalues2'] = yvalues2
    # print(jsonData)
    # 将json格式转成str，因为如果直接将dict类型的数据写入json会发生报错，因此将数据写入时需要用到该函数。
    j = json.dumps(jsonData, cls=DecimalEncoder, ensure_ascii=False)
    # print(j)
    cur.close()
    conn.close()
    # 渲染html模板
    return (j)


if __name__ == '__main__':
    app.run(debug=True)  # 启用调试模式
