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
    return redirect(url_for('show_datas', start='%', date='2023-08-08', end='%'))


@app.route("/planeMap/<start>/<end>/<date>")
def show_datas(start='%', date='2023-08-08', end='%'):
    print(start, date, end)
    return render_template('index.html', start=start, end=end, date=date)


@app.route("/planeMap/trd", methods=['POST'])
def time_range_data():
    data = json.loads(request.form.get('data'))
    start_area = data['start_area']
    end_area = data['end_area']
    act_date = data['act_date']
    # print(start_area, end_area, act_date)

    conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='buggerexe')  # 建立数据库连接
    cur = conn.cursor()
    sql = "SELECT time_range, sum(count_num) FROM time_sum " \
          "WHERE start_area like '%s' and end_area like '%s' and act_date like '%s' " \
          "GROUP BY time_range" % (start_area, end_area, act_date)  # sql语句
    print(sql)
    cur.execute(sql)  # execute(query, args):执行单条sql语句。
    see = cur.fetchall()  # 使结果全部可看
    xdays = []
    jsonData = {}
    yvalues = []

    for data in see:
        xdays.append(data[0])
        yvalues.append(data[1])

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

    conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='buggerexe')  # 建立数据库连接
    cur = conn.cursor()
    sql = "SELECT start_area, end_area FROM time_sum " \
          "WHERE start_area like '%s' and end_area like '%s' and act_date like '%s' " \
          "GROUP BY start_area, end_area" % (start_area, end_area, act_date)  # sql语句
    print(sql)
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
    xaxis = ['400以下', '400~600', '600~800', '800~1000', '1000~1200', '1200~1400', '1400以上']
    jsonData = {}
    yvalues1 = []
    yvalues2 = []

    conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='buggerexe')  # 建立数据库连接
    cur = conn.cursor()
    sql = "SELECT count(1) FROM airline " \
          "WHERE start_area like '%s' and end_area like '%s' and act_date like '%s' " \
          "and Aprice <= 400" % (start_area, end_area, act_date)  # sql语句
    #print(sql)
    cur.execute(sql)  # execute(query, args):执行单条sql语句。
    see1 = cur.fetchall()  # 使结果全部可看
    for data1 in see1:
        yvalues1.append(data1[0])
    sql = "SELECT count(1) FROM airline " \
          "WHERE start_area like '%s' and end_area like '%s' and act_date like date_add('%s', interval 1 day) " \
          "and Aprice <= 400" % (start_area, end_area, act_date)  # sql语句
    print(sql)
    cur.execute(sql)  # execute(query, args):执行单条sql语句。
    see2 = cur.fetchall()  # 使结果全部可看
    for data2 in see2:
        yvalues2.append(data2[0])

    for i in range(400,1201,200):
        sql = "SELECT count(1) FROM airline " \
              "WHERE start_area like '%s' and end_area like '%s' and act_date like '%s' " \
              "and Aprice > %d and Aprice <= %d " % (start_area, end_area, act_date, i, i+200)  # sql语句
        # print(sql)
        cur.execute(sql)  # execute(query, args):执行单条sql语句。
        see1 = cur.fetchall()  # 使结果全部可看
        for data1 in see1:
            yvalues1.append(data1[0])
        sql = "SELECT count(1) FROM airline " \
              "WHERE start_area like '%s' and end_area like '%s' and act_date like date_add('%s', interval 1 day) " \
              "and Aprice > %d and Aprice <= %d " % (start_area, end_area, act_date, i, i+200)  # sql语句
        # print(sql)
        cur.execute(sql)  # execute(query, args):执行单条sql语句。
        see2 = cur.fetchall()  # 使结果全部可看
        for data2 in see2:
            yvalues2.append(data2[0])

    sql = "SELECT count(1) FROM airline " \
          "WHERE start_area like '%s' and end_area like '%s' and act_date like '%s' " \
          "and Aprice > 1400" % (start_area, end_area, act_date)  # sql语句
    # print(sql)
    cur.execute(sql)  # execute(query, args):执行单条sql语句。
    see1 = cur.fetchall()  # 使结果全部可看
    for data1 in see1:
        yvalues1.append(data1[0])
    sql = "SELECT count(1) FROM airline " \
          "WHERE start_area like '%s' and end_area like '%s' and act_date like date_add('%s', interval 1 day) " \
          "and Aprice > 1400" % (start_area, end_area, act_date)  # sql语句
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

    conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='buggerexe')  # 建立数据库连接
    cur = conn.cursor()
    sql = "SELECT air_id, lose_rate FROM airline " \
          "WHERE start_area like '%s' and end_area like '%s' and act_date like '%s' " \
          "order by lose_rate desc limit 20" % (start_area, end_area, act_date)  # sql语句
    print(sql)
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

@app.route("/planeMap/acomd", methods=['POST'])
def air_com_data():
    data = json.loads(request.form.get('data'))
    start_area = data['start_area']
    end_area = data['end_area']
    act_date = data['act_date']
    # print(start_area, end_area, act_date)

    conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='buggerexe')  # 建立数据库连接
    cur = conn.cursor()
    sql = "SELECT air_com, count(1) as acc FROM airline " \
          "WHERE start_area like '%s' and end_area like '%s' and act_date like '%s' " \
          "group by air_com " \
          "order by acc limit 15" % (start_area, end_area, act_date)  # sql语句
    print(sql)
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

    conn = pymysql.connect(host='127.0.0.1', user='root', password='', db='buggerexe')  # 建立数据库连接
    cur = conn.cursor()
    sql = "SELECT plane_type, count(1) as acc FROM airline " \
          "WHERE start_area like '%s' and end_area like '%s' and act_date like '%s' " \
          "group by plane_type " \
          "order by acc limit 5" % (start_area, end_area, act_date)  # sql语句
    print(sql)
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
    print(sql)
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


if __name__ == '__main__':
    app.run(debug=True)  # 启用调试模式
