from flask import Flask, render_template, request , url_for , session , redirect
import os
from datetime import datetime , timedelta
from flask import redirect
from functools import wraps
from detectapp import model_aptos
from flask_sqlalchemy import SQLAlchemy # import sqlalchemy
from database import  db  , Entry , DB_Manager
# webserver gateway interface
app = Flask(__name__)
app.config.update(
    TESTING = True,
    SECRET_KEY = "password"
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/vehicle_db.sqlite3' # Config to use sqlalchemy
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db_manager = DB_Manager()
BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH,'static/upload/')
@app.route('/',methods =['POST','GET'])
def login():
    error= None
    session['logged_in']=False
    if request.method=='POST':
        if (request.form['login'] != '0000' or request.form['password'] != 'admin') and (request.form['login'] != 'yahya' or request.form['password'] != 'yahya') and (request.form['login'] != 'ghofrane' or request.form['password'] != 'ghofrane') :
            error='INVALIDE'
        else:
            session['logged_in']=True
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/home',methods=['POST','GET'])

def home():
    if session['logged_in']==True :
       if request.method == 'POST':
         name = request.form["name"]
         print(name)
         upload_file = request.files['image_name']
         filename = upload_file.filename
         path_save = os.path.join(UPLOAD_PATH,filename)
         upload_file.save(path_save)
         text_aptos=model_aptos(path_save)
         curr_time_new_entry = datetime.now().isoformat(' ', 'seconds')
         new_entry = Entry(malade = name , entry_dtime = curr_time_new_entry , statu=text_aptos)
         db.session.add(new_entry) 
         db.session.commit() 
         db_manager.get_db_data()
         return render_template('index.html',upload=True,upload_image=filename,text=text_aptos,no=len(text_aptos))

       return render_template('index.html',upload=False)
    else:
            return redirect(url_for('login'))
@app.route("/register",methods=['POST','GET'])
def log_mode():
    db_man = DB_Manager()
    page_title = 'Log Mode'
    error = False
    error_message = ""
    try:
        if request.method == 'POST':
            noun = request.form["delete_plate_input"]
            print(noun)
            if noun:
                db_man.delete_pat(noun)
            else:
                error_message = "Input Plate isn't registered or Input is empty"
            return redirect(url_for('log_mode'))
    

    except Exception as e:
        print(f"EXCEPTION AT /database route: {e}")
        error = True
        error_message = "Vehicle Plate is invalid or not existing"

    return render_template("log_mode.html", db_data = db_man.db_data_entries) 


if __name__ =="__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)