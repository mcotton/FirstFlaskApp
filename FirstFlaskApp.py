from flask import Flask
from flask import render_template,request
from flask import json
import sqlite3



app = Flask(__name__)


conn = sqlite3.connect('movies.db')

# conn.execute('CREATE TABLE movies (name TEXT, director TEXT, rating INTEGER)')
# print ("Table created successfully");
conn.close()
@app.route("/")
def hello():
    return render_template('about.html')

@app.route("/<name>")
def hello1(name):
    return "Hello the username is "+name

@app.route('/about')
def helloab(name=None):
    return render_template('about.html')

@app.route('/save-get',methods=['POST', 'GET'])
def saveget():
    if request.method=='GET':
       a=request.args.get('name', '')
       b=request.args.get('director', '')
       c = request.args.get('rating', '')
       return "Name : "+a+" ,  Director :  "+b+"  Rating:  "+c + '/10'
    else:
        return "Not get method"


@app.route('/save-post',methods=['POST', 'GET'])
def savepost():
    conn = sqlite3.connect('movies.db')

    if request.method=='POST':
       a=request.form['name']
       b=request.form['director']
       c = request.form['rating']

       cur = conn.cursor()

       # cur.execute('CREATE TABLE movies (name TEXT, director TEXT, rating INTEGER)')

       # Insert a row of data
       cur.execute("INSERT INTO movies (name,director,rating) VALUES (?,?,?)",(a,b,c))

       # Save (commit) the changes
       conn.commit()

       conn.close()

       # We can also close the connection if we are done with it.
       # Just be sure any changes have been committed or they will be lost.
       return json.dumps({"Title":a ,"Director": b, "Rating": c})
       # return "Title : " + a + " ,  Director :  " + b + "  Rating:  " + c +'/10'
    else:
        return "error"


@app.route('/response-data')
def responsedata():
       conn = sqlite3.connect('movies.db')
       c = conn.cursor()

       # Create table
       c.execute('''select * from movies''')
       for x in c.fetchall():
        print(x["name"])
        print(x['director'])
        print(x['rating'])

        conn.close()
        #return "Name : " + a + " ,  Email :  " + b + "  Password:  " + c


# @app.route('/getjson')
# def getjson():
#     return json.dumps({"name":"king","likes":"batman"})

@app.route('/list')
def list():
    conn = sqlite3.connect('movies.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('select * from movies')

    rows = cur.fetchall();
    return render_template('MovieDirectory.html', rows = rows)


if __name__ == "__main__":
    app.run(debug=True,port=4996)