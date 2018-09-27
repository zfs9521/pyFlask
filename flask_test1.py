from flask import Flask,request,redirect
from flask.templating import render_template
from flask_test import sqlRW
from flask_test import smtpF
import MySQLdb
import pymysql
import time
import json
app=Flask(__name__)
smtpFlag=True
@app.route("/data")
def getData():
    global smtpFlag
    times=time.time()
    sqlRW.writeSQL(times)
    time.sleep(1)
    contents=sqlRW.readSQL(times)
#     if int(contents['cpu'][1])>60 and smtpFlag:
#         smtpF.mail()
#         smtpFlag=False
    jsD=json.dumps(contents)
#     print(jsD)
    return jsD
@app.route("/bar")
def getBar():
    return render_template("bar.html")
@app.route("/cpu")
def getCpu():
    return render_template("cpu.html")
@app.route("/mem")
def getMem():
    times=time.time()
    sqlRW.writeSQL(times)
    time.sleep(1)
    contents=sqlRW.readSQL(times)
    return render_template("mem.html",**contents)
@app.route("/users")
def getUsers():
    times=time.time()
    sqlRW.writeSQL(times)
    time.sleep(1)
    contents=sqlRW.readSQL(times)
    return render_template("users.html",**contents)
@app.route("/net")
def getNet():
    times=time.time()
    sqlRW.writeSQL(times)
    time.sleep(1)
    contents=sqlRW.readSQL(times)
    return render_template("net.html",**contents)
@app.route("/parti")
def getParti():
    times=time.time()
    sqlRW.writeSQL(times)
    time.sleep(1)
    contents=sqlRW.readSQL(times)
    return render_template("parti.html")
@app.route("/process")
def getProcess():
    times=time.time()
    sqlRW.writeSQL(times)
    time.sleep(1)
    contents=sqlRW.readSQL(times)
    return render_template("process.html",**contents)


@app.template_filter("strs")
def strss(st):
    return st.split('/')[-1]

@app.route("/")
def index():
    return render_template("/common/index.html")
# 
@app.route("/regis",methods=['GET'])
def regis():
    return render_template("/common/regis.html",mess="请输入注册信息！！")
 
@app.route("/regis",methods=['POST'])
def regisSucc():
    veri=request.form['VeriText']
    print(veri)
    if veri=='error':
        return render_template("/common/regis.html",mess="验证码不正确！！")
    email=request.form['email']
    username=request.form['username']
    password=request.form['password']
    db=MySQLdb.connect("127.0.0.1","root","","psutils",charset="utf8")
    cursor=db.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE email = '%s' "%email)
        lis=cursor.fetchall()
        print(lis)
    except:
        print("select error")
        lis=[]
    if len(lis)!=0:
        db.close()
        return render_template("/common/regis.html",mess="邮箱已经被使用，请重新输入！")
    try:
        initSig="小哥哥小姐姐没有签名。"
        dat=time.localtime()
        dateT=time.strftime("%Y-%m-%d %X",dat)
#         tiSt="1970-"
        cursor.execute("INSERT INTO users(email,username,password,signature,regisTime,loginTime) VALUES ('%s','%s','%s','%s','%s','%s')"%(email,username,password,initSig,dateT,dateT))
        db.commit()
    except:
        print("insert error")
        db.rollback()
    db.close()
    return redirect('/login')
 
@app.route("/login",methods=['GET'])
def login():
    return render_template("/common/login.html",mess="请输入邮箱和密码！")
 
@app.route("/login",methods=['POST'])
def loginTest():
    email=request.form['email']
    password=request.form['password']
    db=MySQLdb.connect("127.0.0.1","root","","psutils",charset="utf8")
    cursor=db.cursor()
    cursor.execute("SELECT * FROM users WHERE email ='%s' and password = '%s'"%(email,password))
    lis=cursor.fetchall()
    if len(lis)==0:
        return render_template("/common/login.html",mess="输入信息有误，请重新输入！")
    name=lis[0][1]
    signa=lis[0][3]
    dat=time.localtime()
    dateT=time.strftime("%Y-%m-%d %X",dat)
    try:
        cursor.execute("UPDATE users SET loginTime='%s' WHERE email='%s'"%(dateT,email))
        db.commit()
    except:
        print("update error")
        db.rollback()
    db.close()
#     name=lis[0][1]
#     signa=lis[0][3]
#     conn=pymysql.connect(host="127.0.0.1",port=3306,user="root",password="",db="jobInfo",charset="utf8")
#     cursor=conn.cursor()
#     cursor.execute("SELECT job,jobLink,money,companyName FROM jobInfos")
#     lists=cursor.fetchall()
#     conn.close()
#     return render_template("/common/succLogin.html",username="Welcome,%s"%name,lis=lists)
    return render_template("show_zfs.html",username=name,signature=signa,emailU=email)
#     return redirect("/show/'%s'"%email)
# @app.route("/table")
# def table():
#     conn=pymysql.connect(host="127.0.0.1",port=3306,user="root",password="",db="jobInfo",charset="utf8")
#     cursor=conn.cursor()
#     cursor.execute("SELECT job,jobLink,money,companyName FROM jobInfos LIMIT 0,10")
#     lis=cursor.fetchall()
#     conn.close()
#     return render_template("/common/table.html",lis=lis)
# @app.route("/login",methods=['POST'])
# @app.route("/show/<email>")
# def show(email):
#     db=MySQLdb.connect("127.0.0.1","root","","psutils",charset="utf8")
#     cursor=db.cursor()
#     cursor.execute("SELECT * FROM users WHERE email ='%s'"%email)
#     lis=cursor.fetchall()
#     
@app.route('/usInfo',methods=['POST'])
def usInfo():
    sig=request.form['tex']
    email=request.form['hidEmail']
    print(email)
#     if sig=="小哥哥小姐姐没有签名。" or len(sig)>15:
#         print("shio")
#         return
    db=MySQLdb.connect('127.0.0.1',"root","","psutils",charset="utf8")
    cursor=db.cursor()
    
    try:
        cursor.execute("UPDATE users SET signature='%s' WHERE email='%s'"%(sig,email))
        db.commit()
    except:
        print("sigUpdate error")
        db.rollback()
    cursor.execute("SELECT * FROM users WHERE email ='%s'"%email)
    lis=cursor.fetchall()
    name=lis[0][1]
    signa=lis[0][3]
    db.close()
    return render_template("show_zfs.html",username=name,signature=signa,emailU=email)

app.run()