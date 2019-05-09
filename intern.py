from random import randint
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import sha256_crypt
import datetime
import MySQLdb
from flask import Flask, redirect, url_for, render_template, request, json

app = Flask(__name__)

db = MySQLdb.connect(host="localhost",  # your host
                     user="root",  # username
                     passwd="root",  # password
                     db="pvg")  # name of the database


@app.route('/', methods=['GET', 'POST'])
def try1():
    cur = db.cursor()
    cur.execute("select name from user")
    data = cur.fetchall()
    count = 0
    user = {'M_course': []}

    for row in data:
        user['M_course'].append(row[0])
        count=count+1

    return render_template("try.html", user=user, count=count)

x=0

@app.route('/us-<b>', methods=['GET', 'POST'])
def us(b):
    cur = db.cursor()
    cur.execute(" SELECT * from user where Name='" + b + " '")
    data = cur.fetchone()

    u1 = {'nm':b, 'em':data[1], 'credit':data[2]}

    print(type(b))

    global x

    x=b

    return render_template("1.html",u1=u1)

@app.route('/transfer-<a>',methods=['GET', 'POST'])
def transfer(a):

    cur = db.cursor()
    cur.execute(" SELECT * from user where Name !='" + a + " '")
    data = cur.fetchall()
    count = 0
    user1 = {'fname': [], 'mail':[],'credit': []}

    for row in data:

        user1['fname'].append(row[0])
        user1['mail'].append(row[1])
        user1['credit'].append(row[2])
        count = count + 1


    return render_template("transfer.html",user1=user1,count=count)


@app.route('/put')
def put():

    return render_template("thanks.html")

@app.route('/tr-<a>',methods=['GET','POST'])
def tr(a):

    if request.method == 'POST':
        amt = request.form['am']
        print(amt)
        amt1 = int(amt)

        cur = db.cursor()
        cur.execute("select * from user where Name='" + a + "'")
        data = cur.fetchone()

        t = data[2]

        total = t+ amt1
        print(total)


        tt = str(total)
        cur1 = db.cursor()
        cur1.execute("update user set currentCredit='"+ tt +"' where Name='"+a+"'")
        db.commit()

        print(type(x))
        print(x)

        cur3 = db.cursor()
        cur3.execute("select * from user where Name='" + x + "'")
        data = cur3.fetchone()

        t2 = data[2]

        tf = t2 - amt1

        print(tf)

        tff=str(tf)


        cur2 = db.cursor()
        cur2.execute("update user set currentCredit='"+ tff +"' where Name='"+x+"'")
        db.commit()

        date = datetime.date.today()
        cur4 = db.cursor()
        query = "insert into transfers(Sender,Receive,Amount,Date) VALUES(%s,%s,%s,%s)"
        cur4.execute(query, (x, a, amt1, date))
        db.commit()

        return render_template("thanks.html")

    return render_template("amount.html")

if __name__ == '__main__':
    app.run(debug=True)
