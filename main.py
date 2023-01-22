from flask import Flask, render_template,request,session,redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pandas
from datetime import date

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q57738z\n\xec]/'

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='1234'
app.config['MYSQL_DB']='feedback'

mysql=MySQL(app)

@app.route('/')
def index():
    return render_template('base.html')
    
@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/adminLogin', methods=['GET','POST'])
def adminLogin():
    msg = ''
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['pwd']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE name = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['name']
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM hod')
            results = cur.fetchall()
            return render_template('adminHome.html', msg = results)
        else: 
            msg = 'Incorrect username / password !'
            return render_template('error.html', data = msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/addHod')
def addHod():
    
    return render_template('addHod.html')

@app.route('/addHodDb', methods=['GET','POST'])
def addHodDb():

    if request.method == 'POST':
        hod_id = request.form['id']
        name = request.form['name']
        Dept = request.form['dept']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT id FROM hod WHERE id = % s', (hod_id, ))
        account = cursor.fetchone()
        if account:
            msg = 'use different id...  This id already exist...'
            return render_template('error.html', data = msg)
        else:
            cursor.execute('INSERT INTO hod VALUES (%s,%s,%s)',(hod_id,name,Dept))
            mysql.connection.commit()
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM hod')
            results = cur.fetchall()
            return render_template('adminHome.html', msg = results)
        

@app.route('/adminHome')
def adminHome():

    return render_template('adminHome.html')

@app.route('/removeHod')
def removeHod():

    return render_template('removeHod.html')

@app.route('/removeHodDb', methods=['GET','POST'])
def removeHodDb():

    if request.method == 'POST':
        hod_id = request.form['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM hod WHERE id = % s', (hod_id, ))
        account = cursor.fetchone()
        if account:
            cursor.execute('DELETE FROM hod WHERE id = %s', (hod_id,))
            mysql.connection.commit()
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM hod')
            results = cur.fetchall()
            return render_template('adminHome.html', msg = results)
        else:
            msg = 'use different id...  This id does not exist...'
            return render_template('error.html', data = msg)

@app.route('/hod')
def hod():
    return render_template('hod.html')

@app.route('/hodLogin', methods=['GET','POST'])
def hodLogin():
    msg = ''
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['pwd']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM hod WHERE name = % s AND id = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['name']
            cur = mysql.connection.cursor()
            cur.execute('SELECT id,name,role,dept FROM staffs WHERE dept=%s ',[account['dept']] )
            result = cur.fetchall()
            results = [result,account]
            return render_template('hodHome.html', msg = results)
        else:
            msg = 'Incorrect username / password !'
            return render_template('error.html', data = msg)

@app.route('/addStaff')
def addStaff():

    return render_template('addStaff.html')

@app.route('/addStaffDb', methods = ['GET', 'POST'])
def addStaffDb():

    if request.method == 'POST':
        staff_id = request.form['id']
        name = request.form['name']
        Dept = request.form['dept']
        role = request.form['role']
        file = request.files['pic']
        file.save("static/upload/" + file.filename)
        ImageURL="static/upload/" + file.filename
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT id FROM staffs WHERE id = %s', (staff_id, ))
        account = cursor.fetchone()
        if account:
            msg = 'use different id...  This id already exist...'
            return render_template('error.html', data = msg)
        else:
            cursor.execute('INSERT INTO staffs VALUES (%s,%s,%s,%s,%s)',(staff_id,name,Dept,role,ImageURL))
            mysql.connection.commit()
            cur = mysql.connection.cursor()
            cur.execute('SELECT  id,name,role,dept FROM staffs WHERE dept=%s',[Dept])
            results = cur.fetchall()
            return render_template('hodhm.html', msg = results)


@app.route('/removeStaff')
def removeStaff():

    return render_template('removeStaff.html')

@app.route('/removeStaffDb', methods=['GET','POST'])
def removeStaffDb():

    if request.method == 'POST':
        staff_id = request.form['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM staffs WHERE id = % s', (staff_id, ))
        account = cursor.fetchone()
        if account:
            cursor.execute('DELETE FROM staffs WHERE id = %s', (staff_id,))
            mysql.connection.commit()
            cur = mysql.connection.cursor()
            cur.execute('SELECT  id,name,role,dept FROM staffs WHERE dept=%s',[account['dept']])
            results = cur.fetchall()
            return render_template('hodhm.html', msg = results)
        else:
            msg = 'use different id...  This id does not exist...'
            return render_template('error.html', data = msg)


@app.route('/staff')
def staff():

    return render_template('staff.html')

@app.route('/staffLogin', methods=['GET','POST'])
def staffLogin():
    
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['pwd']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM staffs WHERE name = % s AND id = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['name']
            dept = account['dept']
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM student WHERE dept=%s',[dept])
            result = cur.fetchall()
            results = [result,account]
            return render_template('staffHome.html', msg = results)
        else:
            msg = 'Incorrect username / password !'
            return render_template('error.html', data = msg)

@app.route('/addStudent')
def addStudent():

    return render_template('addStudent.html')

@app.route('/addStudentDb', methods = ['GET', 'POST'])
def addStudentDb():

    if request.method == 'POST':
        student_id = request.form['id']
        name = request.form['name']
        year = request.form['year']
        dept = request.form['dept']
        section = request.form['sec']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT id FROM student WHERE id = % s', (student_id, ))
        account = cursor.fetchone()
        if account:
            msg = 'use different id...  This id already exist...'
            return render_template('error.html', data = msg)
        else:
            cursor.execute('INSERT INTO student VALUES (%s,%s,%s,%s,%s)',(student_id,name,year,dept,section))
            mysql.connection.commit()
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM student WHERE dept=%s',[dept])
            results = cur.fetchall()
            return render_template('staffhm.html', msg = results)


@app.route('/removeStudent')
def removeStudent():

    return render_template('removeStudent.html')

@app.route('/removeStudentDb', methods=['GET','POST'])
def removeStudentDb():

    if request.method == 'POST':
        student_id = request.form['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE id = % s', (student_id, ))
        account = cursor.fetchone()
        if account:
            dept = account['dept']
            cursor.execute('DELETE FROM student WHERE id = %s', (student_id,))
            mysql.connection.commit()
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM student WHERE dept=%s',[dept])
            results = cur.fetchall()
            return render_template('staffhm.html', msg = results)
        else:
            msg = 'use different id...  This id does not exist...'
            return render_template('error.html', data = msg)


@app.route('/student')
def student():

    return render_template('student.html')

@app.route('/srudentHome')
def studentHome():

    return render_template('studentHome.html')

@app.route('/studentLogin', methods=['GET','POST'])
def studentLogin():
    msg = ''
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['pwd']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE name = % s AND id = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['name']
            dept = account['dept']
            cur = mysql.connection.cursor()
            cur.execute('SELECT * FROM staffs WHERE dept=%s',[dept])
            results = cur.fetchall()
            
            return render_template('studentHome.html',msg=results)
        else:
            msg = 'Incorrect username / password !'
            return render_template('error.html', data = msg)

@app.route('/feedback/<name>/<dept>')
def feedback(name,dept):
    data = [name , dept]
    return render_template('feedback.html',msg = data)

@app.route('/feedbackDb/<name>/<dept>',methods=['GET','POST'])
def feedbackDb(name,dept):

    if request.method == 'POST':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT img FROM staffs WHERE name=%s AND dept=%s',(name,dept))
        image = cursor.fetchone()
        today = date.today()
        d4 = today.strftime("%b-%d-%Y")
        sub=request.form['sub']
        r1=request.form['rating1']
        r2=request.form['rating2']
        r3=request.form['rating3']
        r4=request.form['rating4']
        r5=request.form['rating5']
        cmnt=request.form['cmnt']
        cursor.execute('INSERT INTO feedbackTb (date,name,image,dept,subject,rating1,rating2,rating3,rating4,rating5,comment) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(d4,name,image["img"],dept,sub,r1,r2,r3,r4,r5,cmnt))
        mysql.connection.commit()
        msg="Your Feedback was submitted successfully"
        return render_template('error.html', data = msg)

@app.route('/staffFeedback/<string:name>/<string:dept>')
def staffFeedback(name,dept):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM feedbackTb WHERE name=%s AND dept=%s',(name,dept))
    data = cursor.fetchall()
    data = list(data)
    return render_template('post.html', msg=data)


@app.route('/post')
def post():

    return render_template('post.html')

@app.route('/fullPost/<id>')
def fullPost(id):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM feedbackTb WHERE id=%s',(id))
    data = cursor.fetchall()
    data = list(data)
    return render_template('fullPost.html', msg=data)


@app.route('/hodFeedback/<string:dept>')
def hodFeedback(dept):

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM feedbackTb WHERE dept=%s',[dept])
    data = cursor.fetchall()
    data = list(data)
    return render_template('post.html', msg=data)

@app.route('/adminFeedback')
def adminFeedback():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM feedbackTb')
    data = cursor.fetchall()
    data = list(data)
    return render_template('post.html', msg=data)
    
if __name__ == "__main__":
    app.run(debug=True)