from flask import Flask

app = Flask(__name__)

'''
视图函数绑定多个URL
'''
@app.route('/')
@app.route('/test')
def hello():
    return "<h1>Hello World! Flask<h1>"

'''
动态URL
'''
@app.route('/hello',defaults={'name':"Stranger"}) #使用defaults设置URL变量的默认值 等同于改写 def hello_name(name="Stranger")
@app.route('/hello/<name>')
def hello_name(name):
    return f"<h1>Hello! {name}<h1>"

'''
flask run --host=0.0.0.0  切换内网ip地址
flask run --port=8000 切换端口

'''