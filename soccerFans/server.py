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

def queryManywithData(sql, data):
    db = psycopg2.connect(database=db_name,host=host_string,port='5432',user=db_username,password=db_password,options="-c search_path=sz3029")
    cursor = db.cursor()
    cursor.execute(sql, data)
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

    if allpost is None:
        abort(404)
    else:
        # get all names of users
        sql = """
            SELECT u.name
            FROM users u, posts p
            WHERE p.uid = u.uid"""
        names = queryMany(sql)
        # get all likes
        like_list = []
        for post in allpost:
            post_id_temp = post[0]
            sql = """
                SELECT COUNT(*)
                FROM likes l, posts p
                WHERE l.post_id = p.post_id AND
                p.post_id = %s"""
            count = queryOnewithData(sql, (post_id_temp,))
            like_list.append(count)

    return render_template('postList.html', allpost=allpost, names=names, len=len(allpost), likes=like_list)

@server.route('/<int:post_id>-viewpost')
def postView(post_id):
    sql = """
            SELECT *
            FROM posts
            WHERE post_id = %s
            """
    post = queryOnewithData(sql, (post_id, ))
    if post is None:
        abort(404)
    else:
        # get author name
        sql = """
            SELECT u.name
            FROM users u, posts p
            WHERE p.post_id = %s AND u.uid = p.uid"""
        name = queryOnewithData(sql, (post_id, ))
        #get comments
        sql = """
            SELECT c.comment_id, c.content, c.com_time, u.name, c.if_anonymous
            FROM comments c, posts p, users u
            WHERE p.post_id = %s AND c.post_id = p.post_id
            AND c.uid = u.uid"""
        comments = queryManywithData(sql, (post_id,))

    return render_template('postview.html', post=post, name=name[0], comments=comments)

@server.route('/<int:uid>-myPost')
def myPost(uid, check_author=True):
    sql = """
    SELECT *
    FROM posts
    WHERE uid = %s""" % (str(uid))
    mypost = queryMany(sql)
    if mypost is None:
        abort(404)
    return render_template('myPost.html', mypost=mypost)

@server.route('/<int:uid>-createpost', methods=['GET', 'POST'])
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

@server.route('/<int:post_id>-deltepost', methods=['GET', 'POST'])
def postDelete(post_id):
    user_id = session["user_id"]
    form = forms.DeletePostForm()
    post = queryOnewithData("SELECT * FROM posts WHERE post_id = %s", (post_id, ))
    #if post exists
    if post:
        if form.validate_on_submit():
            sql = """
                    DELETE FROM comments WHERE post_id = %s AND uid = %s
                """
            execSQLwithData(sql, (post_id, user_id, ))

            sql = """
                    DELETE FROM likes WHERE post_id = %s AND uid = %s
                """
            execSQLwithData(sql, (post_id, user_id,))

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


@server.route('/<int:post_id>-editpost', methods=['GET', 'POST'])
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

@server.route('/<int:post_id>-like')
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

# createcomment
@server.route("/<int:post_id>-createcomment", methods=("GET", "POST"))
def postComment(post_id):
    """Create a new comment for posts."""
    form = forms.Commentform()
    user_id = session["user_id"]
    if form.validate_on_submit():
        comment = form.comment.data
        if_anonymous = form.anonymous.data

        sql = "INSERT INTO comments (content, post_id, uid, if_anonymous) VALUES (%s, %s, %s, %s)"
        execSQLwithData(sql, (comment, post_id, user_id, if_anonymous,))
        flash("Commented!")
        return redirect(url_for('postView', post_id=post_id))

    return render_template('comments.html', form = form, user_id = user_id, post_id = post_id)

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

@server.route('/qa')
def QA():
    sql = """
            SELECT title, content
            FROM raise_questions"""
    allqa = queryMany(sql)

    if allqa is None:
        abort(404)
    else:
        return render_template('qa.html', allqa=allqa)

@server.route('/qa-create', methods=['GET', 'POST'])
def createQA():
    """Create a new post for the current user."""
    user_id = session["user_id"]
    form = forms.qaform()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        # serial not working...
        max_question_id = queryOne('SELECT max(question_id) max_question_id From raise_questions')[0]
        question_id = max_question_id + 1
        sql = """
        INSERT INTO raise_questions (question_id, uid, title, content) VALUES (%s, %s, %s, %s);"""
        data = (question_id, user_id, title, content, )
        execSQLwithData(sql, data)

        flash('Question Submitted!')
        return redirect(url_for("QA"))

    return render_template('qa_create.html', form=form, user_id=user_id)

@server.route('/events')
def eventList():
    user_id = session['user_id']
    sql = """
            SELECT *
            FROM create_events"""
    allevents = queryMany(sql)

    if allevents is None:
        abort(404)
    else:
        # get all names of users
        sql = """
                SELECT u.name
                FROM users u, create_events e
                WHERE e.host_id = u.uid"""
        names = queryMany(sql)
        # get all joined events
        sql = """
        SELECT c.*, u.name
        FROM join_events j, create_events c, users u
        WHERE j.uid = %s AND j.event_id = c.event_id AND c.host_id = u.uid"""
        myjoined = queryManywithData(sql, (user_id,))

    return render_template('eventList.html', allevents=allevents, names=names,
                           len=len(allevents), len_1=len(myjoined), myjoined=myjoined)

