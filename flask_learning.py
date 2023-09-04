from flask import Flask,render_template
from flask import request,make_response,redirect,abort
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

class User():
    def __init__(self,name,age):
        self.name = name
        self.age = age

@app.route('/hello')
def hello_world():
    return "<h1>Hello World!</h1>"

@app.route('/home')
def show_homepage():
    return "<h1>Welcome to Homepage!</h1>"

@app.route('/<string:name>')
def show_your_name(name):
    return f"Your Name is {name}"

@app.route('/agent')
def user_agent():
    ua = request.headers.get('User-Agent')
    return f"Your browser is {ua}"

@app.route('/cookie')
def response_make():
    response = make_response("This document carries a cookie")
    response.set_cookie('answer','42')
    return response

@app.route('/test/baidu')
def RD_baidu():
    return redirect("https://www.baidu.com/") #直接跳转到对应的baidu页面

@app.route('/usr')
def get_user():
    id = None
    if not id:
        abort(404)
    return "We found this guy"

@app.route('/printhello')
def print_helloworld():
    user = User("Zhibin","19")
    return render_template("user_name.html",name=user.name)

@app.route('/temp')
def show_temp():
    return render_template("base.html",current_time = datetime.utcnow())

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html",current_time = datetime.utcnow()),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"),500

if __name__ == "__main__":
    app.run()