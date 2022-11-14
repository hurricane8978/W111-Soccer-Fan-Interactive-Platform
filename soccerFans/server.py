#-*- coding: utf-8 -*-

from flask import Flask,render_template,request,redirect
from flask import url_for,make_response,session,send_from_directory

import uuid
import json
import traceback
import time,psycopg2

server = Flask("an interactive platform for soccer fans or potential fans",static_url_path='',static_folder="static",template_folder="templates")
server.secret_key = "12311"
host_string = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"
db_username = "sz3029"
db_password = "dbuserdbuser"
db_name = "proj1part2"

# config for forms
server.config["SECRET_KEY"] = "ABC"

def queryOne(sql):
    db = psycopg2.connect(database=db_name,host=host_string,port='5432',user=db_username,password=db_password,options="-c search_path=sz3029")
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result

def queryMany(sql):
    db = psycopg2.connect(host='localhost',port='5432',user='root',password='123456')
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    db.close()
    return results

def execSQL(sql):
    db = psycopg2.connect(database=db_name,host=host_string,port='5432',user=db_username,password=db_password,options="-c search_path=sz3029")
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()

@server.route('/fansLogin')
def fansLogin():
    #results = queryMany(sql)
    # follows = []
    # for r in results:
        # follow = {}
        # follow['user_id'] = r[0]
        # follow['name'] = r[1]
        # follows.append(follow)
    return render_template('fansLogin.html')

@server.route('/hostLogin')
def hostLogin():
    #results = queryMany(sql)
    # follows = []
    # for r in results:
        # follow = {}
        # follow['user_id'] = r[0]
        # follow['name'] = r[1]
        # follows.append(follow)
    return render_template('hostLogin.html')

@server.route('/eventView')
def eventView():
    #results = queryMany(sql)
    # follows = []
    # for r in results:
        # follow = {}
        # follow['user_id'] = r[0]
        # follow['name'] = r[1]
        # follows.append(follow)
    return render_template('eventView.html')

@server.route('/postList')
def postList():
    #results = queryMany(sql)
    # follows = []
    # for r in results:
        # follow = {}
        # follow['user_id'] = r[0]
        # follow['name'] = r[1]
        # follows.append(follow)
    return render_template('postList.html')

@server.route('/myPost')
def myPost():
    #results = queryMany(sql)
    # follows = []
    # for r in results:
        # follow = {}
        # follow['user_id'] = r[0]
        # follow['name'] = r[1]
        # follows.append(follow)
    return render_template('myPost.html')

@server.route('/follows')
def follows():
    #sql = "select * from follow where user_id = %s" % (str(session.get(user_id)))
    #results = queryMany(sql)
    # follows = []
    # for r in results:
        # follow = {}
        # follow['user_id'] = r[0]
        # follow['name'] = r[1]
        # follows.append(follow)
    return render_template('follows.html')

@server.route('/vote')
def vote():

    #exist_sql = "select count(*) from vote where user_id = %s" % (str(session.get(user_id)))
    #result = queryOne(exist_sql)
    return render_template('vote.html')

@server.route('/aboutUs')
def aboutUs():
    return render_template('aboutUs.html')

@server.route('/events')
def events():
    #results = queryMany(sql)
    # follows = []
    # for r in results:
        # follow = {}
        # follow['user_id'] = r[0]
        # follow['name'] = r[1]
        # follows.append(follow)
    return render_template('events.html')

@server.route('/comments')
def comments():
    #results = queryMany(sql)
    # follows = []
    # for r in results:
        # follow = {}
        # follow['user_id'] = r[0]
        # follow['name'] = r[1]
        # follows.append(follow)
    return render_template('comments.html')

@server.route('/eventList')
def eventList():
    #results = queryMany(sql)
    # follows = []
    # for r in results:
        # follow = {}
        # follow['user_id'] = r[0]
        # follow['name'] = r[1]
        # follows.append(follow)
    return render_template('eventList.html')

@server.route('/eventsManagement')
def eventsManagement():
    #results = queryMany(sql)
    # follows = []
    # for r in results:
        # follow = {}
        # follow['user_id'] = r[0]
        # follow['name'] = r[1]
        # follows.append(follow)
    return render_template('eventsManagement.html')

@server.route('/checkFansLogin',  methods=['POST'])
def checkFansLogin():
    sql = "select * from users where email = '%s' and password = '%s'" %(request.form['username'],request.form['password'])
    result = queryOne(sql)
    if result is None:
        return "<script>alert('账号密码有误!');window.location='fansLogin';</script>";
    else:
        session['user_id'] = result[0]
        session['name'] = result[2]

        return "<script>alert('登陆成功!');window.location='/';</script>";

@server.route('/reg')
def reg():
    return render_template('register.html')

@server.route('/fansReg',methods=['POST'])
def fansReg():
    sql = "INSERT INTO users(email,name,password,date_of_birth,gender,nation,user_type) VALUES ('%s','%s','%s','%s','%s','%s','host')" %(request.form['username']
            ,request.form['name'],request.form['password'],request.form['birthday'],request.form['gender'],request.form['nation'])
    print(sql)
    execSQL(sql)
    return "<script>alert('register successfully!');window.location='fansLogin';</script>";


@server.route('/')
def indexPage():
    if session.get('user_id') is None:
        session['user_id'] = 0
    return render_template('home.html')

@server.route('/quit')
def quit():
    session.clear
    session['user_id'] = 0
    return render_template('quit.html')

@server.route('/user')
def user():
    #results = queryMany(sql)
    # follows = []
    # for r in results:
        # follow = {}
        # follow['user_id'] = r[0]
        # follow['name'] = r[1]
        # follows.append(follow)
    return render_template('home.html')


if __name__ == '__main__':
    server.run(debug=True, threaded=True)
