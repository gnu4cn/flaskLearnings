#Quickstart

要开始了，很鸡冻吧？此页面给了一个对Flask的不错的介绍。其假定已安装好Flask。如还没有，就请参见[Installation](./02_installation.md)章节。

##最小应用

一个最小的应用，看起来是这样的：

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
```

那么这些代码做了什么呢？

    1. 首先我们导入了类[**`Flask`**](http://flask.readthedocs.org/en/latest/api/#flask.Flask)。此类的一个实例，就将成为我们的WSGI应用。

    2. 接着，创建了类Flask的一个实例。实例构造函数的第一个参数，就是应用的模块或包的名称（the name of the application‘s module or package）。如只要到单一模块（如同本例中这样），就可以使用*`__name__`*作为该参数，因为根据其作为应用启动，还是作为一个模块导入两种情况的不同，该名称参数会有所不同（可以是‘`__main__`’或实际用到的导入名称）。该参数是必须的，有了该参数，Flask才知道去哪里查找相应的模版、静态文件等。关于此实例构造函数的参数，请参阅[Flask](http://flask.readthedocs.org/en/latest/api/#flask.Flask)文档。

    3. 这里接着使用[`route()`](http://flask.readthedocs.org/en/latest/api/#flask.Flask.route)修饰器，告诉Flask激发应用的是什么URL。

    4. 为函数赋予了一个名称，同时也用于生成该特定函数的URLs，并返回打算显示在用户浏览器中的消息。

将这些代码保存为`hello.py`并在Python解释器下运行。

```bash
$flask -a hello run
* Running on http://127.0.0.1:5000/
```

或者替代的：

```bash
$python -m flask -a hello run
* Running on http://127.0.0.1:5000/
```

这将启动一个非常简单的内建服务器，该服务器对于测试来说是足够好的，但大概不会在生产中使用。对于生产部署选项，请参阅[Deployment Options](http://flask.readthedocs.org/en/latest/deploying/#deployment)。

那么现在打开[http://localhost:5000/](http://localhost:5000/)，就可以看到hello world问候语了。

###外部可见的服务器

在运行该服务器时，会注意到该服务器仅能从自己的计算机访问到，而不能从网络中的其它计算机进行访问。这时默认的，因为在调试模式下，应用的用户可执行你的计算机上任意的Python代码。

如关闭了调试器，或是信任网络上的用户，就可以通过简单地加入`--host=0.0.0.0`到命令行，来开启该服务器的公开访问：

```bash
$flask -a hello run --host=0.0.0.0
```

##如果服务器未能启动，该怎么做

如果`python -m flask`运行失败或`flask`不存在，则造成此现象的原因可能有好几种。首先要看看错误消息。

###老版本的Flask

低于1.0版本的Flask采用了多种不同方式来启动应用。也就是说，命令`flask`与`python -m flask`都没有。那么此时有两个办法，要么升级到较新版本的Flask，要么看看[Development Server](http://flask.readthedocs.org/en/latest/server/#server)文档，找一下运行服务器的替代方法。

###Python版本低于了2.7

如果你的Python版本低于2.7，命令`python -m flask`也不能运行。此时可以使用`flask`或`python -m flask.cli`作为替代办法。这是因为在2.7之前版本的Python不允许将包作为可执行模块运作。更多信息参见[Command Line Interface](http://flask.readthedocs.org/en/latest/cli/#cli)。

##无效的导入名称

`flask`的`-a`参数是要导入模块的名称。如果该模块没有正确命名，那么在启动时（或在浏览器中前往到该应用时开启了调试）就会收到导入错误提示。该错误提示告诉你程序要导入的模块及为何会导入失败。

最常见的原因就是拼写错误，或者根本就没有创建一个`app`对象。

##关于调试模式

（只想了解错误日志和栈跟踪？请移步[Application Errors](http://flask.readthedocs.org/en/latest/errorhandling/#application-errors)）

`flask`脚本对于启动一个本地开发服务器来说是不错的，但在每次对代码进行了修改后，都必须重启该服务器。那就不是很好了，而Flask却可以做得更好。在开启了调试支持后，服务器在代码发生改变时，可以侦测到而自动重启一下，同时在出现错误时，还将提供一个有用的调试器。

开启调试模式的方式有很多，最为显见的就是`flask`命令的`--debug`参数：

```bash
flask --debug -a hello run
```

此命令完成下面这些事：

    1. 激活调试器

    2. 激活自动重载器

    3. 开启该Flask应用的调试模式

在[Development Server](http://flask.readthedocs.org/en/latest/server/#server)文档中有讲到更多的参数。

##注意事项

>尽管在派生环境中（in forking environment）交互是调试器是无法工作的（这令到在生产服务器上不可能用上调试器），但仍然允许执行任意代码。这就导致调试器成为一个重大安全隐患，因此**在生产机器上绝对不要使用调试模式**。

下面是一个运行中的调试器屏幕截图：

![调试器屏幕截图](./images/debugger.png)

想看看别的调试器？请参阅[Working with Debuggers](http://flask.readthedocs.org/en/latest/errorhandling/#working-with-debuggers)

##路由，Routing

现代web应用都有着优美的URLs。这有助于人们记住这些URLs，对于从慢速的网络连接的移动设备使用到的那些应用，这尤其好用。如用户可以直接前往到所需页面，而无须点击首页，那么就更会喜欢上这个页面并再次来到这个页面。

如同上面看到的那样，`route()`修饰器用于将一个函数绑定到一个URL。这里有一些基础示例：

```python
@app.route('/')
def index():
    return 'Index Page\n'

