from flask import Flask,render_template, request
from flask_mysqldb import MySQL
import os
import pandas as pd 
from flask_jsonpify import jsonpify
import json

template_dir = os.path.abspath('../Users/spans')
print(template_dir) 
app = Flask(__name__, template_folder=r"C:/Users/spans")
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sec_interview'
  
mysql = MySQL(app)

 

@app.route('/')
def form():
    return render_template('home.html')
  

@app.route('/SetData', methods = ['POST'])
def homeSet():
    if request.method == 'POST':
        req = request.get_json()

        Stage = req["stage"]
        Iteam = req["item"]
        Percentage = req["percentage"]
        print(Stage,Iteam,Percentage)
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO threathunting (Stage,Item,Percentage_of_Complation) VALUES(%s,%s,%s)''',(Stage,Iteam,Percentage))
        mysql.connection.commit()
        cursor.close() 
        return ('', 204) 



@app.route('/GetData', methods=['GET'])
def homeGet():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("""SELECT Item,Percentage_of_Complation FROM threathunting; """)
        data=cursor.fetchall()
        cursor.execute(""" SELECT Stage,AVG(Percentage_of_Complation) FROM `threathunting` GROUP by Stage""")
        gbData = cursor.fetchall()
        print(type(data))
        print(type(gbData))
        df1 = pd.DataFrame(data,columns=['x','y'])
        df2 = pd.DataFrame(gbData,columns=['x','y'])
        return jsonpify(fullData = json.loads(df1.to_json(orient='index')),gbData = json.loads(df2.to_json(orient='index')) )


if __name__=='__main__':

      #http = WSGIServer(('', 5000), app.wsgi_app) 
      #http.serve_forever()
       app.run  (debug=True,threaded=True)