@server.route('/<int:uid>-eventsManagement')
def eventsManagement(uid):
    sql = """
    SELECT *
    FROM create_events
    WHERE host_id = %s""" % (str(uid))
    myevents = queryMany(sql)
    if myevents is None:
        abort(404)
    return render_template('eventsManagement.html', myevents=myevents)


@server.route('/<int:uid>-createevent', methods=['POST', 'GET'])
def eventCreate(uid):
    """Create anew post for the current user."""
    if request.method == 'POST':
        sql = """INSERT INTO create_events(host_id,event_name,description,place,regist_fee,start_time, end_time, max_capacity) VALUES 
                ('%s','%s','%s','%s','%s','%s','%s','%s')""" % (uid, request.form['event_name'], request.form['description'],
                request.form['place'],request.form['regist_fee'],request.form['start_time'],
                request.form['end_time'],request.form['max_capacity'],)
        execSQL(sql)
        flash('Event Created!')
        return redirect(url_for("eventsManagement", uid=uid))

    return render_template('eventcreate.html', uid=uid)


@server.route('/<int:event_id>-deleteevent', methods=['GET', 'POST'])
def eventDelete(event_id):
    user_id = session["user_id"]
    form = forms.DeleteEventForm()
    event = queryOnewithData("SELECT * FROM create_events WHERE event_id = %s", (event_id, ))
    #if event exists
    if event:
        if form.validate_on_submit():
            sql = """
                DELETE FROM join_events WHERE event_id = %s
                            """
            execSQLwithData(sql, (event_id, ))

            sql = """
                    DELETE FROM create_events WHERE event_id = %s AND host_id = %s
                """
            execSQLwithData(sql, (event_id, user_id, ))

            flash("Deleted your events and all joins!")
            return redirect(url_for("eventsManagement", uid=user_id))
        title = event[2]
        return render_template('eventdelete.html', form=form, event_id=event_id, title=title)
    else:
        flash("Event not Found!")
    return redirect(url_for("eventsManagement", uid=user_id))


@server.route('/<int:event_id>-joinevent', methods=['GET', 'POST'])
def eventJoin(event_id):
    user_id = session["user_id"]
    event = queryOnewithData("SELECT * FROM create_events WHERE event_id = %s", (event_id, ))
    #if event exists
    if event:
        sql = """
        INSERT INTO join_events(uid, event_id) VALUES ('%s', '%s')
        """
        execSQLwithData(sql, (user_id, event_id, ))

        flash("Joined Event!")
        return redirect(url_for("eventList"))
    else:
        flash("Event not Found!")
    return redirect(url_for("eventList"))

@server.route('/<int:event_id>-disjoinevent', methods=['GET', 'POST'])
def eventDisjoint(event_id):
    user_id = session["user_id"]
    event = queryOnewithData("SELECT * FROM join_events WHERE event_id = %s AND uid = %s", (event_id, user_id,))
    #if event exists
    if event:
        sql = """
        DELETE FROM join_events WHERE event_id = %s AND uid = %s
        """
        execSQLwithData(sql, (event_id, user_id, ))
        flash("Dis-joined Event!")
        return redirect(url_for("eventList"))
    else:
        flash("Event not Found!")
    return redirect(url_for("eventList"))

@server.route('/checkFansLogin',  methods=['POST'])
def checkFansLogin():
    sql = "select * from users where email = '%s' and password = '%s'" %(request.form['username'],request.form['password'])
    result = queryOne(sql)
    if result is None:
        return "<script>alert('Wrong Account name or password!');window.location='fansLogin';</script>";
    else:
        session['user_id'] = result[0]
        session['name'] = result[2]
        # add user type
        session['user_type'] = result[-1]

        return "<script>alert('Logged In!');window.location='/';</script>";

@server.route('/reg')
def reg():
    return render_template('register.html')

@server.route('/fansReg',methods=['POST'])
def fansReg():
    sql = "INSERT INTO users(email,name,password,date_of_birth,gender,nation,user_type) VALUES ('%s','%s','%s','%s','%s','%s','host')" %(request.form['username']
            ,request.form['name'],request.form['password'],request.form['birthday'],request.form['gender'],request.form['nation'])
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

# account info
@server.route('/<int:uid>-user')
def user(uid):
    sql = "select * from v_users where uid = '%s'"
    result = queryOnewithData(sql, (uid,))
    if result is None:
        return "<script>alert('Account Info Extract Failed!');window.location='fansLogin';</script>";
    else:
        return render_template('account.html', user=result)


# <<<<<<< HEAD
# # if __name__ == '__main__':
# #     server.run()

if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    print("running on %s:%d" % (HOST, PORT))
    server.run(host=HOST, port=PORT, debug=True, threaded=True)
  run()
# =======
# if __name__ == '__main__':
#     server.run(debug=True, threaded=True)
# >>>>>>> bbd4337b717eeccac4386255a5ae1e7bf564b9ca
