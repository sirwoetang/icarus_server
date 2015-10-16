from flask import Flask

app = Flask(__name__)

from sys import platform as _platform
if _platform == "linux" or _platform == "linux2":
    # linux
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost/icarus'
    pass
elif _platform == "darwin":
    # OS X
    pass
elif _platform == "win32":
    # Windows...
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/icarus'
    pass

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.debug = False


print("App Created...")

'''initilializing the database connection to SQLLite db'''
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.types import NVARCHAR
import random
import datetime
from flask import render_template, redirect


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(500))
    email = db.Column(db.String(120), unique=True)
    region = db.Column(db.String(120))
    country = db.Column(db.String(120))
    language = db.Column(db.String(120))
    sex = db.Column(db.String(10))
    age=db.Column(db.Numeric(10))
    avatar = db.Column(db.String(120))
    fb_token = db.Column(db.String(250))
    g_token = db.Column(db.String(250))
    registered_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)

    def __init__(self, username, password, email, avatar, fb_token):
        self.username = username
        self.password = password
        self.email = email
        self.avatar = avatar
        self.fb_token = fb_token
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def __repr__(self):
        return '<User %r>' % (self.username)


class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    device_id=db.Column(db.Numeric(10))
    v1=db.Column(db.Float(10))
    v2=db.Column(db.Float(10))
    v3=db.Column(db.Float(10))
    v4=db.Column(db.Float(10))
    v5=db.Column(db.Float(10))
    v6=db.Column(db.Float(10))
    v7=db.Column(db.Float(10))
    v8=db.Column(db.Float(10))
    v9=db.Column(db.Float(10))
    device_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    created_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, device_id, v1, v2, v3, v4, v5, v6, v7, v8, v9,device_time):
        self.device_id = device_id
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.v4 = v4
        self.v5 = v5
        self.v6 = v6
        self.v7 = v7
        self.v8 = v8
        self.v9 = v9
        self.device_time = device_time

print("Classes Created...")
db.create_all()
db.session.commit()
print("Tables Created...")

def populate_users(db):
    users = User.query.all()
    if not users:
        user = User("admin","admin","1", "1","1")
        db.session.add(user)
        db.session.commit()
    else:
        pass

populate_users(db)

@app.route('/')
def render_home():
    return render_template('index.html')


@app.route('/logout')
def render_logout():
    return redirect("/login", code=302)


@app.route('/login')
def render_login():
    return render_template('login.html')


@app.route('/map')
def render_map():
    return render_template('map.html')


@app.route('/charts')
def render_charts():
    return render_template('charts.html')


@app.route('/vehicle_table')
def render_vehicle():
    return render_template('vehicle_table.html')


@app.route('/fuel_table')
def render_fuel_table():
    return render_template('fuel_table.html')


@app.route('/api/v1/data_logger', methods = ['POST', 'GET'])
def api_solar_logger():
    from flask import request
    content = request.json
    if request.method == 'GET':
        print('GET')
    else:
        # print('OTHER')
        pass

    # if 'type' in content:
    #     try:
    #         event = Event(content['type'],content['value'],content['device_id'])
    #         db.session.add(event)
    #         db.session.commit()
    #         print("Success")
    #         return 'Success'
    #     except Exception:
    #         db.session.rollback()
    #         print("Failure")
    #         return 'Failure'


    if "id" in content:
        for datum in content['data']:
            try:
                event = Event(device_id=content['id'],v1=datum['v1'],
                          v2=datum['v2'],v3=datum['v3'],
                          v4=datum['v4'],v5=datum['v5'],
                          v6=datum['v6'],v7=datum['v7'],
                          v8=datum['v8'],v9=datum['v9'],
                          device_time=datum['t1'])
                db.session.add(event)
                db.session.commit()
            except Exception:
                db.session.rollback()
                return 'Failure'

    return 'Success'

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=port)
