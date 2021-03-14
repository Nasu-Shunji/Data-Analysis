from flask import Flask, render_template, request, session, redirect, url_for, jsonify, g
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlite3
import pickle

app = Flask(__name__)
app.secret_key = b'random string...'

engine = create_engine('sqlite:///TF.sqlite3')
Base = declarative_base()

member_data = {}
member_data_file = 'member_data.dat'

#load member_data from file
try:
    with open(member_data_file, "rb") as f:
        list = pickle.load(f)
        if list != None:
            member_data = list
except:
    pass

# model class
class Mydata(Base):
    __tablename__ = 'mydata'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    age = Column(Integer)
    people = Column(String(255))
    gender = Column(String(255))
    live = Column(String(255))
    ride = Column(String(255))
    destination = Column(String(255))
    money = Column(Integer)

    #get Dict data
    def toDict(self):
        return {
            'id': int(self.id),
            'name': str(self.name),
            'age': int(self.age),
            'people': str(self.people),
            'gender': str(self.gender),
            'live': str(self.live),
            'ride': str(self.ride),
            'destination': str(self.destination),
            'money': int(self.money)
        }
# get List data
def getByList(arr):
    res = []
    for item in arr:
        res.append(item.toDict())
    return res

# get all mydata record
def getAll():
    Session = sessionmaker(bind=engine)
    ses = Session()
    res = ses.query(Mydata).all()
    ses.close()
    return res

#access top page.
@app.route('/', methods=['GET'])
def index():
    return render_template('form.html', \
        login =False, \
        title = 'Sign up/Login', \
        message='not logined...',)

@app.route('/ajax', methods=['GET'])
def ajax():
    mydata = getAll()
    return jsonify(getByList(mydata))

#login form sended.
@app.route('/login', methods=['POST'])
def login_post():
    global member_data
    id = request.form.get('id')
    pswd = request.form.get('pass')
    if id in member_data:
        if pswd == member_data[id]:
            flg = 'True'
        else:
            flg = 'False'
    else:
        flg = 'False'
        try:
            with open(member_data_file, 'wb') as f:
                pickle.dump(member_data, f)
        except:
            pass
    return flg

@app.route('/signup', methods=['POST'])
def signup_post():
    global member_data
    id = request.form.get('id')
    pswd = request.form.get('pass')
    age = request.form.get('age')
    people = request.form.get('people')
    gender = request.form.get('sel1')
    live = request.form.get('sel2')
    if id == "" or pswd == "" or age == '' or people == "" or gender == "" or live == "":
        flg = 'False'
    else:
        member_data[id] = pswd
        flg = 'True'
        try:
            with open(member_data_file, 'wb') as f:
                pickle.dump(member_data, f)
        except:
            pass
    return flg
@app.route('/index', methods=['POST'])
def trip_post():
    id = request.form.get('id')
    age = request.form.get('age')
    people = request.form.get('people')
    gender = request.form.get('sel1')
    live = request.form.get('sel2')
    ride = request.form.get('ride')
    destination = request.form.get('destination')
    money = request.form.get('money')
    if age == "20代":
        age = 20
    elif age == "30代":
        age = 30
    elif age == "40代":
        age = 40
    elif age == "50代":
        age = 50
    else:
        age = 60
    if ride == "":
        return 'False'
    else:
        mydata = Mydata(name=id, age=age, people=people, gender=gender, live=live, ride=ride, destination=destination, money=money)
        Session = sessionmaker(bind=engine)
        ses = Session()
        ses.add(mydata)
        ses.commit()
        ses.close()
        return 'True'

if __name__ == "__main__":
    app.run(host="localhost")