@app.route('/hello')
def hello():
    return 'Hello World!\n'
```

不过关于路由还有很多的东西！你可以令到URL的一些部分成为动态的，同时给某个函数加入多条规则。

###各种变量规则

要将一些变量部分加入到URL，可将这些特殊部分标记为`<variable_name>`。这样的一个部分就作为一个关键字参数，传递给函数。其中可通过指定`<converter:variable_name>`规则，使用一个可选的转换器（a converter）。下面有一些不错的示例：

```python
@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s\n' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post: %d\n' % post_id
```

以下是一些存在的转换器：

| 转换器        | 用法                                      |
| --------      | :----------:                              |
| *string*      | 接受任何不带有斜杠的文本（默认的转换器）  |
| *int*         | 接受整数                                  |
| *float*       | 像是int但只接受浮点数值                   |
| *path*        | 像默认转换器，但也接受斜杠                |
| *any*         | 接受上面四种类型值之一种                  |
| *uuid*        | 仅接受UUID字串                            |

>##关于UUID：

>UUID含义是通用唯一识别码 (Universally Unique Identifier)，这 是一个软件建构的标准，也是被开源软件基金会 (Open Software Foundation, OSF) 的组织应用在分布式计算环境 (Distributed Computing Environment, DCE) 领域的一部分。

>###作用

>UUID 的目的，是让分布式系统中的所有元素，都能有唯一的辨识资讯，而不需要透过中央控制端来做辨识资讯的指定。如此一来，每个人都可以建立不与其它人冲突的 UUID。在这样的情况下，就不需考虑数据库建立时的名称重复问题。目前最广泛应用的 UUID，即是微软的 Microsoft‘s Globally Unique Identifiers (GUIDs)，而其他重要的应用，则有 Linux ext2/ext3 档案系统、LUKS 加密分割区、GNOME、KDE、Mac OS X 等等。

>###组成

>UUID是指在一台机器上生成的数字，它保证对在同一时空中的所有机器都是唯一的。通常平台会提供生成的API。按照开放软件基金会(OSF)制定的标准计算，用到了以太网卡地址、纳秒级时间、芯片ID码和许多可能的数字

>UUID由以下几部分的组合：

>1. 当前日期和时间，UUID的第一个部分与时间有关，如果你在生成一个UUID之后，过几秒又生成一个UUID，则第一个部分不同，其余相同。

>2. 时钟序列。

>3. 全局唯一的IEEE机器识别号，如果有网卡，从网卡MAC地址获得，没有网卡以其他方式获得。

>UUID的唯一缺陷在于生成的结果串会比较长。关于UUID这个标准使用最普遍的是微软的GUID(Globals Unique Identifiers)。在ColdFusion中可以用CreateUUID()函数很简单地生成UUID，其格式为：xxxxxxxx-xxxx- xxxx-xxxxxxxxxxxxxxxx(8-4-4-16)，其中每个 x 是 0-9 或 a-f 范围内的一个十六进制的数字。而标准的UUID格式为：xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx (8-4-4-4-12)，可以从cflib 下载CreateGUID() UDF进行转换。

>###应用

>使用UUID的好处在分布式的软件系统中（比如：DCE/RPC, COM+,CORBA）就能体现出来，它能保证每个节点所生成的标识都不会重复，并且随着WEB服务等整合技术的发展，UUID的优势将更加明显。根据使用的特定机制，UUID不仅需要保证是彼此不相同的，或者最少也是与公元3400年之前其他任何生成的通用唯一标识符有非常大的区别。
    
>通用唯一标识符还可以用来指向大多数的可能的物体。微软和其他一些软件公司都倾向使用全球唯一标识符（GUID），这也是通用唯一标识符的一种类型，可用来指向组建对象模块对象和其他的软件组件。第一个通用唯一标识符是在网络计算机系统（NCS）中创建，并且随后成为开放软件基金会（OSF）的分布式计算环境（DCE）的组件。

##唯一URLs/重定向行为

Flask的URL规则，是基于Werkzeug的路由模块的。该模块背后的规则，就是确保在由Apache及其它早期的HTTP服务器所订下的规则基础上，有着漂亮及唯一的URLs。

看看这两个规则：

```python
@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'
```

尽管它们看起来相当类似，但在URL*定义（definition）*中对最后的斜杠的使用是不同的。在第一种情况里，*projects*的规范URL有着一个结束斜杠。从这个意义上讲，其与文件系统上的某个文件夹是类似的。通过不带结束斜杠方式访问该URL，就会导致Flask重定向到有着结束斜杠的规范URL。

在第二种情况下，该URL就没有了那个结束斜杠，这与在类UNIX系统上的一个文件的路径名称很像了。这时如果通过带有结束斜杠方式访问该URL，就会产生一个404“页面未找到（Not Found）”错误。

此行为允许在省略其结束斜杠时，相对URLs（relative URLs）仍能继续工作，从而与Apache及其它服务器的运作保持一致。又同时保持了URLs的唯一性，而这有助于搜索引擎避免两次索引同一页面。

##URL的构建

既然Flask具备匹配URLs的能力，其还能生成URLs吗？当然可以。要给某个特定函数构建一个URL，可以使用[`url_for()`](http://flask.readthedocs.org/en/latest/api/#flask.url_for)函数。该函数接受函数名称作为第一个参数，及一些关键字参数，这些参数与URL规则的变量部分一一对应。未知变量部分则是追加到URL上作为查询参数。这里有一些示例：

```python
>>> from flask import Flask, url_for
>>> app = Flask(__name__)
>>> @app.route('/')
... def index(): pass
... 
>>> @app.route('/login')
... def login(): pass
... 
>>> @app.route('/user/<username>')
... def profile(username): pass
... 
>>> with app.test_request_context():
...     print url_for('index')
...     print url_for('login')
...     print url_for('login', next='/')
...     print url_for('profile', username='John Doe')
... 
/
/login
/login?next=%2F
/user/John%20Doe
```

（这里还用到了[`test_request_context()`](http://flask.readthedocs.org/en/latest/api/#flask.Flask.test_request_context)方法，将在下面讲到。该方法告诉Flask表现得像是在处理一个请求，尽管我们是在一个Python shell中在与其交互。可以看看下面的解释。[Context Locals](http://flask.readthedocs.org/en/latest/quickstart/#context-locals)）。

为什么要使用这个URL逆向函数`url_for()`来构建处URLs，而不是将这些URLs硬编码到模版中呢？有三个这么做的理由：

1. 逆向生成比起硬编码URLs，通常都更具描述性。更重要的是，逆向生成允许你一次完成所有URLs的修改，无须记住在所有地方去修改URLs。

2. 有该方法实现的URL构建，将为你对特殊字符及Unicode的数据进行透明处理，所以就无须手动处理这些字符了。

3. 如应用是放在URL根的外面的（比如，是在`/myapplication`而不是`/`中），此时`url_for()`方法仍将对其正确处理。


##HTTP的那些方法

HTTP（正是web应用所操的协议）在存取URLs时，理解几种不同方法。默认情况下，一个路由只对`GET`请求进行响应，不过这可以通过将*`methods`*参数提供给`route()`修饰器，进行改变。这里有一些示例：

```python
from flask import request

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        do_the_login()
    else:
        show_the_login_form()
