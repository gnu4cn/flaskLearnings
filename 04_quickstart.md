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


