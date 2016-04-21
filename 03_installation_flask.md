#Flask的安装

Flask依赖一些外部库，比如Werkzeug以及Jinja2。Werkzeug是一个用于WSGI的工具套件，而WSGI则是位处web应用与各种不同服务器之间，这些服务器在开发和部署上有着不同。Jinja2则是用于渲染模版。

那么怎样才能快速地令到Flask及其依赖的这些库在计算机上都运行起来呢？完成这个有多种方式，但最暴力的方法就是[virtualenv](./Python的虚拟环境virtualenv.pdf)了，所以这里要先说这种方法。

要开始安装，需要Python 2.6或更新的版本，所以请确保有着一个更新了的Python 2.x安装。要在Python 3下使用Flask，请参见[Python 3 Support](http://flask.readthedocs.org/en/latest/python3/#python3-support)。

##关于virtualenv

Virtualenv大概就是在开发过程中你想要的了，同时如有着对生产机器的shell访问，则也大概会在那里使用virtualenv。

virtualenv解决了什么问题呢？如你如同我一样喜欢Python，那么就会在除了基于Flask的web应用之外的其它项目都用到Python。但你有的项目越多，就越会遇到对Python本身版本要求的不同，或至少会对那些库的版本有不同要求。我们必须面对这样的问题：这些库通常会破坏向后兼容性，同时任何重要应用都不会有零依赖（zero dependencies）。那么在两个或更多的项目有着依赖冲突时，该怎么办呢？

这时virtualenv技术成了救命稻草！Virtualenv令到多个Python的并行安装可行，从而为单个的项目安装一个Python。其并不是真的安装上Python的独立拷贝，而是提供了一种明晰方式，来保持不同项目环境的隔离。下面看看virtualenv的工作原理。

如果你用的是Mac OS X或者Linux，下面两个命令都能运行：

```bash
$sudo easy_install virtualenv
```

或者更好的：

```bash
$sudo pip install virtualenv
```

这两个命令都将在你的系统上安装virtualenv。或者在软件包管理器中。如使用Ubuntu，就尝试：

```bash
$sudo apt-get install python-virtualenv
```

而在Windows上则没有**`easy_install`**命令，就需要先安装这个命令。请查看[pip and setuptools on Windows](http://flask.readthedocs.org/en/latest/installation/#windows-easy-install)章节，以获得如何安装该命令的更多信息。而一旦安装好此命令，就可以运行上面的命令了，不过要去掉**`sudo`**前缀。

在安装好virtualenv后，仅需开启一个shell并建立自己的环境了。我通常会建立一个文件夹和其内部的`venv`文件夹。

```bash
$mkdir myproject
$cd myproject
$virtualenv venv
New python executable in venv/bin/python
Installing setuptools, pip, wheel...done.
```

现在，当你要在某个项目上做事时，只须激活相应的环境即可。在OS X和Linux上，执行下面的命令：

```bash
$. venv/bin/activate
```

或者：

```bash
$source venv/bin/activate
```

而如果在Windows上，则执行下面的命令：

```bash
$venv\scripts\activate
```

不管那种方式，现在都可以用上virtualenv（请注意shell提示符已变成显示该活动的环境了）。

而要退回到真实世界，就使用下面的命令：

```bash
$deactivate
```

在执行该命令后，shell提示符将是熟悉的样子。

现在继续后面的操作。请输入下面的命令来在虚拟环境中激活Flask:

```bash
$pip install Flask
```

过几秒钟，就可以开始Flask框架的编程了。

##全系统安装Flask

这样做可能也不错，但我不建议这样做。这里只需以root权限运行**`pip`**即可：

```bash
$sudo pip install Flask
```

（在Windows系统上，在一个具有管理员权限的命令行提示窗口（a command-prompt window with administrator privileges）运行该命令，同时去掉其中的**`sudo`**）。

##保持版本最新

如你想要使用最新版的Flask，那么有两种方法：通过**`pip`**拉入开发版本，或者告诉pip通过git checkout进行Flask的安装。同样都建议在virtualenv下进行。

下面是在一个新的virtualenv下获取git checkout，并在开发模式下运行：

```bash
$git clone http://github.com/pallets/flask.git
Initialized empty Git repository in ~/dev/flask/.git/
$cd flask
$virtual venv
New python executable in venv/bin/python
Installing setuptools, pip, wheel...done.
$. venv/bin/activate
$python setup.py develop
...
Finished processing dependencies for Flask
```

该操作将拉入依赖的库，并将git头部作为当前版本，在这个virtualenv中进行激活。此后要更新到最新版本，就仅需运行`git pull origin`命令了。

##Windows上的*pip*与*setuptools*

（略）