```

如果出现了`GET`，则`HEAD`就会自动添加进来。就无须对其进行处理。同时也将确保这些`HEAD`请求按照[HTTP RFC](http://www.ietf.org/rfc/rfc2068.txt)（描述HTTP协议的文档）的要求进行处理，因此可以完成忽略HTTP规格的那一部分。同样，对于Flask 0.6版本，`OPTIONS`也是自动应用的。

你对HTTP方法没有一点了解吗？无需担心，这里对HTTP方法及为何它们是重要的，有一个快速介绍：

HTTP方法（又常成为“动词（the verb）”）告诉服务器，客户端想要用请求的页面*做*什么（the HTTP method tells the server what the client wants to *do* with the requested page）。下面这些方法都是很常见的：

- `GET`
    
    浏览器告诉服务器，仅*获取（get）*存储在该页面的信息并发送该页面。这可能是最常见的方法了。

- `HEAD`

    浏览器告诉服务器获取信息，但仅对*头部（headers）*感兴趣，而不是页面内容。应用被认为是要像处理一个`GET`请求那样处理`HEAD`请求，却不要投送实际内容。在Flask中完全不必手工处理这类请求，而是由所采用的Werkzeug库来处理。

- `POST`

    浏览器告诉服务器，它想要将一些新信息*post*到那个URL，同时服务器务必要确保这些数据得到保存且只保存一次。此方法通常就是HTML表单将数据传输到服务器所用的方法。

- `PUT`

    此方法与`POST`类似，但服务器可能会通过数次的覆写旧数值，而多次触发储存过程。现在你可能认为这没什么用处，但这样做可是有很多好的理由。想象一下在传输过程中连接丢失的情况吧：在此情形下，位于浏览器和服务器之间的系统可能会在不对事情造成破坏的情况下，第二次安全地收到该请求。而采用`POST`则是不会出现这样的情况，因为`POST`务必仅有一次触发。

- `DELETE`

    移除URL所给位置的信息。

- `OPTIONS`

    该方法提供了一种令到客户端找出该URL所支持的哪些方法的快速方式。从Flask 0.6版本开始，此方法已自动应用了。

现在有趣的是在HTML4和XHTML1中的部分了，表单提交到服务器的方法只有两种，分别是`GET`和`POST`。但在JavaScript和将来的HTML标准中，就可以使用其它方法了。最近HTTP已成为相当流行的了，同时浏览器也不再是唯一使用到HTTP的客户端。比如许多版本控制系统（revision control system）也用到HTTP。

##关于静态文件

动态web应用同样是需要静态文件的。那通常都是CSS和JavaScript文件了。理想情况下web服务器配置用于提供这些文件，不过在开发Flask过程中也可以做到。只需在python包中，或在模块隔壁创建一个叫做`static`的文件夹，后者则需在应用的`/static`处可用即可。

要生成这些静态文件的URLs，需使用这个特殊的端点名称`static`（the special `static` endpoint name）：

```python
url_for('static', filename='style.css')
```

该文件必须以`static/style.css`保存在文件系统上。

##关于模版的渲染

自Python中生成HTML并不好玩，实际上因为要保持应用安全而必须完成HTML转换，而是相当麻烦的。为此Flask为你自动配置好了Jinja2模版引擎。

可以使用[`render_template()`](http://flask.readthedocs.org/en/latest/api/#flask.render_template)，来渲染一个模版。只需提供模版的名称，及打算以关键字参数形式传递给模版引擎的一些变量，就行。下面是一个如何渲染模版的简单示例：

```python
from flask import render_template

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
```

Flask将在`templates`文件夹中查找用到的模版。所以如应用是一个模块，那么该文件夹就在那个模块的隔壁，而如该应用是一个包，则那个文件夹就在这个包中：

**第一种情况**：应用是一个模块：

```bash
/application.py
/templates
    /hello.html
