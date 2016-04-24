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

Flask-RESTful对来自视图方法的多种返回值类型，都是理解的。与Flask类似，可以返回任何可迭代的值，同时其会被转换成一个相应，以及原始的Flask响应对象（similar to Flask, you can return any interable and it will be converted into a response, including raw Flask response objects）。使用多个的返回值，Flask-RESTful同样支持响应代码与响应头部的设置，如下所示：

```python
class Todo1(Resource):
    def get(self):
        # Default to 200 OK
        return {'task': 'Hello world'}

class Todo2(Resource):
    def get(self):
        # Set the response code to 201
        return {'task': 'Hello world'}, 201

class Todo3(Resource):
    def get(self):
        # Set the response code 201 and return custom headers
        return {'task', 'Hello world'}, 201, {'Etag': 'some-opaque-string'}
```

###端点，Endpoints

在某个API中多数时间，资源都将有着多个的URLs。可将多个的URLs传递给Api对象的[`add_resource()`](http://flask-restful.readthedocs.org/en/0.3.5/api.html#flask_restful.Api.add_resource)方法。每个URL都将被路由到该资源：

```python
api.add_resource(HelloWorld, 
    '/',
    '/hello')
```

也同样可以对路径的一些部分进行匹配，以将其作为到资源方法的变量：

```python
api.add_resource(Todo,
    '/todo/<int:todo_id>', endpoint='todo_ep')
```

>注意：

>如果某次请求与所有应用端点都不匹配，Flask-RESTful就会返回一个带有一些建议的与被请求端点匹配接近的端点的404错误消息（if a request does not match any of your application‘s endpoints, Flask-RESTful will return a 404 error message with suggestions of other endpoints that closely match the requested endpoint）。此特性可通过在应用配置中将`ERROR_404_HELP`设置为`FALSE`加以关闭。

###参数解析，Argument Parsing

尽管Flask提供了容易的对请求数据的访问（比如查询字串<querystring>或POST的表单编码数据），但对于验证表单数据，仍然比较痛苦。而Flask-RESTful就通过使用一个类似于[argparse](http://docs.python.org/dev/library/argparse.html)的库，具有对请求数据进行验证的内建支持。

```python
from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('rate', type=init, help='Rate to charge for this resource')
args = parser.parse_args()
```

>注意：

>与argparse模块不同，[`reqparse.RequestParser.parse_args()`]返回一个Python字典，而不是一种定制的数据结构。

使用该`reqparse`模块，还免费给出了完整的错误消息。如果某个参数未能通过验证，Flask-RESTful就会给出一个400 Bad Request的响应，以及一个突出显示该错误的响应。

```bash
$ curl -d 'rate=foo' http://127.0.0.1:5000/todos
{'status': 400, 'message': 'foo cannot be converted to int'}
```

而[inputs](http://flask-restful.readthedocs.org/en/0.3.5/api.html#module-inputs)模块又提供了一些其所包含的常用转换函数，比如[`inputs.date()`](http://flask-restful.readthedocs.org/en/0.3.5/api.html#inputs.date)及[`inputs.url()`](http://flask-restful.readthedocs.org/en/0.3.5/api.html#inputs.url)等。

以带有`strict=True`方式调用`parse_args`方法，就会在请求包含了解析器中未定义的参数时，保证抛出一个错误消息（calling `parse_args` with `strict=True` ensures that an error is thrown if the request includes arguments your parser does not define）。

```python
args = parser.parse_args(strict=True)
```

###数据的格式化，Data Formatting

默认情况下，返回迭代中的所有字段都将被原样渲染。尽管这样做在仅处理Python数据结构时毫无问题，但在操作到对象时，就会带来很大困扰（by default, all fields in your return iterate will be rendered as-is. it can be very frustrating when working with objects）。为解决这个问题，Flask-RESTful提供了[fields](http://flask-restful.readthedocs.org/en/0.3.5/api.html#module-fields)模块及[`marshal_with()`](http://flask-restful.readthedocs.org/en/0.3.5/api.html#flask_restful.marshal_with)修饰器。与Django的ORM及WTForm类似，可使用该`fields`模块来描述响应的结构。

```python
from collections import OrderedDict
from flask_restful import fields marshal_with

resource_fields = {
        'task': fields.String
        'url': fields.Url('todo_ep')
}

class TodoDao(object):
    def __init__(self, todo_id, task):
        self.todo_id = todo_id
        self.task = task

        # This field will not be sent in the response
        self.status = 'active'

class Todo(Resourse):
    @marshal_with(resource_fields)
    def get(self, **kwargs):
        return TodoDao(todo_id='my_todo', task='Remember the milk')
```

###完整示例

请将本示例保存在*api.py*中：

```python
from flask import Flask
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

TODOS = {
        'todo1': {'task': 'build an API'},
        'todo2': {'task': '?????'},
        'todo3': {'task': 'profit!'},
        }

def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')

# Todo
# shows a single todo item and lets you delete a todo item

class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201

# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo'))+1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

##
## Actually setup the Api resource routing here
##

api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
```

示例的用法：

```bash
$python api.py
 * Running on http://127.0.0.1:5000/
 * Restarting with reloader
```

清单的获取：

```bash
$ curl http://localhost:5000/todos
{"todo1": {"task": "build an API"}, "todo3": {"task": "profit!"}, "todo2": {"task": "?????"}}
```

获取一个单一的task:

```bash
$ curl http://localhost:5000/todos/todo3
{"task": "profit!"}
```

删除一个task:

```bash
$ curl http://localhost:5000/todos/todo2 -X DELETE -v

> DELETE /todos/todo2 HTTP/1.1
> User-Agent: curl/7.19.7 (universal-apple-darwin10.0) libcurl/7.19.7 OpenSSL/0.9.8l zlib/1.2.3
> Host: localhost:5000
> Accept: */*
>
* HTTP 1.0, assume close after body
< HTTP/1.0 204 NO CONTENT
< Content-Type: application/json
< Content-Length: 0
< Server: Werkzeug/0.8.3 Python/2.7.2
< Date: Mon, 01 Oct 2012 22:10:32 GMT
```

加入一个新的task:

```bash
$ curl http://localhost:5000/todos -d "task=something new" -X POST -v

> POST /todos HTTP/1.1
> User-Agent: curl/7.19.7 (universal-apple-darwin10.0) libcurl/7.19.7 OpenSSL/0.9.8l zlib/1.2.3
> Host: localhost:5000
> Accept: */*
> Content-Length: 18
> Content-Type: application/x-www-form-urlencoded
>
* HTTP 1.0, assume close after body
< HTTP/1.0 201 CREATED
< Content-Type: application/json
< Content-Length: 25
< Server: Werkzeug/0.8.3 Python/2.7.2
< Date: Mon, 01 Oct 2012 22:12:58 GMT
<
* Closing connection #0
{"task": "something new"}
```

更新某个task:

```bash
$ curl http://localhost:5000/todos/todo3 -d "task=something different" -X PUT -v

> PUT /todos/todo3 HTTP/1.1
> Host: localhost:5000
> Accept: */*
> Content-Length: 20
> Content-Type: application/x-www-form-urlencoded
>
* HTTP 1.0, assume close after body
< HTTP/1.0 201 CREATED
< Content-Type: application/json
< Content-Length: 27
< Server: Werkzeug/0.8.3 Python/2.7.3
< Date: Mon, 01 Oct 2012 22:13:00 GMT
<
* Closing connection #0
{"task": "something different"}
```


