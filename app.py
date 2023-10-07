from flask import Flask,render_template,session,url_for,flash
from flask import request,make_response,redirect
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired,EqualTo,Email,Optional
from flask_sqlalchemy import SQLAlchemy
import mysql_utils as mu
from flask_migrate import Migrate

'''
ORM模型映射成表的三步
1. flask db init: 这步只需要执行一次
2. flask db migrate: 识别ORM模型的改变, 形成迁移脚本
3. flask db upgrade: 运行迁移脚本, 同步到数据库中
'''


app = Flask(__name__)

app.config['SECRET_KEY'] = "hardtoguessstring"
#app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{mu.username}:{mu.password}@{mu.host}:{mu.port}/{mu.database}"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////Users/zhibin.chen/Documents/模型/flask_learning/data/sqlite_data.db"

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
migrate = Migrate(app,db)

#创建数据库
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique = True)
    users = db.relationship('User',backref='roles') #一对多关系

    def __repr__(self):
        return '<Role %r>' %self.name
    
    def __init__(self,name):
        self.name = name
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    roles_id = db.Column(db.Integer,db.ForeignKey('roles.id')) #一对多关系

    def __repr__(self):
        return '<User %r>' %self.username

    def __init__(self,username):
        self.username = username

class Dimuser(db.Model):
    __tablename__ = 'Dimuser'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    password = db.Column(db.String(64),nullable=False)
    email = db.Column(db.String(64))
    #more = db.Column(db.String(64))

    def __init__(self,name,password):
        self.name = name
        self.password = password
        self.email = email

class Users():
    def __init__(self,name,age,email):
        self.name = name
        self.age = age
        self.email = email

def dformat_date(time):
    return time.strftime("%Y-%m-%d")

app.jinja_env.filters['dform'] = dformat_date

#创建表单
class NameForm(FlaskForm):
    name = StringField("What is your name",validators=[DataRequired()])
    email = StringField("What is your email",validators=[Optional()])
    password = PasswordField("Set Your Password", validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField('Submit')

'''
with app.app_context():
    db.create_all()
'''

@app.shell_context_processor
def make_shell_context():
    return dict(db=db,Dimuser=Dimuser,Users=Users,Role=Role)

@app.route('/')
def home():
    ip_address = request.remote_addr
    return render_template('homepage.html',current_time = datetime.utcnow(),page_type = "HomePage", ip=ip_address)

@app.route('/hello/<string:name>')
def hello_world(name):
    return f"<h1>Hello World! {name}!</h1>"

@app.route('/home')
def show_homepage():
    return "<h1>Welcome to Homepage!</h1>"

@app.route('/cookie')
def response_make():
    response = make_response("This document carries a cookie")
    response.set_cookie('answer','42')
    return response

@app.route('/test/baidu')
def RD_baidu():
    return redirect("https://www.baidu.com/") #直接跳转到对应的baidu页面

@app.route('/printhello')
def print_helloworld():
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    return render_template("user_name.html",name = "Guest",ip=ip_address,ua=user_agent,current_time = datetime.utcnow(),page_type='Hello')

@app.route('/mepage')
def myaccount():
    usr = Users("Bob",27,'xxxx@qq.com')
    return render_template("mepage_name.html",now = datetime.now(),user=usr)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html",current_time = datetime.utcnow()),404


@app.route("/login",methods=['GET','POST'])
def to_login():
    form = NameForm()
    if form.validate_on_submit():
        if Dimuser.query.filter_by(name=form.name.data).first() is not None:
            user = Dimuser.query.filter_by(name=form.name.data).first()
            user.password = form.password.data
            user.email = form.email.data
            db.session.commit()
            flash("You Success Change the password!")
            session['name'] = form.name.data
            session['password'] = form.password.data
        else:
            user = Dimuser(form.name.data,form.password.data,form.email.data)
            db.session.add(user)
            db.session.commit()
            flash('Add a new Person')
            session['name'] = form.name.data
            session['password'] = form.password.data
        return redirect(url_for('to_login'))
    return render_template('login_page.html',form=form,name=session.get('name'),password=session.get('password'))

'''
@app.route("/login",methods=['GET','POST'])
def to_login():
    form = NameForm()
    if form.validate_on_submit(): #当用户有提交的时候才会返回false
        old_name = session.get('name')
        if old_name is not None or old_name != form.name.data:
            flash('You success change the user name!')
        session['name'] = form.name.data
        session['password'] = form.password.data
        return redirect(url_for('to_login'))
    return render_template('login_page.html',form=form,name=session.get('name'),password=session.get('password'))
'''

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"),500

if __name__ == "__main__":
    app.run()