```

**第二种情况**：应用作为一个包：

```bash
/application
    /__init__.py
    /templates
        /hello.html
```

从模块就可以看出Jiaja2模版的全部威力。请移步到官方的[Jinja2 模版文档](http://jinja.pocoo.org/docs/templates)获取更多信息。

这里是一个示例模版：

```html
<!doctype html>
<title>Hello from Flask</title>
{% if name %}
    <h1>Hello {{name}}!</h1>
{% else %}
    <h1>Hello, World!</h1>
{% endif %}
```

在模版内部，还可以访问到[`request`](http://flask.readthedocs.org/en/latest/api/#flask.request)、[`session`](http://flask.readthedocs.org/en/latest/api/#flask.session)和[`g`](http://flask.readthedocs.org/en/latest/api/#flask.g)这三个对象，以及函数[`get_flashed_message()`](http://flask.readthedocs.org/en/latest/api/#flask.get_flashed_messages)。

>不知道对象`g`是何物？它是可以为各种需求而在其中保存信息的一个对象，请查阅该对象的文档及[Using SQLite3 with Flask](http://flask.readthedocs.org/en/latest/patterns/sqlite3/#sqlite3)以获取更多信息。

在使用了继承后，模版功能就特别有用了。如想要知道继承的工作原理，请移步[Template Inheritance](http://flask.readthedocs.org/en/latest/patterns/templateinheritance/#template-inheritance)模式文档。简单地说，模版继承可令到在各个页面上保留下一些确定元素成为可能（比如头部、导航栏及底部等元素）。

自动转换是开启的，所以如果*名称（name）*中包含了HTML，就会被自动转换掉。在对某个变量可信、同时知道该变量将是安全的HTML（比如该变量来自于某个将维基标签转换成HTML的模块）时，就可以通过使用`Markup`类，或在模版中使用`|safe`过滤器，将其标记为安全。请参阅Jinja2的文档以得到更多示例。

下面是一个介绍`Markup`类工作原理的示例：

```python
>>> from flask import Markup
>>> Markup('<strong>Hello %s!</strong>' % '<blink>hacker</blink>')
Markup(u'<strong>Hello <blink>hacker</blink>!</strong>')
>>> Markup.escape('<blink>hacker</blink>')
Markup(u'&lt;blink&gt;hacker&lt;/blink&gt;')
>>> Markup('<em>Marked up</em>&raquo;HTML').striptags()
u'Marked up\xbbHTML'
```

*版本0.5中的变化*：不再对所有模版都开启自动转换。下面的文件扩展名会引发自动转换: `.html`、`.htm`、`.xml`及`.xhtml`。从字符串装入的模版将不进行自动转换。

##对请求数据的访问

对于web应用来说，对从客户端发送到服务器的数据进行响应，是最重要的。在Flask中，该信息是由全局的`request`对象提供的。如你有着Python方面的经验，就会想该对象是怎样成为全局性的，以及Flask怎样设法做到线程安全（threadsafe）。答案就是context locals:

###context locals

>内幕信息：

>如你想要掌握context locals工作原理及怎样对context locals应用测试，就请阅读这个小节，否则可以直接忽视。

Flask中的某些对象确实是全局对象，但又不是通常意义上的全局对象。这些对象实际上是到一些对于特定上下文来说属于本地对象的代理（these objects are actually proxies to objects that are local to specific context）。说起来拗口，但实际上是很容易理解的。

请将上下文想象为处理线程（Imagine the context being the handling thread）。进来了一个请求，服务器就决定孵出一个新的线程（或其它什么，所采用的对象具备利用并发系统而不是线程来进行请求处理的能力）。在Flask开始其内部请求处理时，其找出当前活动的线程并将当前应用与WSGI环境与那个上下文（线程）绑定起来。Flask以一种明智的方式完成此操作，因此一个应用可以不中断地调用另一应用。

那么这意味着什么呢？简单地说，你可以完全忽略此过程，除非要完成一些像是单元测试（unit testing）一类的工作。你会注意到由于缺少request对象而导致依赖于某个request对象的代码突然中断了。解决方法就是创建一个request对象，并将其绑定到上下文（线程）。单元测试的最容易方案，就是使用[`test_request_context()`](http://flask.readthedocs.org/en/latest/api/#flask.Flask.test_request_context)上下文管理器。结合使用`with`语句，就可以绑定上一个测试请求，如此就能与其进行互动操作。这里是一个示例：

```python
from flask import request, Flask
app = Flask(__name__)

