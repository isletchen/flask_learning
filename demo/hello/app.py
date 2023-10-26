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
@app.route('/hello',defaults={'name':"Stranger"}) 
#使用defaults设置URL变量的默认值 等同于改写 def hello_name(name="Stranger")
@app.route('/hello/<name>')
def hello_name(name):
    return f"<h1>Hello! {name}<h1>"

'''
flask run --host=0.0.0.0  切换内网ip地址
flask run --port=8000 切换端口
可以使用url_fo()函数来获取端点 (endpoint), 端点用来标记视图函数与对应URL的规则, 端点的默认值是视图函数名
当URL有动态部分的时候: url_for('hello_name',name="Jack")
若将_external参,数设为True, 则会生成可供外部使用的完整URL
'''

# 1.8 Flask命令
@app.cli.command() 
#使用该装饰器注册一个新的flask命令, 命令与函数名相同: flask new_func
#同时也可以在装饰器中修改命令名称 => @app.cli.command("say_hello") => flask say_hello
def new_func():
    print("Say hello to you")


# 1.9 模版和静态文件
'''
模版文件(HTML)存放在：/templates
静态文件(CSS)存放在：/static

CDN指分布式服务器系统。服务商把你需要的资源存储在分布于不同地理位置的
多个服务器，它会根据用户的地理位置来就近分配服务器提供服务(服务器越近，
资源传送就越快)。使用CDN服务可以加快网页资源的加载速度, 从而优化用户体
验。对于开源的CSS和JavaScript库, CDN提供商通常会免费提供服务
'''


# 1.10 Flask与MVC架构
'''
MVC架构 ==> Model - View - Controller, 模型-视图-控制器 , 数据处理 - 用户界面 - 交互逻辑
'''