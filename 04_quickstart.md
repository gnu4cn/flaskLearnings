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

> 关于UUID：
    UUID含义是通用唯一识别码 (Universally Unique Identifier)，这 是一个软件建构的标准，也是被开源软件基金会 (Open Software Foundation, OSF) 的组织应用在分布式计算环境 (Distributed Computing Environment, DCE) 领域的一部分。

    UUID 的目的，是让分布式系统中的所有元素，都能有唯一的辨识资讯，而不需要透过中央控制端来做辨识资讯的指定。如此一来，每个人都可以建立不与其它人冲突的 UUID。在这样的情况下，就不需考虑数据库建立时的名称重复问题。目前最广泛应用的 UUID，即是微软的 Microsoft‘s Globally Unique Identifiers (GUIDs)，而其他重要的应用，则有 Linux ext2/ext3 档案系统、LUKS 加密分割区、GNOME、KDE、Mac OS X 等等。

    UUID是指在一台机器上生成的数字，它保证对在同一时空中的所有机器都是唯一的。通常平台会提供生成的API。按照开放软件基金会(OSF)制定的标准计算，用到了以太网卡地址、纳秒级时间、芯片ID码和许多可能的数字
UUID由以下几部分的组合：
    1. 当前日期和时间，UUID的第一个部分与时间有关，如果你在生成一个UUID之后，过几秒又生成一个UUID，则第一个部分不同，其余相同。
    2. 时钟序列。
    3. 全局唯一的IEEE机器识别号，如果有网卡，从网卡MAC地址获得，没有网卡以其他方式获得。

    UUID的唯一缺陷在于生成的结果串会比较长。关于UUID这个标准使用最普遍的是微软的GUID(Globals Unique Identifiers)。在ColdFusion中可以用CreateUUID()函数很简单地生成UUID，其格式为：xxxxxxxx-xxxx- xxxx-xxxxxxxxxxxxxxxx(8-4-4-16)，其中每个 x 是 0-9 或 a-f 范围内的一个十六进制的数字。而标准的UUID格式为：xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx (8-4-4-4-12)，可以从cflib 下载CreateGUID() UDF进行转换。

    使用UUID的好处在分布式的软件系统中（比如：DCE/RPC, COM+,CORBA）就能体现出来，它能保证每个节点所生成的标识都不会重复，并且随着WEB服务等整合技术的发展，UUID的优势将更加明显。根据使用的特定机制，UUID不仅需要保证是彼此不相同的，或者最少也是与公元3400年之前其他任何生成的通用唯一标识符有非常大的区别。
    
    通用唯一标识符还可以用来指向大多数的可能的物体。微软和其他一些软件公司都倾向使用全球唯一标识符（GUID），这也是通用唯一标识符的一种类型，可用来指向组建对象模块对象和其他的软件组件。第一个通用唯一标识符是在网络计算机系统（NCS）中创建，并且随后成为开放软件基金会（OSF）的分布式计算环境（DCE）的组件。