with app.test_request_context('/hello', method='POST'):
    assert request.path == 'hello'
    assert request.method == 'POST'
```

另一种可能的做法，就是将整个的WSGI环境，传递给[`request_context()`](http://flask.readthedocs.org/en/latest/api/#flask.Flask.request_context)方法：

```python
from flask import request

with app.request_context(environ):
    assert request.method == 'POST'
```

###关于请求对象

在API章节，有着该请求对象的文档，同时这里不会详细介绍该对象（参见[request](http://flask.readthedocs.org/en/latest/api/#flask.request)）。这里是对其一些最常见操作的宽泛概览。首先必须将其从*flask*模块导入该对象：

```python
from flask import request
```

通过使用其`method`属性，可获取其当前的方法。要取得表单数据（在`POST`或`PUT`请求中传输的数据），可使用其`form`属性。这里是上面提到的其两个属性的示例：

```python
from flask import Flask, request
app = Flask(__name__)

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)
```

如*form*属性中的键不存在，会发生什么呢？此时就会产生一个[`KeyError`](https://docs.python.org/dev/library/exceptions.html#KeyError)。可将其作为一个标准的KeyError捕获到，但如不想那样做，就会显示出一个HTTP 400 Bad Request 错误页面。所以很多情况下都不必去处理这个问题。

而要获取到URL中提交的参数（`?key=value`），就可使用`args`属性：

```python
searchword = request.args.get('key', '')
```

这里建议使用*get*来获取URL参数，或通过捕获`KeyError`。因为用户可能会改变URL从而显示给他们一个400 bad request page，那样就不是用户友好的了。

对于完整的HTTP方法和request对象的属性清单，请移步[request](http://flask.readthedocs.org/en/latest/api/#flask.request)文档。

###关于文件上传

通过Flask，可轻易地处理上传的文件。只要确保没有忘记在HTML表单中设置上`enctype="multipart/form-data"`属性就行，否则浏览器将一点也不会发送文件。

上传的文件是存储在内存中或文件系统的某个临时地址的。通过查看request对象的`files`属性，就能访问到这些文件。每个上传的文件都保存在那个字典中。其与标准的Python `file`对象表现一致，不过其还有一个`save()`方法，该方法允许将那个文件存储在服务器的文件系统中。这里是展示其工作原理的一个简单示例：

```python
from flask import request

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/upload_file.txt')
    ...
