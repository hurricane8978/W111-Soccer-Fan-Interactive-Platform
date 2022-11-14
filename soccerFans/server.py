#-*- coding: utf-8 -*-

from flask import Flask,render_template,request,redirect, abort, flash
from flask import url_for,make_response,session,send_from_directory

import uuid
import json
import traceback
import time,psycopg2
import forms
from datetime import datetime

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

def queryOnewithData(sql, data):
    db = psycopg2.connect(database=db_name,host=host_string,port='5432',user=db_username,password=db_password,options="-c search_path=sz3029")
    cursor = db.cursor()
    cursor.execute(sql, data)
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result

def queryMany(sql):
    db = psycopg2.connect(database=db_name,host=host_string,port='5432',user=db_username,password=db_password,options="-c search_path=sz3029")
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

## query with data input
def execSQLwithData(sql, data):
    db = psycopg2.connect(database=db_name,host=host_string,port='5432',user=db_username,password=db_password,options="-c search_path=sz3029")
    cursor = db.cursor()
    cursor.execute(sql, data)
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
    sql = """
        SELECT *
        FROM posts"""
    allpost = queryMany(sql)
    # get all names of users
    sql = """
    SELECT u.name
    FROM users u, posts p
    WHERE p.uid = u.uid"""
    names = queryMany(sql)
    if allpost is None:
        abort(404)
    return render_template('postList.html', allpost=allpost, names=names, len=len(allpost))

@server.route('/<int:post_id>/viewpost')
def postView(post_id):
    sql = """
            SELECT *
            FROM posts
            WHERE post_id = %s
            """
    post = queryOnewithData(sql, (post_id, ))
    # get author name
    sql = """
       SELECT u.name
       FROM users u, posts p
       WHERE p.post_id = %s AND u.uid = p.uid"""
    name = queryOnewithData(sql, (post_id, ))

    return render_template('postview.html', post=post, name=name[0])

@server.route('/<int:uid>/myPost')
def myPost(uid, check_author=True):
    sql = """
    SELECT *
    FROM posts
    WHERE uid = %s""" % (str(uid))
    mypost = queryMany(sql)
    if mypost is None:
        abort(404)
    return render_template('myPost.html', mypost=mypost)

@server.route('/<int:uid>/createpost', methods=['GET', 'POST'])
def postCreate(uid, check_author=True):
    """Create a new post for the current user."""
    user_id = session["user_id"]
    form = forms.Postform()

    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        time = datetime.utcnow()

        # serial not working...
        max_post_id = queryOne('SELECT max(post_id) max_post_id From posts')[0]
        post_id = max_post_id + 1
        sql = """INSERT INTO posts (post_id, title, content, post_time, uid) VALUES 
                 (%s,%s, %s, %s, %s);"""
        data = (post_id, title, post, time, user_id, )
        execSQLwithData(sql, data)
        flash('Post Submitted!')
        return redirect(url_for("myPost", uid=user_id))

    return render_template('postcreate.html', form=form, user_id=user_id)

@server.route('/<int:post_id>/deltepost', methods=['GET', 'POST'])
def postDelete(post_id):
    user_id = session["user_id"]
    form = forms.DeletePostForm()
    post = queryOnewithData("SELECT * FROM posts WHERE post_id = %s", (post_id, ))
    #if post exists
    if post:
        if form.validate_on_submit():
            #sql = """
                    #DELETE FROM comment WHERE post_id = %s AND uid = %s
                #"""
            #execSQLwithData(sql, (post_id, user_id, ))

            #sql = """
                    #DELETE FROM liked WHERE post_id = %s AND user_id = %s
                #"""
            #execSQLwithData(sql, (post_id, user_id,))


            sql = """
                    DELETE FROM posts WHERE post_id = %s AND uid = %s
                """
            execSQLwithData(sql, (post_id, user_id, ))

            flash("Deleted your post and all comments!")
            return redirect(url_for("myPost", uid=user_id))

        return render_template('postdelete.html', form=form, post_id=post_id)
    else:
        flash("Post not Found!")
    return redirect(url_for("myPost", uid=user_id))


@server.route('/<int:post_id>/editpost', methods=['GET', 'POST'])
def postEdit(post_id, check_author=True):
    user_id = session["user_id"]
    """Update a post if the current user is the author."""
    sql = """
            SELECT *
            FROM posts
            WHERE post_id = %s AND uid = %s
            """
    post = queryOnewithData(sql, (post_id, user_id, ))

    form = forms.Postform(
        title=post[3],
        post=post[4])

    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        time = datetime.utcnow()
        # update sql
        sql = """
        
                UPDATE posts
                SET title = %s, content = %s, post_time = %s
                WHERE post_id = %s
            """
        execSQLwithData(sql, (title, post, time, post_id,))
        flash("updated your post!")
        return redirect(url_for('postList'))

    return render_template('postedit.html', post_id=post_id, form=form)

@server.route('/<int:post_id>/like')
def like(post_id):
    user_id = session["user_id"]
    sql = """
                SELECT *
                FROM posts
                WHERE post_id = %s
                """
    post = queryOnewithData(sql, (post_id, ))
    if post:
        # serial not working...
        max_like_id = queryOne('SELECT max(like_id) max_like_id From likes')[0]
        like_id = max_like_id + 1
        time = datetime.utcnow()
        sql = """INSERT INTO likes (like_id, like_time, post_id, uid) VALUES 
                (%s, %s, %s, %s)"""
        execSQLwithData(sql, (like_id, time, post_id, user_id,))
        flash("Liked!")
    else:
        flash("Post not found!")

    return redirect(url_for('postList'))

@server.route('/<int:post_id>/comment')
def comment():
    #sql = "select * from follow where user_id = %s" % (str(session.get(user_id)))
    #results = queryMany(sql)
    # follows = []
    # for r in results:
        # follow = {}
        # follow['user_id'] = r[0]
        # follow['name'] = r[1]
        # follows.append(follow)
    return render_template('comments.html')

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
    session.clear()
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
