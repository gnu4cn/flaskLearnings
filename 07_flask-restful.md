#Flask-RESTful

**Flask-RESTful**是一个将快速构建REST APIs功能加入进来的Flask的扩展。其是一个对现有ORM/库进行操作的一个轻量级抽象。Flask-RESTful鼓励最小设置最佳实践（Flask-RESTful encourages best pratices with minimal setup）。如对Flask比较熟悉，那么使用Flask-RESTful也将较为容易。

##Flask-RESTful的安装

都应在virtualenv下进行，使用`pip`：

```bash
(venv) unisko@peng-R429:~/flask$ pip install flask-restful
```

而最新的开发版本，可从[项目的GitHub页面](https://github.com/flask-restful/flask-restful)下载到：

```bash
git clone https://github.com/flask-restful/flask-restful.git
cd flask-restful
python setup.py develop
```

Flask-RESTful有着下面的以来（在使用`pip`时将自动安装）：

- [Flask](http://flask.pocoo.org/) 版本0.8已上

Flask-RESTful要求Python的版本为2.6、2.7、3.3或3.4。


##快速入门

现在就是编写第一个REST API的时间了。本手册假定有着对Flask可以使用的掌握，同时已经安装好Flask及Flask-RESTful。否则请参考上面的安装过程。

###一个最小的API

这个最小的Flask-RESTful API看起来像是这样的：

```python
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world!'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
```

将这段代码保存为*api.py*并使用Python解释器加以运行。请注意这里开启了Flask的调试模式，来提供到代码重新装入及更好的错误消息。

```bash
(venv) unisko@peng-R429:~/flask/demos/restful$ python api.py
 * Running on http://127.0.0.1:8080/
 * Restarting with reloader
```

>警告：

>在生产环境下绝对不要开启调试模式！

现在打开一个新的终端窗口，使用curl来测试该API：

```bash
$curl http://localhost:8080/
{
    "hello": "world!"
}
```

###资源式的路由

Flask-RESTful提供的主要构建块，就是这些资源了（the main building block provided by Flask-RESTful are resources）。这些资源，是建立在[Flask的可插入式视图，Flask pluggable views](http://flask.pocoo.org/docs/views/)上的，从而提供到通过定义出资源上的方法，而容易地对多种HTTP方法的访问。某个应用的基本CRUD资源（a basic CRUD<create, retrieve, udpate and delete> resource），看起来像是这样：

```python
from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = []

class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
```

>注意，这里URL中变量规则的写法：`<string:todo_id>`，其中类型和变量名之间是不能有空格的!


可像下面这样来试一下这段代码：

```bash
$ curl http://localhost:5000/todo1 -d "data=Remember the milk" -X PUT
{"todo1": "Remember the milk"}
$ curl http://localhost:5000/todo1
{"todo1": "Remember the milk"}
$ curl http://localhost:5000/todo2 -d "data=Change my brakepads" -X PUT
{"todo2": "Change my brakepads"}
$ curl http://localhost:5000/todo2
{"todo2": "Change my brakepads"}
```

或者在安装了`requests`库后，也可以从Python进行尝试：

```python
>>> from requests import put, get
>>> put('http://localhost:5000/todo1', data={'data': 'Remember the milk'}).json()
{u'todo1': u'Remember the milk'}
>>> get('http://localhost:5000/todo1').json()
{u'todo1': u'Remember the milk'}
>>> put('http://localhost:5000/todo2', data={'data': 'Change my brakepads'}).json()
{u'todo2': u'Change my brakepads'}
>>> get('http://localhost:5000/todo2').json()
{u'todo2': u'Change my brakepads'}
```