```

而如想知道该文件于将其上传之前，在客户端上是如何命名的，就可访问request对象的`filename`属性。但请记住该值可以被伪造，所以绝对不要信任那个值。如要使用客户端的文件名来在服务器上存储该文件，就将其经由Werkzeug库提供的`secure_filename()`函数，进行传递：

```python
from flask import request
from werkzeug.utils import secure_filename

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/' + secure_filename(f.filename))
    ...
```

查看[Uploading Files](http://flask.readthedocs.org/en/latest/patterns/fileuploads/#uploading-files)模式，得到一些更好的示例。

###关于cookies

可使用`cookies`属性，来获取[cookies](http://flask.readthedocs.org/en/latest/api/#flask.Request.cookies)。而要设置一些cookies，则可以使用那些response对象的[`set_cookie`](http://flask.readthedocs.org/en/latest/api/#flask.Response.set_cookie)方法。request对象的cookies属性，是一个具有所有客户端传送的cookies的字典。如打算用到会话，不不要直接使用这些cookies，而是使用Flask中，已在cookies之上加入了一些安全措施的[Session](http://flask.readthedocs.org/en/latest/quickstart/#sessions)功能。

读取cookies:

```python
from flask import request

@app.route('/')
def index():
    username = request.cookies.get('username')
    #这里使用了cookies.get(key)而不是cookies[key], 是
    #为了在cookie缺失时不会得到一个KeyError错误
