import os

import pymysql as pymysql
from flask import *
from werkzeug.utils import secure_filename

task = Flask(__name__)
task.secret_key = "abc"
con = pymysql.connect(host="localhost", user="root", password="root", port=3306, db="taskproject", charset="utf8")
cmd = con.cursor()
import functools
def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if "logid" not in session:
            return redirect("/")
        return func()
    return secure_function

@task.route('/')
def login():
    return render_template('LOGIN1.html')


@task.route('/signup')
def signup():
    return render_template('REGI.html')


@task.route('/insert', methods=['post'])
def insert():
    name = request.form['textfield']
    age = request.form['textfield2']
    ph = request.form['textfield3']
    add = request.form['textarea']
    email = request.form['textfield4']
    gender = request.form['gender']
    qual = request.form.getlist('qualification')
    qualif = ','.join(qual)
    lan = request.form['select']
    psd = request.form['textfield5']
    photo = request.files['fileField']
    pho = secure_filename(photo.filename)
    photo.save(os.path.join("static/phot", pho))

    cmd.execute("insert into `tasklogin` values(null,'" + email + "','" + psd + "')")
    rid = cmd.lastrowid
    con.commit()
    cmd.execute("insert into `taskregister` values(null,'" + name + "','" + age + "','" + ph + "','" + add + "','" + gender + "','" + qualif + "','" + email + "','" + lan + "','" + str(rid) + "','" + pho + "')")
    con.commit()
    return '''<script>alert("successfully registered");window.location='/'</script>'''


@task.route('/logincheck', methods=['post'])
def logincheck():
    user = request.form['textfield']
    psd = request.form['textfield2']
    cmd.execute("select * from tasklogin where username='" + user + "' and password='" + psd + "'")
    result = cmd.fetchone()
    if result is None:
        return '''<script>alert("INVALID USERNAME AND PASSWORD");window.location='/'</script>'''
    else:
        session['logid']=result[0]
        return render_template("VIEWALL.html")


@task.route('/viewdetails')
@login_required
def viewdetails():
    cmd.execute("select * from taskregister")
    result = cmd.fetchall()
    return render_template("TABLEREGISTER.html", val=result)


@task.route('/delete')
@login_required
def delete():
    id = request.args.get("id")
    cmd.execute("delete from taskregister where id='" + id + "'")
    con.commit()
    return '''<script>alert("Succefully deleted");window.location='/viewdetails'</script>'''


@task.route('/edit')
@login_required
def edit():
    id = request.args.get("id")
    session['aid'] = id
    cmd.execute("select * from taskregister where id='" + id + "'")
    result = cmd.fetchone()
    return render_template("updation.html", val=result)


@task.route('/update',methods=['post'])
@login_required
def update():
    uid = session['aid']
    name = request.form['textfield']
    age = request.form['textfield2']
    ph = request.form['textfield3']
    add = request.form['textarea']
    em = request.form['textfield5']
    gen = request.form['GENDER']
    qual = request.form.getlist('qualification')
    qualif = ','.join(qual)
    lan = request.form['select']
    cmd.execute("update taskregister set name='" + name + "',age='" + age + "',phone_number= '" + ph + "',address='" + add + "',email='" + em + "',gender='" + gen + "',qualification='" + qualif + "',language='" + lan + "' where id='" + uid + "'")
    con.commit()
    return '''<script>alert("successfully updated");window.location='/viewdetails'</script>'''


@task.route('/changeimage')
@login_required
def changeimage():
    return render_template("change.html")


@task.route('/upimage', methods=['post'])
@login_required
def upimage():
    photo = request.files['fileField']
    pho = secure_filename(photo.filename)
    photo.save(os.path.join("static/phot",  pho))
    ide = session['aid']
    cmd.execute("update taskregister set photo='" + pho + "' where id='" + ide + "'")
    con.commit()
    return '''<script>alert("Image updated successfully");window.location='/viewdetails'</script>'''
@task.route('/viewprofile')
@login_required
def viewprofile():
    loginid=session['logid']
    cmd.execute("select * from taskregister where login_id='"+str(loginid)+"'")
    result=cmd.fetchone()
    return render_template("VIEWPROFILE.html",value=result)
@task.route('/profileupdate',methods=['post'])
@login_required
def profileupdate():
    loginid = session['logid']
    name = request.form['textfield']
    age = request.form['textfield2']
    ph = request.form['textfield3']
    add = request.form['textarea']
    em = request.form['textfield4']
    gen = request.form['gender']
    qual = request.form.getlist('qualification')
    qualif = ','.join(qual)
    lan = request.form['select']
    cmd.execute("update taskregister set name='" + name + "',age='" + age + "',phone_number= '" + ph + "',address='" + add + "',email='" + em + "',gender='" + gen + "',qualification='" + qualif + "',language='" + lan + "' where login_id='" +str(loginid)+ "'")
    con.commit()
    return '''<script>alert("successfully updated");window.location='/homepage'</script>'''

@task.route('/changeimg')
@login_required
def changeimg():
    return render_template("CHANGEPI.html")

@task.route('/uppropic',methods=['post'])
@login_required
def uppropic():
    photo = request.files['fileField']
    pho = secure_filename(photo.filename)
    photo.save(os.path.join("static/phot",  pho))
    loginid = session['logid']
    cmd.execute("update taskregister set photo='" + pho + "' where login_id='" +str(loginid)+ "'")
    con.commit()
    return '''<script>alert("Image updated successfully");window.location='/homepage'</script>'''
@task.route('/homepage')
@login_required
def homepage():
    return render_template("HOMEPAGE.html")
@task.route('/logout')
def logout():
    session.clear()
    return redirect('/')



task.run(debug=True)