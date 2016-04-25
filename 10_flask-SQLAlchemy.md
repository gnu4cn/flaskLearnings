Flask-SQLAlchemy是一个将SQLAlchemy支持，加入到应用中的Flask扩展。其需要0.6版本以上的SQLAlchemy。其目标是通过提供一些有用的默认及额外助手对象及方法来完成一些常见任务，从而简化Flask中SQLAlchemy的使用。

##快速入门

Flask-SQLAlchemy使用起来非常有意思，对于简单应用是难以置信的容易，同时对较大应用也有很好的扩展支持。要获得完整手册，可以查看**SQLAlchemy**的API文档。

###一个最小应用

通常情况下，要制作一个Flask应用，必须要做的就是创建该Flask应用，装入选择配置并通过传入到应用来建立**SQLAlchemy**对象。

一旦建立起来，该对象就包含了来自**sqlalchemy**及**sqlalchemy.org**的那些函数及助理对象及方法了（contains all the functions and helpers from both **sqlalchemy** and **sqlalchemy.org**）。此外，该对象还提供了一个名为*Model*的类，该类是一个可用于声明应用模型的生命基础（furthermore it provides a class called *Model* that is a declarative base which can be used to declare models）：

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username
```

而要建立该初始化的数据库，就只须在一个交互式Python shell中导入该db对象并运行`SQLAlchemy.create_all()`方法，来创建表与数据库：

```python
>>> from yourapplication import db
>>> db.create_all()
```

这样一下子就有了数据库。现在来建立一些用户：

```python
>>> from yourapplication import User
>>> admin = User('admin', 'admin@example.com')
>>> guest = User('guest', 'guest@example.com')
```

不过现在它们还不在数据库中，所以这里要确保将他们存入数据库：

```python
>>> db.session.add(admin)
>>> db.session.add(guest)
>>> db.session.commit()
```

对数据库中数据的访问，也就变得是小菜一叠了：

```python
>>> users = User.query.all()
[<User u'admin'>, <User u'guest'>]
>>> admin = User.query.filter_by(username='admin').first()
<User u'admin'>
```

###一些简单的关系

SQLAlchemy连接到的是关系型数据库，而关系型数据库最擅长的自然就是关系了。为此，这里要拿出一个用到两个有着相互关系的数据表的示例应用：

```python
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', 
            backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category

    def __repr__(self):
        return '<Post %r>' % self.title

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name
```

首先来建立一些对象：

```python
>>> py = Category('Python')
>>> p = Post('Hello Python!', 'Python is pretty cool', py)
>>> db.session.add(py)
>>> db.session.add(p)
```

现在因为已将*posts*作为backref中的动态关系进行了声明，其就显示为一次查询：

```python
>>> py.posts
<sqlalchemy.orm.dynamic.AppenderBaseQuery object at 0x1027d37d0>
```

于是*posts*就表现得与一个常规的查询对象一样，因此可以询问其所有与测试的“Python”类别相关的文章了：

```python
>>> py.posts.all()
[<Post 'Hello Python!'>]
```

###启蒙之路，Road to Enlightment

下面是一点与普通SQLAlchemy相比，需要知道的事：

1. SQLAlchemy给与到以下方面的访问：
    - **sqlalchemy**与**sqlalchemy.orm**中的所有函数与类
    - 一个预先配置好的有范围的名为*session*的会话（a preconfigured scoped session called *session*）
    - **元数据**（the **metadata**）
    - **引擎**（the **engine**）
    - 用于经由模型创建及丢弃数据表的**SQLAlchemy.create_all()**及**SQLAlchemy.drop_all()**方法
    - 一个配置好的声明性基类**Model**基类

2. 该**Model**声明性基类与常规的Python类表现一致，但有着一个附带的*query*属性，可用于对该模型的查询。（**Model**及**BaseQuery**）。

3. 必须要提交会话，但又不必在请求结束时移除会话，Flask-SQLAlchemy会自动移除会话。

##引入上下文，Introduction into Contexts

如只会在一个应用中使用Flask-SQLAlchemy，就可跳过本章。只需将应用传递给**SQLAlchemy**构造函数就好了。但如打算用到多个应用或在函数中动态建立应用，则要阅读一下本章。

如在函数中定义应用，却是全局性地定义**SQLAlchemy**对象，后者是如何知道前者的呢？答案就是**`init_app()`**函数：

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app
```