```

存储cookie:

```python
from flask import make_response

@app.route('/')
def index():
    resp = make_response(render_template(...))
    resp.set_cookie('username', 'the username')
    return resp
```

请注意这些cookies是设置在response对象上的。自通常地仅返回自那些视图函数返回的字串以来，Flask都会将它们转换成response对象。如要显式地完成这一转换，就可使用`make_resonse()`函数，然后对其进行修改。

某些时候，可能会在某个response对象尚不存在时就设置一个cookie，这也是可以的，只需通过使用[Deferred Request Callback](http://flask.readthedocs.org/en/latest/patterns/deferredcallbacks/#deferred-callbacks)模式即可。

这方面也可参考[About Responses](http://flask.readthedocs.org/en/latest/quickstart/#about-responses)部分。

###关于重定向和出错

使用[`redirect()`](http://flask.readthedocs.org/en/latest/api/#flask.redirect)函数，将用户重定向到另一断点（endpoint）；而要在早期使用一个错误代码放弃某个请求，就使用[`abort()`](http://flask.readthedocs.org/en/latest/api/#flask.abort)函数：

```python
from flask import abort, redirect, url_for

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    abort(401)
    this_is_never_execute()
```

当然这时一个没有意义的示例，因为用户将自首页被重定向到一个无法访问的（401的意思是拒绝访问）页面，但其显示了这两个方法的原理。

默认下，每个错误代码都将显示为一个黑白的错误页面。而如打算定制错误页面，可以使用[`errorhandler()`](http://flask.readthedocs.org/en/latest/api/#flask.Flask.errorhandler)修饰器：

```python
from flask import render_template

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
```

请注意在`render_template()`调用后面的`404`代码。这告诉Flask那个页面的状态代码应是404，就是说未找到。默认下200被认为翻译成：所有事情都顺利进行。

更多信息，请参阅[Error handlers](http://flask.readthedocs.org/en/latest/errorhandling/#error-handlers)。

###关于响应

来自某个视图函数的返回值，被自动转换成一个response对象。而如过返回值是一个字符串，则就将该字符串作为响应主体，一个`200 OK`的状态码及一个*text/html*的mimetype，而转换成响应对象。在将返回值转换成响应对象时，Flask用到的逻辑如下：

1. 如有返回的是一个正确类型的响应对象，则将直接从视图返回，而不经转换。

2. 如返回的是一个字符串，就用该字符串数据及一些默认参数，转换出一个响应对象。

3. 如返回的是一个元组（tuple），这该元组中的元素就可提供一些额外信息。这样的元组必须是`(response, status, headers)`或`(response, headers)`这样的形式，至少有一个的项目是在元组中的。该*status*值将覆盖掉状态码，同时*headers*可以是一个一些附加头部值的清单或字典。

4. 如上面列举的都没有，Flask就会假定返回值是一个有效的WSGI应用，并将其转换成一个响应对象。

如要在视图内部保有生成的响应对象，就可使用`make_response()`方法。

想象你有着这样一个视图：

```python
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404
```

那么要取得其响应对象以加以修改，就只需将该return表达式用`make_response()`包围起来，然后在返回就可以了：

```python
@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Somethins'] = 'A value'
    return resp
```

###关于会话

除了request对象，还有一个名为`session`的对象，允许你将特定于某个用户的信息，进行跨越请求的存储。该对象是在cookies之上实现的，其对cookies进行了加密签名。这就意味着用户能够看到cookie，却不能对其进行修改，除非他们知道签名的密钥。

要使用sessions, 首先要设置一个密钥。这里是sessions的工作原理：

```python
import os
from flask import Flask, session, redirect, url_for, escape, request

