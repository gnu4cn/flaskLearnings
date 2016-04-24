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

###配置 uwsgi

下面的内容引用自： [阿里云部署 Flask + WSGI + Nginx 详解](http://www.tuicool.com/articles/zUvqMr)。

好了，项目的准备工作已经做完了，是时候回过头去配置 uwsgi 了，它的具体指令可以去看它的官方文档，我们在这里采用其中的一种指令方式：配置起动。我采用 .ini文件作为配置，在项目目录下创建一个 confg.ini （具体见下文）写好后可以这样执行：

```bash
(venv)my_flask root$ uwsgi config.ini
```

我认为是最简单的方式，也容易更改。好了重要部分来了，*config.ini* 是这样写的：


```ini
[uwsgi]

# uwsgi 启动时所使用的地址与端口
socket = 127.0.0.1:8001 

# 指向网站目录
chdir = /home/www/ 

# python 启动程序文件
wsgi-file = manage.py 

# python 程序内用以启动的 application 变量名
callable = app 

# 处理器数
processes = 4

# 线程数
threads = 2

#状态检测地址
stats = 127.0.0.1:9191
```

注意 ： `callable=app` 这个 `app` 是 *manage.py* 程序文件内的一个变量，这个变量的类型是 Flask的 application 类 。

运行 uwsgi：

```bash
(venv)my_flask root$ uwsgi config.ini

[uWSGI] getting INI configuration from config.ini

*** Starting uWSGI 2.0.8 (64bit) on [Fri Dec 19 14:34:11 2014]

// 此处略去那些无用的启动信息

Stats server enabled on 127.0.0.1:9191 fd: 15 ***
```

OK， 此时已经正常启动 uwsgi 并将 Flask 项目载入其中了，ctrl+c 关闭程序。但这只是命令启动形式，要使其随同服务器启动并作为后台服务运行才是运营环境的实际所需要。因此接下来我们需要安装另一个工具来引导 uwsgi 。


###安装 Supervisor

[Supervisor](http://supervisord.org/configuration.html) 可以同时启动多个应用，最重要的是，当某个应用Crash的时候，他可以自动重启该应用，保证可用性。

```bash
sudo apt-get install supervisor
```

Supervisor 的全局的配置文件位置在：

```bash
/etc/supervisor/supervisor.conf
```

正常情况下我们并不需要去对其作出任何的改动，只需要添加一个新的 *.conf 文件放在

```bash
/etc/supervisor/conf.d/
```


下就可以，那么我们就新建立一个用于启动 my_flask 项目的 uwsgi 的 supervisor 配置 (命名为： *my_flask_supervisor.conf*)：

```ini
[program:my_flask]
# 启动命令入口
command=/home/www/my_flask/venv/bin/uwsgi /home/www/my_flask/config.ini

# 命令程序所在目录
directory=/home/www/my_flask
#运行命令的用户名
user=root
    
autostart=true
autorestart=true
#日志地址
stdout_logfile=/home/www/my_flask/logs/uwsgi_supervisor.log        
```


####启动服务

```bash
sudo service supervisor start
```

####终止服务

```bash
sudo service supervisor stop
```

###安装 Nginx

[Nginx](http://nginx.com/) 是轻量级、性能强、占用资源少，能很好的处理高并发的反向代理软件。

```bash
sudo apt-get install nginx
```

####配置 Nginx

Ubuntu 上配置 Nginx 也是很简单，不要去改动默认的 nginx.conf 只需要将

```bash
/ext/nginx/sites-available/default
```

文件替换掉就可以了。

新建一个 default 文件:

```ini
  server {
    listen  80;
    server_name XXX.XXX.XXX; #公网地址
  
    location / {
    include      uwsgi_params;
    uwsgi_pass   127.0.0.1:8001;  # 指向uwsgi 所应用的内部地址,所有请求将转发给uwsgi 处理
    uwsgi_param UWSGI_PYHOME /home/www/my_flask/venv; # 指向虚拟环境目录
    uwsgi_param UWSGI_CHDIR  /home/www/my_flask; # 指向网站根目录
    uwsgi_param UWSGI_SCRIPT manage:app; # 指定启动程序
    }
  }
```

将default配置文件替换掉就大功告成了！还有，更改配置还需要记得重启一下nginx:

```bash
sudo service nginx restart
```
