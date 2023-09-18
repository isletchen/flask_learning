from flask import Flask,render_template,session,url_for
from flask import request,make_response,redirect
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired,EqualTo

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = "hardtoguessstring"

class User():
    def __init__(self,name,age,email):
        self.name = name
        self.age = age
        self.email = email

def dformat_date(time):
    return time.strftime("%Y-%m-%d")

app.jinja_env.filters['dform'] = dformat_date

class NameForm(FlaskForm):
    name = StringField("What is your name",validators=[DataRequired()])
    password = PasswordField("Set Your Password", validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField('Submit')

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
    usr = User("Bob",27,'xxxx@qq.com')
    return render_template("mepage_name.html",now = datetime.now(),user=usr)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html",current_time = datetime.utcnow()),404

'''
@app.route("/login",methods=['GET','POST'])
def to_login():
    name = None
    password = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        password = form.password.data
        form.name.data = ''
        form.password.data= ''
    return render_template('login_page.html',form=form,name=name,password=password)
'''
@app.route("/login",methods=['GET','POST'])
def to_login():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['password'] = form.password.data
        return redirect(url_for('to_login'))
    return render_template('login_page.html',form=form,name=session.get('name'),password=session.get('password'))

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"),500

if __name__ == "__main__":
    app.run()