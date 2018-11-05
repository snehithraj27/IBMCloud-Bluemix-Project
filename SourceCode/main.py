# Author: Snehith Raj Bada

import csv
import io
import random
from flask import Flask, render_template, request
app = Flask(__name__)
import pyodbc


server = 'cloud071.database.windows.net'
database = 'cloud'
username = 'snehith123'
password = '*****'
driver = '{ODBC Driver 13 for SQL Server}'
con = pyodbc.connect(
      'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

cursor = con.cursor()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/uploadcsv', methods=['POST', 'GET'])
def insert_table():
   cursor.execute("CREATE TABLE if not exists earthquake(time varchar(50), latitude float(30), longitude float(30), depth float(10), mag float(10), magType varchar(10), nst int, gap float(10), dmin float(30), rms float(10), id varchar(20), place varchar(50), depthError float(10), magError float(10), magNst int, locationSource varchar(10))")
   con.commit()
   print('Connected to the database')
   if request.method == 'POST':
       f = request.files['inputfile']
       if not f:
           return "No file"
       stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
       csv_input = csv.reader(stream)
       next(csv_input)
       for row in csv_input:
           print(row)
           try:
               cursor.execute(
                   "INSERT INTO earthquake(time, latitude, longitude, depth, mag, magType, nst, gap, dmin, rms, id, place, depthError, magError, magNst, locationSource) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",row)
               cursor.commit()
           except Exception as e:
               print(e)
               cursor.rollback()
   return render_template('home.html')

#Method to display all the records
@app.route('/getrecords', methods=['POST', 'GET'])
def get_records():
    if request.method == 'POST':
        cursor.execute('SELECT * from earthquake;')
        rows = cursor.fetchall()
        print(rows)
        return render_template("data.html", msg=rows)

#Method to delete all the records
@app.route('/deleterecords', methods=['POST', 'GET'])
def delete_records():
    if request.method == 'POST':
        cursor.execute("delete from earthquake")
        con.commit()
        rows = cursor.fetchall();
        print(rows)
        return render_template("result.html", msg="All records deleted")

#Method to find magnitude greater than some value
@app.route('/magnitudevalue', methods=['POST', 'GET'])
def search_magnitudevalue():
    rows = ''
    if request.method == 'POST':
        magnitude = request.form['magnitude']
        print(magnitude)
        cursor.execute("SELECT count(*) from earthquake where mag > 5", (magnitude,))
        rows=cursor.fetchall()
        print(rows)
        return render_template('data.html', msg=rows)

#Method to retrieve records based on the specified magnitude range and date
@app.route('/magnituderange', methods=['POST', 'GET'])
def search_magnituderange():
    if request.method == 'POST':
        mag1 = request.form['magnitude1']
        mag2 = request.form['magnitude2']
        date1 = request.form['date1']
        date2 = request.form['date2']
        print(mag1, mag2, date1, date2)
        cursor.execute("select * from earthquake where ((mag between ? and ?) and (time between ? and ?)) ", (mag1,
                    mag2, date1, date2,))
        rows = cursor.fetchall();
        print(rows)
        return render_template("data.html", msg=rows)

#Method to find earthquakes near to specific location
@app.route('/magnitudeplace', methods=['POST', 'GET'])
def search_magnitudeplace():
    if request.method == 'POST':
        distance = request.form['distance']
        place=request.form['place']
        print(distance,place)
        replace = '{0}km%{1}'.format(distance, place)
        print (replace)
        cursor.execute("SELECT * FROM earthquake WHERE place like ?", (replace,))
        rows = cursor.fetchall();
        print(rows)
        return render_template("data.html", msg=rows)

#Method to find the stats
@app.route('/stats', methods=['POST', 'GET'])
def search_stats():
    if request.method == 'POST':
        magnitude = request.form['magnitude']
        print(magnitude)
        cursor.execute("SELECT * FROM earthquake WHERE mag > ? and (CAST( time as time) >= '20:00:00' or CAST( time as time)< '07:00:00')",(magnitude,))
        rows = cursor.fetchall();
        c = len(rows)
        print(c)
        print(rows)
        result="No of earthquakes of magnitude greater than {0} during night is {1}".format(magnitude,c)
        return render_template("result.html", msg=result)

#Method to find the cluster
@app.route('/cluster', methods=['POST', 'GET'])
def earthquake_cluster():
    if request.method == 'POST':
        cursor.execute("SELECT nst from earthquake")
        rows = cursor.fetchall();
        print(rows)
        result=list(rows)
        resultnew=[]
        for i in rows:
            resultnew.append(i[0])
        print(resultnew)
        clustering(resultnew)
        return render_template("result.html", msg=resultnew)


a, b = -100, -100
cluster1, cluster2 = [], []


def centroid(l1, l2):
    l11 = float(sum(l1)) / float(len(l1))
    l22 = float(sum(l2)) / float(len(l2))
    return (l11, l22)


def distance(items, i, j):
    print(items, i, j)
    i = items - i
    j = items - j
    if abs(i) < abs(j):
        return 1
    else:
        return 0


def kmeanscluster(result, x, y):
    global cluster1, cluster2
    global a, b
    print("a", a, "b", b, "x", x, "y", y)
    if a == x and b == y:
        return cluster1, cluster2
    else:
        cluster1, cluster2 = [], []
        for items in result:
            print(items)
            temp = distance(items, x, y)
            if temp == 1:
                cluster1.append(items)
            elif temp == 0:
                cluster2.append(items)
        a, b = x, y
        x, y = centroid(cluster1, cluster2)
        kmeanscluster(result, x, y)


def clustering(result):
    t = 0
    while t == 0:
        i = random.sample(result, 1)
        j = random.sample(result, 1)
        if i != j:
            t = 1
    x = i[0]
    y = j[0]
    print("samples",x,y)
    kmeanscluster(result, x, y)
    print(cluster1, cluster2)

if __name__ == '__main__':
    app.run(debug = True)