app = Flask(__name__)

@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p><input type=text name=username />
            <p><input type=submit value=Login />
        </form>
        '''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

app.secret_key = os.urandom(24)
```

这里提到的[`escape()`](http://flask.readthedocs.org/en/latest/api/#flask.escape)方法在没有用到模版引擎时，完成对字符串的转换（如同本例中这样）。

>如何生成良好的密钥：

>随机数的问题在于很难断定其是真正随机的。同时一个密钥应要尽可能的随机。操作系统具有一些生成良好随机数的方法，随机程度则是基于获取这样一个密钥所使用的密码学随机数生成器的。

```python
>>>import os
>>>os.urandom(24)
'\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
```

>这里只需将生成的字串拷贝/粘贴到代码中就可以了。

关于基于cookie的sessions功能的注意点：Flask将接手放入到**session对象**中的数值，并将这些数值序列化为一个cookie。如发现了一些在跨请求中已不存在的数值，那么是开启了cookies的缘故，此时还不能收到某种明确的错误消息，就要检查页面响应中cookie的大小，并将其与web浏览器所支持的cookie大小进行比较。

###消息刷新，Message Flashing

良好的应用及用户界面，都是有关反馈方面的。如用户没有受到足够反馈，那么他们多半会以对该应用的厌恶告终。Flask提供了给与用户反馈的一种极为简单的方式--刷新系统（the flashing system）。刷新系统基础性地令到在一次请求结束时记录一条消息，并在下一次（也仅在下一次）请求中访问到该消息成为可能。此功能又通常与一个布局模版结合，来展示该消息。

使用[`flash()`](http://flask.readthedocs.org/en/latest/api/#flask.flash)方法，来刷新一条消息。要获取到消息，可以使用`get_flashed_messages()`，该方法在模版中也是可用的。请查看[Message Flashing](http://flask.readthedocs.org/en/latest/patterns/flashing/#message-flashing-pattern)部分，获取完整示例。


##日志功能

*版本0.3中引入的新功能。*

有时可能会与到所处理的数据应该是正确的，但实际则不然的情形。比如可能得到了一些发出一个HTTP请求到服务器的客户端代码，但确实明显格式错误的代码。这可能是由于用户对数据做了篡改，或者客户端代码失误造成的。在那种情况下，多数时候回应其一个`400 Bad Request`就可以了，但有时却没有作用，代码会继续运行。

同时还会打算将发生的一些可疑事件记录下来。这就是日志记录器用到的地方。在Flask 0.3中，已为日志记录预先配置了一个日志记录器（a logger）。

这里是一些日志调用的示例：

```python
app.logger.debug('A value for debugging')
app.logger.warning('A warning occured (%d apples)' % 42)
app.logger.error('An error occured')
```

这里所附上的[`logger`](http://flask.readthedocs.org/en/latest/api/#flask.Flask.logger)，是一个标准的日志记录[`Logger`](https://docs.python.org/dev/library/logging.html#logging.Logger)，所以请移步官方的[logging documentation](https://docs.python.org/library/logging.html)以获取更多信息。

同时请越多更多的有关[Application Errors](http://flask.readthedocs.org/en/latest/errorhandling/#application-errors)文档。

##对WSGI中间件的调用，Hooking in WSGI Middlewares

可将内部的WSGI应用加以封装，实现将一个WSGI中间件加入到应用。比如在打算使用Werkzeug包的一个有关解决lighttpd的漏洞的中间件时，可以这样做：

```python
from werkzeug.contrib.fixers import LighttpdCGIRootFix
app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)
```

##Flask众多扩展的使用

这些扩展是一些有助于完成常见任务的包。比如Flask-SQLAlchemy就提供了SQLAlchemy的支持，从而使得在Flask使用起来简单又容易。

##部署到某种Web服务器

已准备好将新的Flask应用进行部署了？请移步[Deployment Options](http://flask.readthedocs.org/en/latest/deploying/#deployment)。

