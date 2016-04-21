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
$python hello.py
```

这将启动一个非常简单的内建服务器，该服务器对于测试来说是足够好的，但大概不会在生产中使用。对于生产部署选项，请参阅[Deployment Options](http://flask.readthedocs.org/en/latest/deploying/#deployment)。

那么现在打开[http://localhost:5000/](http://localhost:5000/)，就可以看到hello world问候语了。

###外部可见的服务器

在运行该服务器时，会注意到该服务器仅能从自己的计算机访问到，而不能从网络中的其它计算机进行访问。这时默认的，因为在调试模式下，应用的用户可执行你的计算机上任意的Python代码。

如关闭了调试器，或是信任网络上的用户，就可以通过简单地加入`--host=0.0.0.0`到命令行，来开启该服务器的公开访问。

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

`flask`脚本对于启动一个本地开发服务器来说是不错的，但在每次对代码进行了修改后，都必须重启该服务器。那就不是很好了，而Flask却可以做得更好。

