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

>译者注：无论是经由直接使用SQLAlchemy的构造函数`SQLAlchemy(app)`, 抑或使用SQLAlchemy的`init_app(app)`方式，都会在生成的`db`实例中，生成一个`app`属性，该属性就是`app`这个flask的实例，可以经由`db.app`访问到这个flask的`app`实例的方法或属性。

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

*0.8版本中的新配置键值情况*： 新加入的`SQLALCHEMY_NATIVE_UNICODE`, `SQLALCHEMY_POOL_SIZE`, `SQLALCHEMY_POOL_TIMEOUT`及`SQLALCHEMY_POOL_RECYCLE`。

*0.12版本新键值*：加入了`SQLALCHEMY_BINDS`。

*0.17版本新键值*：加入了`SQLALCHEMY_MAX_OVERFLOW`。

*2.0版本新建值*：加入了`SQLALCHEMY_TRACK_MODIFICATIONS`。

*2.1版本新情况*：在为对`SQLALCHEMY_TRACK_MODIFICATIONS`进行设置时将发出警告。


###连接URI的格式

完整的连接URIs清单，请查看SQLAlchemy文档[Supported Databases](http://www.sqlalchemy.org/docs/core/engines.html)。这里是一些常见的连接字串。

SQLAlchemy将某种引擎的资源，表示为带有指明该引擎各种选项的可选关键字参数的URI。URI的格式为：

```
dialect+driver://username:password@host:port/database
```

字串中的多个部分都是可选的。如未指定数据库驱动，则就选择默认驱动（但要确保此时不要包括`+`号）。

Postgres:

```
postgresql://scott:tiger@localhost/mydatabase
```

MySQL：

```
mysql://scott:tiger@localhost/mydatabase
```

Oracle:

```
oracle://scott:tiger@127.0.0.1:1521/sidname
```

SQLite(请注意开头的四个斜杠)：

```
sqlite:////absolute/path/to/foo.db
```

###使用定制元数据MetaData及命名约定

可以使用一个定制的**MetaData**对象，来构建出**SQLAlchemy**对象。这样做除了其它一些目的外，允许指定一种[定制的常量命令约定(custom constraint naming convention)](http://docs.sqlalchemy.org/en/latest/core/constraints.html#constraint-naming-conventions)。在处理数据库迁移时，这么做是重要的（比如[这里](http://alembic.readthedocs.org/en/latest/naming.html)指出的使用[alembic](https://alembic.readthedocs.org/)）。因为SQL并没有定义标准的命名约定，所以其默认在不同数据库实现之间既没有保证，也没有有效的兼容性。此时就可以定义一种定制的命名约定，如同这里的SQLAlchemy文档中所建议的那样：

```python
from sqlalchemy import MetaData
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

convention = {
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constrant_names)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
        }

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
```

关于**MetaData**的更多内容，参见[check out the offical docs on it](http://docs.sqlalchemy.org/en/latest/core/metadata.html)。

##模型的声明

一般来讲，Flask-SQLAlchemy与一个已被良好配置的[declarative](http://www.sqlalchemy.org/docs/orm/extensions/declarative/api.html#module-sqlalchemy.ext.declarative)扩展中的声明性基类表现一致（Generally Flask-SQLAlchemy behaves like a properly configured declarative base from the [declarative](http://www.sqlalchemy.org/docs/orm/extensions/declarative/api.html#module-sqlalchemy.ext.declarative) extension）。因此这里建议阅读一下SQLAlchemy的文档，以获得全面的掌握。但最常用的一些用例，在这里都有说明。

要记住下面一些事情：

- 所有应用模型的基类，叫做*db.Model*。该基类是存储在必须要创建的SQLAlchemy实例上的。

- SQLAlchemy中所必须的一些部分，在Flask-SQLAlchemy中是可选的。比如数据表名称在没有刻意重写时，会被自动设置。其是派生自类名称转换成小写形式，及驼峰表示法“CamelCase”到“camel_case”的转换。

###简单示例

这里有一个非常简单的示例：

```python
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

可以看出，这里使用`db`对象的**Column**方法来定义一个列。列的名称就是指派给它的名称。如打算在数据表中用一个不同的名称，可提供可选的第一个参数，该参数就是一个所需列名称的字符串（if you want to use a different name in the table you can provide a optional first argument which is a string with the desired column name）。主键是使用`primary_key=True`来标记出的。可将多个键标记为主键，此时它们就成为了一个复合主键。

列的类型是`Column`方法的第一个参数。既可以直接提供出列类型，也可以在稍后对其进行调用来加以指定（比如提供一个长度值）。下面是一些最常见的列类型：

| 列数据类型                | 说明                                      |
| :-----------:             | :------------------:                      |
| 整数（Integer）           | 一个整数                                  |
| 字符串（String(size)）    | 一个有着最大长度的字符串                  |
| 文本（Text）              | 一些较长的unicode文本                     |
| 日期时间数据（DateTime）  | 以Python的`datetime`对象表示日期和时间    |
| 浮点值数据（Float）       | 存储浮点值                                |
| 逻辑值（Boolean）         | 存储一个逻辑数值                          |
| PickleType                | 存储一个经Python的pickle模块转换后的Python 对象  |
| 大型二进制文件            | 存储任意的大型二进制数据                  |


###一到多的关系

最常见的关系，就是一到多的关系了。因为关系时在确立前声明的，所以可以使用字符串来代表一些尚未建立的类（举例来说比如类*Person*定义了一个到*Article*的关系，而*Article*时在文件的后面才声明的）。

关系是用[`relationship()`](http://www.sqlalchemy.org/docs/orm/relationship_api.html#sqlalchemy.orm.relationship)函数进行表达的。但是外键就必须使用类[`sqlalchemy.schema.ForeignKey`](http://www.sqlalchemy.org/docs/core/constraints.html#sqlalchemy.schema.ForeignKey)进行单独声明：

```python
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    addresses = db.relationship('Address', backref='person',
            lazy='dynamic')

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'))
```

那么`db.relationship()`到底做了什么呢？该函数返回了一个新的可以完成多个事情的属性值。在本例中，告诉它指向到`Address`类并装入多个的此类。其是怎么知道这将返回多个的地址的呢？因为SQLAlchemy从声明中猜到一个有用的默认值。而如果打算要一个一对一的关系，可将`uselist=False`传递给`relationship()`方法。

这里的*backref*和*lazy*又是什么意思呢？*backref*是一种同时在*Address*类上声明一个新的属性值的简单方式。随后就可以使用`my_address.person`来获取到该地址上的那个人了。*lazy*定义出了SQLAlchemy于何时从数据库装入数据：

- `'select'`（这时默认的*lazy*选项），意思是SQLAlchemy将在必要的使用标准*select*语句时，才装入数据（`'select'`(which is the default) means that SQLAlchemy will load the data as neccessary in one go using a standard *select* statement）。

- `'joined'`告诉SQLAlchemy，在父类使用*JOIN*语句时，在同一查询中装入该关系（`'joined'`tells SQLAlchemy to load the relationship in the same query as the parent using a *JOIN* statement）。

- `'subquery'`与`'joined'`工作类似，但此时SQLAlchemy将使用一个子查询（`'subquery'` works like `'joined'` but instead SQLAlchemy will use a subquery）。

- `'dynamic'` 是比较特殊的，同时在有着许多关系数据条目时是有用的。SQLAlchemy将返回另一个可在装入之前进一步处理的查询对象，而不是装入这些数据条目。在期望得到许多的此关系的数据时，通常会采用此选项（`'dynamic'` is special and useful if you have many items. Instead of loading the items SQLAlchemy will return another query object which you can further refine before loading the items. This is usually what you want if you expect more than a handful of items for this relationship）。

怎样来定义backrefs的lazy状态呢？使用[`backref()`](http://www.sqlalchemy.org/docs/orm/relationship_api.html#sqlalchemy.orm.backref)函数：

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    addresses = ad.relationship('Address',
            backref=db.backref('person', lazy='joined'), lazy='dynamic')
```

###多到多的关系

在打算使用多到多关系时，需要定义出一个用于关系的助手数据表（a helper table）。对于助手数据表，这里强烈建立**不要**使用模型，而是一个实际的数据表：

```python
tags = db.Table('tags',
        db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
        db.Column('page_id', db.Integer, db.ForeignKey('page.id'))
        )

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tags = db.relationship('Tag', secondary=tags,
            backref=backref('pages', lazy='dynamic'))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
```

这里将*Page.tags*配置为一个装入后的标签清单，因为这里不期望一个页面有太多标签。而每个标签下的页面（*Tag.pages*）则是一个动态的backref。如上面提到的一样，这意味着将获取到一个查询对象，随后可对该查询对象进行自主的选择。

##数据的选择、插入和删除操作

现在已经完成了模型的声明，是时间从数据库进行数据的查询了。这里是使用到快速起步章节中的模型定义（the model definitions）。

###插入记录

在能查询到数据前，务必要插入一些数据。所有模型都应具备一个构造器，所以如果忘记了这个构造器，那么要记得添加一个进去。构造器是仅供SQLAlchemy的用户使用的，其内部并不会用到，所以如何定义构造器完全是代码编写者自己决定的。

将数据插入到数据库分三步：

1. 创建相关Python对象

2. 将其加入到数据库会话

3. 提交会话

此会话并非Flask的会话，而是Flask-SQLAlchemy的会话。其本质上是一个数据库事务的加强版本（it is essentially a beefed up version of a database transaction）。下面是如何使用的示例：

```python
>>> from relations import User
>>> from relations import db
>>> her = User('Feng Xiaochun', 'xchunf@gmail.com')
>>> db.session.add(her)
>>> db.session.commit()
```

那么，这并不那么难吧。这里发生了什么呢？在将该对象加入到数据库会话前，SQLAlchemy基本上没有将其加入到事务。那是很好的，因为到这里仍然可以丢弃变更。比如在某个页面建立文章时，只打算将该文章传递给模版做预览渲染，而不需要存入到数据库时。

这里的`add()`函数调用随后加入了该对象。其将执行一条数据库的*INSERT*语句，但因为该事务仍未被提交，所以不会立即获取到一个ID。如完成了提交，则用户就有了一个ID：

```python
>>>her.id
4
```


###删除记录

删除记录与此非常类似，只不过使用`delete()`方法，而不是`add()`方法：

```python
>>> db.session.delete(me)
>>> db.session.commit()
```

###查询记录

那么怎样从数据库取回数据呢？为此Flask-SQLAlchemy提供了一个`Model`类上的`query`属性。在访问该属性时，就会取回一个新的包含所有记录的查询对象（a query object）。随后就可以使用诸如`filter()`等的方法，在启动使用`all()`或`first()`方法进行选择前，对这些记录进行过滤。而如打算使用主键进行记录查询，则要使用`get()`方法。

随后的查询假设数据库中有着一下数据条目：

| id        | username      | email             |
| :-------: | :------:      | :----------:      |
| 1         | admin         | admin@example.com |
| 2         | peter         | peter@example.org |
| 3         | guest         | guest@example.com |


通过username获取到一名用户：

```python
>>> peter = User.query.filter_by(username='peter').first()
>>> peter.id
1
>>> peter.email
u'peter@example.org'
```

与上面一样，不过要查找一个不存在的username，将给出*None*：

```python
>>> missing = User.query.filter_by(username='missing').first()
>>> missing is None
True
```

通过稍加复杂的表达式，来选择出一批用户：

```python
>>> User.query.filter(User.email.endswith('@example.com')).all()
[<User u'admin'>, <User u'guest'>]
```

按照某种条件对用户进行排序：

```python
>>> User.query.order_by(User.username).all() #修正
[<User u'admin'>, <User u'guest'>, <User u'peter'>]
```

限制用户数：

```python
>>> User.query.limit(1).all()
[<User u'admin'>]
```

通过主键获取到某名用户：

```python
>>> User.query.get(1)
<User u'admin'>
```

###视图中的记录查询

如编写一个Flask视图函数，那么为一些缺失的数据条目返回404错误，是很常见的。因为这是一种十分常见的做法，Flask-SQLAlchemy专为此目的提供了一个助手函数。这种情况下可使用`get_or_404()`而不是`get()`函数，以及使用`first_or_404()`而不是`first()`函数。这都会生成404错误而不是返回`None`：

```python
@app.route('/user/<username>')
def show_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('show_user.html', user=user)
```

##使用Binds功能实现多个数据库

从0.12版本的Flask-SQLAlchemy开始，就可以连接到多个数据库了。为达到连接多个数据库的目的，Flask-SQLAlchemy将SQLAlchemy预配置为支持多个“binds”。

那么什么是binds呢？在SQLAlchemy中讲到的一个bind，是某种可以执行SQL语句，且通常是一个连接或引擎。在Flask-SQLAlchemy中，binds就总是指的在场景背后自动创建出的引擎了。创建出的每个这些引擎，随后都被关联上一个简短的键（就是bind键）。该键随后又在模型声明时被用于将某个模型关联到特定于该键的引擎（What are binds? In SQLAlchemy speak a bind is something that can execute SQL statements and is usually a connection or engine. In Flask-SQLAlchemy binds are always engines that are created for you automatically behind the scences. Each of these engines is then associated with a short key(the bind key). This key is then used at model declaration time to associate a model with a specific engine）。

如未对某个模型指定bind键，则该模型就使用默认连接（默认连接就是用`SQLALCHEMY_DATABASE_URI`所配置的那个数据库连接）。

###示例配置

下面的配置声明了三个数据库连接。特殊的默认连接，以及另外两个名为*users*（用于存储用户数据）及名为*appmeta*（该数据库引擎连接到一个sqlite数据库，用于对一些应用内部提供的一些数据只读操作）：

```python
SQLALCHEMY_DATABASE_URI = 'postgres://localhost/main'
SQLALCHEMY_BINDS = {
    'users':        'mysqldb://localhost/users',
    'appmeta':      'sqlite:////path/to/appmeta.db'
}
```

###数据表的建立和丢弃

默认下[`create_all()`](http://flask-sqlalchemy.pocoo.org/2.1/api/#flask.ext.sqlalchemy.SQLAlchemy.create_all)及[`drop_all()`](http://flask-sqlalchemy.pocoo.org/2.1/api/#flask.ext.sqlalchemy.SQLAlchemy.drop_all)方法会在所有声明的binds上进行操作，包括默认数据库引擎。此行为可通过提供*bind*参数，进行定制。既可给该参数一个单独的bind名称，也可给它`'__all__'`以表示所有的binds，还可以给其一个binds的清单。而默认的bind(`SQLALCHEMY_DATABASE_URI`)则名为*None*:

```python
>>> db.create_all()
>>> db.create_all(bind=['users'])
>>> db.create_all(bind='appmeta')
>>> db.drop_all(bind=None)
```

###对binds的引用，Referring to Binds

在声明某个模型时，可通过使用内建的`__bind_key__`属性，来指定其bind：

```python
class User(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
```

在Flask-SQLAlchemy内部，该bind键是以`'bind_key'`，存储在该数据表的*info*字典中的。知道这点，对于打算直接创建一个数据表对象来说是很重要的，因为必须把bind键放在那里（在建立多对多关系时，需要直接创建数据表）：

```python
user_favorites = db.Table('user_favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('message_id', db.Integer, db.ForeignKey('message.id')),
    info={'bind_key': 'users'}
)
```

如已在模型中指定了*__bind_key__*，就可以惯常方式，使用这些模型了。该模型将连接到其所指定的数据库连接。


##信号发射的支持，Singalling Support

要在数据变更提交到数据库之前或之后收到提示，就要连接到下面的这些信号。只有在配置中开启了`SQLALCHEMY_TRACK_MODIFICATIONS`选项后，才会追踪这些变更。

*这是0.10版本中新引入的特性*。

*2.1版本中的修改*：`before_models_committed`已可被正确地触发。

*自2.1版本起弃用的特性*：在未来的版本中此特性将被关闭。


##API，编程接口
