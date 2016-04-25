打算要使用Python和Flask框架开发一个应用了？这里就可以通过例子进行学习。在本教程中，将建立一个简单的微博客应用（a simple microblogging application）。其只支持一个用户，且只能创建文本条目，同时没有源或评论（no feeds or comments），但仍旧具备了对于起步所需的那些特性。这里将使用到Flask，并将SQLite作为数据库（SQLite是Python自带的），因此而不需要其它的库了。

如需完整的事先写好的代码或作对比用途，可下载到[example source](https://github.com/pallets/flask/tree/master/examples/flaskr/)。

##关于Flaskr

这里将这个博客应用叫做Flaskr，但取一个不那么Web-2.0式的（Web-2.0-ish）名字也都是可以的；）这里基本上要该应用完成下面的功能：

1. 令到用户可以使用在配置文件中指定的凭据进行登入登出操作。只支持一个用户。

2. 在用户登入后，就可以加入包含了一个文本标题及内容的一些HTML的新文章到页面。并未对这些HTML进行清理（sanitized），因为这里是信任用户的。

3. 在首页以新旧顺序显示所有的文章（最新的在顶部），同时用户如已登入，就可以在首页加入新文章。

这里将直接使用SQLite3，因为对于这样大小的应用，其已足够好了。对于大型应用，则使用到SQLAlchemy就很有必要，因为其处理数据库连接的方式更为明智，允许同时利用不同的关系型数据库等特性。而如果数据更适合于NoSQL数据库，就要考虑使用一些流行的此类数据库了。

下面是该应用最终的一个屏幕截图：

![flaskr](./images/flaskr.png)

##步骤0：建立各个文件夹

在起步前，要建立该应用所需的文件夹：

```bash
/flaskr
    /static
    /templates
```

该`flaskr`文件夹并不是一个Python包，而仅是一个要放入一些文件的地方。随后将放入数据库图式及主模块（database schema as well as main module）到此文件夹。该应用是按下面地方式完成的。位于`static`文件夹中的文件，通过HTTP投递到应用的用户。CSS及JavaScript文件是放在这里的。而在`templates`文件夹中，Flask将查找Jinja2模版。本教程后面所创建的模版，都将放在这里。


##步骤1：数据库图式

首先，这里要创建出数据库图式。本应用只需一个简单的表，同时只打算支持SQLite，所以数据库图式的创建是相当容易的。只需将下面的内容放入到刚才所建立的*flaskr*文件夹下的一个名为*schema.sql*中：

```sql
drop table if exists entries;
create table entries (
    id integer primary key autoincrement,
    title text not null,
    'text' text not null
);
```

该图式又一个名为`entries`的单一表构成。该表中每行记录都有一个`id`、`title`和`text`。`id`是一个自动增加的整数，同时作为一个主键（a primary key），其它两个字段都是非空的字符串（strings that must not be null）。

##步骤2：应用的设置代码，Application Setup Code

现在已有了数据库图式，就可以建立该应用的模块了。这里称其为`flaskr.py`。将其放在`flaskr`文件夹中。这里以加入一些所需库的导入，及配置部分的添加开始。对于小型应用，是可以将其配置直接放到模块中的，当这里不会这样做。因此一种更为明晰的方案是建立一个独立的`.ini`或`.py`文件，然后载入该文件从而导入里面的各种值。

首先，添加`flaskr.py`中的导入库或模块：

```python
#all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
        render_template, flash
```

接着，就可以建立实际的应用，并对其应用来自同一文件`flaskr.py`中的配置，进行初始化：

```python
#create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

#Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
    ))

app.config.from_envvar('FLASKR_SETTING', silent=True)
```

>关于数据库路径：

>操作系统掌握着各个进程的当前工作目录的概念（Operating systems know the concept of a current working directory for each process）。但不幸的是，在web应用中是不能信任操作系统所提供的进程当前目录的，因为在同一进程中可能有多个的应用。

>因此，`app.root_path`这个属性就可用于取得到该应用的路径。于`os.path`模块已到，就可以方便地找到一些文件。在本例中，是将数据库放到应用模块隔壁的。

>而对于真实世界的应用，建议使用[Instance Folders](http://flask.readthedocs.org/en/latest/config/#instance-folders)。

通常，装入一个独立的、特定于环境的配置文件，是一个不错地主意。Flask允许导入多个的配置文件，而其将使用到定义在最后导入的配置文件中的设置项。这带来了鲁棒的配置设置。[`from_envvar()`](http://flask.readthedocs.org/en/latest/api/#flask.Config.from_envvar)方法可有助于达到这个目的。

```python
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
```

此时只需简单地将环境变量`FLASKR_SETTINGS`定义为指向到一个要装入的配置文件（points to a config file）即可。该静默开关（the silent switch）只是告诉Flask， 在没有设置此环境键时不要抱怨（just tells Flask to not complain if no such environment key is set）。

除此之外，可在应用的配置对象（the config object）上应用[`from_object()`](http://flask.readthedocs.org/en/latest/api/#flask.Config.from_object)方法，而为其提供一个模块的导入名称。Flask随后将对那个模块中的变量进行初始化。请注意在所有情况下，都只有那些大写的变量名称才会加以考虑。

`SECRET_KEY`用于保持客户端sessions的安全。要精心选择该密钥并令其难于猜中而尽可能的复杂。

下面还将加入一个令到与指定数据库容易地连接起来的一个方法。该方法可用于开启一个在客户端请求下的连接，也可用于开启一个自Python shell或脚本发起的到数据库的连接。该方法在后面会经常用到。这里经由SQLite建立了一个简单的数据库连接，并接着告诉SQLite使用[`sqlite3.Row`](https://docs.python.org/dev/library/sqlite3.html#sqlite3.Row)对象，来表示表格中的行。这样做允许将这些行作为字典，而不是元组进行对待。

```python
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
```

有了这个方法后，就可以无问题地启动该应用了。使用下面的命令启动该应用：

```bash
flask --app=flaskr --debug run
```

`--debug`标志（the `--debug` flag）开启或关闭交互式调试器。*在生产系统中绝对不要激活调试模式*，因为那将用户在服务器上执行代码！

将看到一条告诉你服务器已启动，并带有可以访问到该应用的地址的消息。

当在浏览器中前往到服务器时，将收到一个404错误，因为这里还没有任何的视图。稍后将着重讲解视图，但首先要让数据库工作起来。

>外部可见的服务器：

>想要服务器可以公开访问？请查阅[externally visible server](http://flask.readthedocs.org/en/latest/quickstart/#public-server)部分，获取更多信息。


##关于数据库连接，Database Connections

前面已经创建了一个用于建立数据库连接的函数*connect_db*，但仅有这个函数，是没什么用的。任何情况下，数据库连接的建立和关闭总是效率极低的，因此要让数据库连接保持一个较长的时间。而因为数据库连接都封装了一个事务，所以还需要在使用一次连接时，每次只有一个请求。那么怎么时与Flask来巧妙地达到这个目的呢？

这里就是**应用上下文**发挥作用的地方（this is where **the application context** comes to play），所以我们从那里开始。

Flask提供了两种上下文（two contexts）：应用上下文和请求上下文（the application context and the request context）。眼下只需知道有一些特别的变量会用到这些上下文。比如,`request`变量就是与当前请求相关的请求对象，而`g`则是一个与当前应用上下文相关的通用目的变量。稍后会对此有更深入的讨论。

目前，需要了解的就只是可在`g`对象上安全地保存信息。

那么该什么时候使用这个`g`对象呢？为了使用到该对象，可构造一个助手函数（a helper function）。在初次调用该函数是，其会为当前上下文建立一个数据库连接，而后续调用都会返回该已建立好的连接：

```python
def get_db():
    """Opens a new database connection if there is none yet for the
    current applicaiton context."""

    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()

    return g.sqlite_db
```

那么现在已经知道如何进行数据库连接了，但又该如何正确地断开连接呢？为此，Flask提供了[`teardown_appcontext()`](http://flask.readthedocs.org/en/latest/api/#flask.Flask.teardown_appcontext)这一修饰器。在每次应用上下文拆除时，其都将被执行：

```python
@app.teardown_appcontext
def close_db(error):
    """Close the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
```

由`teardown_appcontext()`所标记的那些函数，在每次应用上下文拆除时，都会被调用到。这意味着什么呢？从根本上讲，该应用上下文在数据库访问请求发生前就被创建出来，然后在请求完成后就被破坏掉（拆除）。有两个原因会导致应用上下文的拆除：既会在进展顺利（此时那个错误参数将是`None`）时，也会在有例外发生（an exception happened）时，而在列外中的错误，将传递给那个拆除函数。

还不知道这些上下文是什么意思？请看看[The Application Context](http://flask.readthedocs.org/en/latest/appcontext/#app-context)文档来掌握更多信息。

>提示：

>要把这些代码放在哪里呢？

>如一直在学习此教程，那么可能想知道应该将此步骤及以后的代码放到何处。合理的地方就是将这些模块级别的函数放在一起，并将新的`get_db`及`close_db`函数放在已有的`connect_db`函数下面（照教程这样一行接一行的写）。

>如需要点时间来找到顺序，就看看[example source](https://github.com/pallets/flask/tree/master/examples/flaskr/)是怎么组织代码的吧。在Flask中，可将所有应用代码都放在一个Python模块中。但不一定非得要这么做，特别是在[应用变得越来越大时](http://flask.readthedocs.org/en/latest/patterns/packages/#larger-applications)，这么做并不好。


##步骤4：数据库的建立

如同先前指出的那样，Flaskr是一个数据库驱动的应用，同时更准确地讲，其是一个由关系型数据库系统支持的应用。这样的数据库系统是需要一个图式来告诉它们如何存储信息的。在首次启动数据库服务器前，建立那个图式是重要的。

这样的一个图式可通过将`schema.sql`文件经由管道方式提供给*sqlite3*命令，像下面这样创建出来：

```bash
sqlite3 /tmp/flaskr.db < schema.sql
```

此方式不好的地方在于其需要安装上`sqlite3`命令，而在所有系统上这都是不必要的。同时该命令还需要将路径提供给数据库，那会引入一些错误。那么为应用加入一个初始化数据库的函数，就是一个不错的注意了。

为了完成这个操作，可创建一个函数，并将其调用到初始化数据库的**flask**命令中（hook it into the **flask** command that initializes the database）。这里先给出其代码。只需将下面的函数加入到`flaskr.py`中的*connect_db*函数后面：

```python
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print 'Initialized the database.'
```

修饰器`app.cli.command()`在**flask**脚本上注册一个新的命令。在该命令执行时，Flask就会自动建立一个绑定到正确的应用的应用上下文。有了这个函数，就可以访问到`flask.g`对象和其它一些期望的东西。在*flask*脚本结束时，该应用上下文就会被拆除，同时该数据库连接也会被释放出来。

但这里想要有一个真实的用于初始化该数据库的函数（we want to keep an actual function around that initializes the database），这样就能够容易地建立后面会用到的单元测试中的数据库了。（更多有关信息，请参见[Testing Flask Applications](http://flask.readthedocs.org/en/latest/testing/#testing)）

这里应用对象的`open_resource()`方法，是一个可以打开该应用所提供的资源的、方便的帮助函数。该函数从资源位置（也就是`flaskr`文件夹），打开一个文件，并允许读取到该文件。这里使用此帮助函数时为了在该数据库连接上执行一个SQL脚本。

由SQLite所提供的连接对象可给出一个cursor对象。在那个cursor上，有着一个执行一套完整脚本的方法。最终，就只须提交更改（commit the changes）就可以了。SQLite3和其它一些事务性数据库在没有显式地告诉它们要提交修改前，都不会进行修改的提交。

现在，就可以使用该**flask**脚本，来建立一个数据库了。

```bash
$flask --app=flaskr initdb
Initialized the database.
```

>故障排除：

>如在本教程的后面收到一个指出表不存在的列外告警，就要看看有没有执行这个`initdb`命令，以及表的名称是对的（其是单数还是复数，比如）。


##步骤5：关于视图函数

既然数据库连接已经可用了，那么这里就要开始编写那些视图函数了。我们需要4个这样的视图函数：

###显示文章的视图

该视图将存储在数据库中的文章都显示出来。其监听着该应用的根，并将从数据库选用标题和内容。而带有最高id（也就是最新的文章）的文章将位处页面顶部。同时从cursor返回的那些行，看起来有些像是一些字典，因为这里使用了[sqlite.Row](https://docs.python.org/dev/library/sqlite3.html#sqlite3.Row)这个行工厂（row factory）。

该视图函数将把这些文章传递给`show_entries.html`模版并返回一个渲染后的`show_entries.html`：

```python
@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)
```

###添加新文章的视图

该视图则是令到用户在登入后可以添加新文章。其只对`POST`请求进行响应；真实的表单是显示在*show_entries*页面上的。如所有事情都正确运作，就会将一条信息消息[`flash()`](http://flask.readthedocs.org/en/latest/api/#flask.flash)到下一次请求，并重定向回*show_entries*页面：

```python
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
            [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))
```

请注意这里检查了用户是登入了的（session中有这个*logged_in*键，同时其值为`True`）。

>安装注意事项：

>请确保在构建SQL语句时，使用的是问号，如在上面的示例那样。否则，应用在使用字符串格式化方式构建SQL语句时，将易受SQL注入攻击。参见[Using SQLite3 with Flask](http://flask.readthedocs.org/en/latest/patterns/sqlite3/#sqlite3)得到更多信息。


###登入和登出视图

这些函数用于用户的登入和登出。登入函数将用户名和口令，与配置中的进行查验，并设置好session的*logged_in*键值。如用户成功登入，就将该键值设为`True`，并将用户重定向到*show_entries*页面。此外，还将刷新一条通知用户其已成功登入的消息（a message is flashed that informs the user that he/she was logged in successfully）。而如果发生错误，就通知到模版，同时再次询问用户的用户名和口令：

```python
@app.route('/login', method=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You ware logged in')
            return redirect(url_for('show_entries'))
        return render_template('login.html', error=error)
```

而另外的*logout*函数，会再次从session中移除掉那个键值。这里用了一个巧妙的花招：如使用该字典的[`pop()`](https://docs.python.org/dev/library/stdtypes.html#dict.pop)方法，并传递给该方法第二个参数（默认的），那么如果该字典中有这个键值，该方法就会从该字典删除掉那个键值，而如果该键值不存在，该方法就什么也不会做。这么做是大有裨益的，因为现在无须去检查用户是否已登入。

```python
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
```

请注意，将口令以明文形式进行存储不是好主意。如碰巧有人能够访问到数据库时，总是想要保护好登录凭据的。一种方式就是使用Werkzeug中的一些安全助手函数（Security Helpers from Werkzeug），将口令进行散列化处理。不过本教程重点时演示Flask的基础，所以为简化起见，这里使用了明文的口令。


##步骤6：模版

现在应开始建立模版了。如果此时去请求那些URLs，只会收到Flask无法找到模版的例外信息（an exception that Flask cannot find the templates）。Flask中的模版使用了Jinja2的语法，并默认开启了自动转换。这就是说除非在代码中对某个值使用[Markup](http://flask.readthedocs.org/en/latest/api/#flask.Markup)，或者模版中的`|safe`过滤器进行了标记，Jinja2都会将那些特殊字符，比如`<`或`>`，转换成其对应的XML表示形式。

这里还将用到模版继承，从而使得在所有页面中重用到站点的布局成为可能。

请将下面这些模版，放入到`templates`文件夹。

###layout.html

此模版包含了一个HTML骨架，头部及一个登入的链接（或是在用户已登入时到登出的链接）。同时还显示出可用的刷新消息（also displays the flashed messages if there are any）。块`{% block body %}`可在子模版中使用同样名称的块`(body)`进行替换。

在模版中，[session](http://flask.readthedocs.org/en/latest/api/#flask.session)字典也是可以使用的，可使用其判断用户是否已登入。请注意在Jinja中，对那些缺失的属性值，以及对象/字典中的项目，是可以访问到的，而正是这些属性和项目，才令到下面的代码能够运行起来，甚至在session中没有`logged_in`键值都行。

```html
<!doctype html>

<title>Flaskr</title>

<link rel='stylesheet' type='text/css' href="{{ url_for('static', filename='style.css') }}" />
<div class='page'>
        <h1>Flaskr</h1>
        <div class='metanav'>
                {% if not session.logged_in %}
                    <a href="{% url_for('login') %}">log in</a>
                {% else %}
                    <a href="{% url_for('logout') %}">log out</a>
                {% endif %}
        </div>
        {% for message in get_flashed_messages() %}
        <div>{{ message }}</div>
        {% endfor %}
        {% block body %}{% endblock %}
</div>
```

###show_entries.html

此模版对上面的`layout.html`模版进行扩展，以显示那些博客文章。请注意这里的`for`循环对通过[`render_template()`](http://flask.readthedocs.org/en/latest/api/#flask.render_template)函数传入的那些文章，进行遍历。这里还告诉表单提交到*add_entry*函数，并采用`POST`作为HTTP方法：

```html
{% extends "layout.html" %}

{% block body %}
    {% if session.logged_in %}
        <form action="{% url_for('add_entry') %}" method='post' class='add-entry'>
            <dl>
                <dt>Title: </dt>
                <dd><input type='text' size='30' name='title' /></dd>
                <dt>Text:</dt>
                <dd><textarea name='text' rows='5' cols='40'></textarea></dd>
                <dd><input type='submit' value='Share' /></dd>
            </dl>
        </form>
    {% endif %}

    <ul class='entries'>
        {% for entry in entries %}
            <li><h2>{{ entry.title }}</h2>{{ entry.text|safe }}</li>
        {% else %}
            <li><em>Unbelievable, No entries here so far</em></li>
        {% endfor %}
    </ul>

{% endblock %}
```

###login.html

这是登入模版，其只简单地显示一个允许用户登入的表单。

```html
{% extends "layout.html" %}

{% block body %}

    <h2>Login</h2>

    {% if error %}<p class='error'><strong>Error: </strong>{{ error }}</p>{% endif %}

    <form action="{{ url_for('login') }}" method='post'>
            <dl>
                <dt>Username: </dt>
                <dd><input type='text' name='username' /></dd>
                <dt>Password: </dt>
                <dd><input type='password' name='password' /></dd>
                <dd><input type='submit' value='Login' /></dd>
            </dl> 
    </form>

{% endblock %}
```


##加入样式

现在所有东西都有了，是时候将一些样式加入到应用中了。只需在之前建立的`static`文件夹中创建一个名为`style.css`的样式表：

```css3
body {
    font-family: sans-serif; 
    background: #eee;
}
a, h1, h2 {
    color: #377ba8;
}
h1, h2 {
    font-family: 'Georgia', serif; 
    margin: 0;
}
h1 {
    border-bottom: 2px solid #eee;
}
h2 {
    font-size: 1.2em;
}

.page {
    margin: 2em auto;
    width: 35em;
    border: 5px solid #ccc;
    padding: 0.8em;
    background: white;
}

.entries {
    list-style: none;
    margin: 0;
    padding: 0;
}

.entries li {
    margin: 0.8em 1.2em;
}

.entries li h2 {
    margin-left: -1em;
}

.add-entry {
    font-size: 0.9em;
    border-bottom: 1px solid #ccc;
}

.add-entry dl {
    font-weight: bold;
}

.metanav {
    text-align: right;
    font-size: 0.8em;
    padding: 0.3em;
    margin-bottom: 1em;
    background: #fafafa;
}

.flash {
    background: #cee5f5;
    padding: 0.5em;
    border: 1px solid #aacbe2;
}

.error {
    background: #f0d6d6;
    padding: 0.5em;
}
```

##附加内容：测试该应用

现在已经完成了这个应用，所有东西都会如预期那样运行，而加入自动测试，则是简化今后对其进行修改的好主意。上面这个应用是作为[Testing Flask Application]章节中进行单元测试时的基本示例的。在那里可以看到测试Flask应用是比较容易的。


