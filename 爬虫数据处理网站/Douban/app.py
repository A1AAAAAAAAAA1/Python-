# @Author:77
# -*- codeing = utf-8 -*-
# @TIME : 2022/5/18 22:00
# @File : app.py.py
# @Software: PyCharm

from flask import Flask,render_template
import sqlite3
app=Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/index')
def home():
    #return render_template("index.html")
    return index()
@app.route('/movie')
def movie():
    datalist =[]
    con = sqlite3.connect("douban.db")
    cur =con.cursor()
    sql ="select * from movie250"
    data =cur.execute(sql)          #查询完的语句一定要放在列表里
    for item in data:
        datalist.append(item)
    cur.close()
    con.close()
    return render_template('movie.html',movies = datalist)
@app.route('/score')
def score():
    score = []
    num = []
    con = sqlite3.connect("douban.db")
    cur = con.cursor()
    sql = "select score,count(score) from movie250 group by score"
    data = cur.execute(sql)  # 查询完的语句一定要放在列表里
    for item in data:
        score.append(item[0])
        num.append(item[1])
    cur.close()
    con.close()
    return render_template("score.html",score = score,num=num)
@app.route('/word')
def word():
    return render_template("word.html")
@app.route('/team')
def team():
    return render_template("team.html")

@app.route('/temp')
def temp():
    return render_template("temp.html")



if __name__=='__main__':
    app.run(debug=True)