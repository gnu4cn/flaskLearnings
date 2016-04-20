#Flask的安装

Flask依赖一些外部库，比如Werkzeug以及Jinja2。Werkzeug是一个用于WSGI的工具套件，而WSGI则是位处web应用与各种不同服务器之间，这些服务器在开发和部署上有着不同。Jinja2则是用于渲染模版。

那么怎样才能快速地令到Flask及其依赖的这些库在计算机上都运行起来呢？完成这个有多种方式，但最暴力的方法就是[virtualenv](./Python的虚拟环境virtualenv.pdf)了，所以这里要先说这种方法。

要开始安装，需要Python 2.6或更新的版本，所以请确保有着一个更新了的Python 2.x安装。要在Python 3下使用Flask，请参见[Python 3 Support](http://flask.readthedocs.org/en/latest/python3/#python3-support)。

##关于virtualenv

Virtualenv大概就是在开发过程中你想要的了，同时如有着对生产机器的shell访问，则也大概会在那里使用virtualenv。

virtualenv解决了什么问题呢？如你如同我一样喜欢Python，那么就会在除了基于Flask的web应用之外的其它项目都用到Python。但你有的项目越多，就越会遇到对Python本身版本要求的不同，至少会对那些库的版本的不同要求。