这段代码做的就是准备该应用使用**SQLAlchemy**。但现在却还没有将该**SQLAlchemy**对象绑定到应用。为何没有完成呢？因为可能会创建了多个应用。

那么**SQLAlchemy**究竟怎样才真正了解到应用呢？就必须要建立一个应用上下文环境。如果是在某个Flask视图函数中，那就会自动进行。但如交换式shell中，就要手动完成（参加[Creating an Application Context](http://flask.pocoo.org/docs/appcontext/#creating-an-application-context)）。

在某个shell中，像下面这样做：

```python
>>> from yourapp import create_app
>>> app = create_app()
>>> app.app_context().push()
```

在一些脚本中，其与使用with语句差不多（Inside scripts it makes also sense to use the with-statement）:

```python
def my_function():
    with app.app_context():
        user = db.User(...)
        db.session.add(user)
        db.session.commit()
```

Flask-SQLAlchemy中的某些函数接受将该应用作为选项来运行：

```python
>>> from yourapp import db, create_app
>>> db.create_all(app=create_app())
```

###配置

Flask-SQLAlchemy有着下面这些配置值。Flask-SQLAlchemy从Flask主配置装入这些值，这些值可通过各种方式生成。请注意一些配置值在引擎建立后是无法修改的，所以要尽可能早地配置好，而不要在运行时对其进行修改。

###配置键值

该扩展当前可以理解的配置键值如下：

| 配置键值                  | 说明                                  |
| :------------------------:| :----------------------------------:  |
| SQLALCHEMY_DATABASE_URI   | 用于连接的数据库的URI。比如：`sqlite:////temp/test.db`, `mysql://username:password@server/db` |
| SQLALCHEMY_BINDS          | 将绑定键值与SQLAlchemy连接URIs影视起来的一个字典。有关其的更多信息，参见[Multiple Databases with Binds](http://flask-sqlalchemy.pocoo.org/2.1/binds/#binds)。 |
| SQLALCHEMY_ECHO           | 如将该键值设置为*True*，则SQLAlchemy将记录下所有执行到stderr中的语句，这在调试时，会有用处。    |
| SQLALCHEMY_RECORD_QUERIES | 可用于显式开启或关闭查询记录。在调试或测试模式下，将自动进行查询记录。参见[`get_debug_queries()`]。 |
| SQLALCHEMY_NATIVE_UNICODE | 可用于显示关闭原生的unicode支持。在使用了不恰当的未指定编码的数据库时，在某些数据库适配器上这是必须的（比如某些Ubuntu版本上的PostgreSQL）    |
| SQLALCHEMY_POOL_SIZE      | 数据库数据池的大小。默认设置为引擎的默认值（通常是 5）。  |
| SQLALCHEMY_POOL_TIMEOUT   | 指定数据池的连接超时。默认为10。  |
| SQLALCHEMY_POOL_RECYCLE   | 多少秒后一个连接被回收。对于MySQL这时必须的，MySQL默认在8小时空闲后移除连接。请注意Flask-SQLAlchemy在使用MySQL时自动将该键值设置为2小时。 |
| SQLALCHEMY_MAX_OVERFLOW   | 对数据池达到最大大小后，控制可建立的连接数。在这些额外连接返回数据池时，其被断开并丢弃。  |
| SQLALCHEMY_TRACK_MODIFICATIONS    | 如设置为`True`，Flask-SQLAlchemy将对对象的修改进行追踪并发射出信号。而设置为`None`时，将开启追逐而发出一条通知其将在后面默认关闭的警告。这会需要更多内存同时在不需要时应将其关闭。    |


