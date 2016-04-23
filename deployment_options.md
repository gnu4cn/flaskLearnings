尽管其是轻量级且易于使用的，但**Flask的内建服务器却并不适合用于生产**，因为其无法良好伸缩，同时默认下只能一次服务一个请求。下面对一些在生产下运行Flask的选项，进行了讲解。

如打算将Flask应用部署到一种这里没有列出的WSGI服务器，就需要参照该服务器文档，看看如何在该服务器下使用WSGI应用。只要记住那个**Flask**应用对象，就是这个真实的WSGI应用即可。

##寄存主机选项（略）


##自行提供服务的选项

###mod_wsgi(Apache服务器)

（略）

###单独运行的WSGI容器

（略）

###uWSGI（nginx）

uWSGI是Flask应用在[nginx](http://nginx.org/)、[lighttpd](http://www.lighttpd.net/)以及[cherokee](http://cherokee-project.com/)这样的服务器上的一种部署选项；对于其它选项，参见[FastCGI](http://flask.readthedocs.org/en/latest/deploying/fastcgi/#deploying-fastcgi)以及[Standalone WSGI Containers](http://flask.readthedocs.org/en/latest/deploying/wsgi-standalone/#deploying-wsgi-standalone)。要在uWSGI协议下使用上WSGI应用，首先需要一个uWSGI的服务器。uWSGI既是一种协议，还是一种应用服务器；该应用服务器可支持uWSGI、FastCGI及HTTP协议。

最流行的uWSGI服务器就是[uwsgi](http://projects.unbit.it/uwsgi/)了，在本手册种，将使用这个服务器。在继续下面的操作前，务必要安装好该服务器。

>注意：

>请事先确定在应用中可能存在的`app.run()`都位于`if __name__ == '__main__':`程序块中，或已被移入到一个单独文件。就是要确保其不被调用，因为对`app.run()`的调用总是会启动一个本地的WSGI服务器，而这在将该应用部署到uWSGI是不想要的。

###使用uwsgi启动应用

*uwsgi*设计用于在python模块中发现的可进行WSGI调用的对象上运作（*uwsgi* is designed to operate on WSGI callables found in python modules）。

比如对于在*myapp.py*中的某个flask应用，就要使用下面的命令：

```bash
$uwsgi -s /tmp/uwsgi.sock --manage-script-name --mount /yourapplication=myapp:app
```

这里的`--manage-script-name`选项，将对`SCRIPT_NAME`的处理，转移给uwsgi，因为uwsgi更为高明。该选项与另一个`--mount`指令一同使用，而`--mount`指令将那些到`/yourapplication`的请求，导向至`myapp:app`。而如应用可在根级别进行访问，就可以用单独的`/`取代`/yourapplication`。`myapp`指的是提供出`app`对象的flask应用的文件名（是不带扩展名`.py`的）或模块名称。`app`就是应用中所调用的对象了（通常该行就是`app = Flask(__name__)`）。

而如打算将flask应用部署在一个虚拟环境中，则需加入`--virtualenv /path/to/virtual/environment`。同时根据项目所用到的Python版本，可能还需要加入`--plugin python`或`--plugin python3`。

###nginx的配置

一个基本的nginx配置看起来像这样：


