##Flask应用配置的处理

*版本0.3中的新特性*

应用总是需要某种配置的。实际开发中，根据应用环境的不同，总是想要对多个不同配置进行修改，比如调试模式的开启与关闭，密钥的设置，以及其它针对环境的一些事物。

Flask设计方式通常要求在应用启动时其配置需要可用。对于许多小型应用来说，可将配置硬编码在代码中，这么做也没什么坏处，但仍有更好的方式来处理应用的配置。

不管如何去装入配置，应用都有着一个保存所装入的各种配置值的对象：即[`Flask`](http://flask.readthedocs.org/en/latest/api/#flask.Flask)对象的[`config`](http://flask.readthedocs.org/en/latest/api/#flask.Flask.config)属性。这里就是Flask本身将一些配置值放入的地方，同时也是那些Flask扩展（译者注：比如Flask-SQLAlchemy等）可将其配置值放入的地方。这里还可以放入应用本身的一些配置。

###配置基础

该config对象实际上是字典的子类（a subclass of a dictionary），因此可像任何字典那样对其进行修改：

```python
app = Flask(__name__)
app.config['DEBUG'] = True
```

一些配置值是转发到`Flask`对象的，因此也可在那里对其进行读取和写入：

```python
app.debug = True
```

而要一次性更新多个键，可使用`dict.update()`方法：

```python
app.config.update(
    DEBUG=True,
    SECRET_KEY='...'
)
```

###内建的那些配置值

下面的这些配置值，是Flask内部所用到的：

| 配置值                        | 说明                                  |
| :-----------:                 | :-----------------------------------: |
| DEBUG                         | 开启/关闭调试模式。                   |
| TESTING                       | 开启/关闭测试模式。                   |
| PROPAGATE_EXCEPTIONS          | 显式开启或关闭列外的传播/传递。如为对该配置值进行设置，或显式地设置为`None`，那么在`TESTING`或`DEBUG`二者之一设置为`True`时，该配置值将隐式为`True`。    |
| PRESERVE_CONTEXT_ON_EXCEPTION | 默认下当应用处于调试模式时，该请求上下文在出现例外时不会生成以开启调试器来对数据进行检查。可通过此键关闭这个行为。同样可以使用该设置来强制开启非调试执行下的此功能，这样做可对生产应用进行调试（但风险很高）。    |
| SECRET_KEY                    | 密钥（Session功能用到，RESTful API则一点也用不到）。  |
| SESSION_COOKIE_NAME           | （略）    |
| SESSION_COOKIE_DOMAIN         | （略）    |
| SESSION_COOKIE_PATH           | （略）    | 
| SESSION_COOKIE_HTTPONLY       | （略）    |
| SESSION_COOKIE_SECURE         | （略）    |
| PERMANENT_SESSION_LIFETIME    | （略）    |
| SESSION_REFRESH_EACH_REQUEST  | （略）    |
| USE_X_SENDFILE                | 开启/关闭 x-sendfile功能。    |
| LOGGER_HANDLER_POLICY         | 默认日志记录处理器的策略。该配置值默认为`'always'`，意思是默认日志记录处理器总是开启的。`'debug'`值将仅在调试模式下开启日志记录，`'production'`则仅在生产中进行记录同时`'never'`则完全关闭日志记录功能。    |
| LOGGER_NAME                   | 日志记录器名称。  |
| SERVER_NAME                   | 服务器的名称和端口号。对于子域名支持是必要的（比如：`'myapp.dev:5000'`），请注意localhost是不支持子域名的，所以将此配置设置为“localhost”没有作用。同时设置一个`SERVER_NAME`就默认开启无需请求上下文的，而是在应用上下文下的URL生成（Setting a 'SERVER_NAME' also by default enables URL generation without a request context but with an application context）。 |
| APPLICATION_ROOT              | 在应用没有占据一个完整的域或子域时，此配置可设置为该应用配置做存活的路径。该配置将作为session cookie的路径值。而在使用了域时，就应将此配置设置为`None`。  |
| MAX_CONTENT_LENGTH            | 如此配置被设置为一个字节数，那么Flask将以返回一个413状态代码方式，拒绝那些内容长度超过此配置值的请求。   |
| SEND_FILE_MAX_AGE_DEFAULT     | 与[`send_static_file()`](http://flask.readthedocs.org/en/latest/api/#flask.Flask.send_static_file)（默认的静态文件处理函数）及[`send_file()`](http://flask.readthedocs.org/en/latest/api/#flask.send_file)一起使用的，默认缓存控制最大存活时间，可已是[`datetime.timedelta`](https://docs.python.org/dev/library/datetime.html#datetime.timedelta)类型的值，或秒数。可使用[Flask](http://flask.readthedocs.org/en/latest/api/#flask.Flask)或[Blueprint](http://flask.readthedocs.org/en/latest/api/#flask.Blueprint)上相应的[`get_send_file_max_age()`](http://flask.readthedocs.org/en/latest/api/#flask.Flask.get_send_file_max_age)钩子，来对其进行覆写。默认为43200（也就是12小时）。    |
| TRAP_HTTP_EXCEPTIONS          | 如将此配置设为`True`，Flask就不会执行HTTP例外错误处理器（the error handlers of HTTP exceptions），而会将例外像其它例外一样处理，同时通过例外堆栈将其冒出。这样做对于在不得不找出HTTP例外来自何处的危险的调试情形下，是有帮助的。    |
| TRAP_BAD_REQUEST_ERRORS       | Werkzeug模块用于处理特定于请求数据的内部数据结构，将出现特殊的键错误，这也是不良请求例外。
| PREFFERED_URL_SCHEME          | 在没有可用的URL方案时，用于URL生成的方案。默认为`http`。  |
| JSON_AS_ASCII                 | 默认情况下，Flask将对象序列化为ascii编码的JSON。而如将此配置设置为`False`，就不会编码为ASCII，而原样输出字串并返回unicode编码的字符串。`jsonify`会自动将对象进行编码，随后做为实例进行传输（`jsonify` will automatically encode it in `utf-8` then for transport for instance）。    |
| JSON_SORT_KEYS                | 默认下，Flask将按键值排序的方式，对JSON对象进行序列化处理。这样做是为了确保字典的散列化种子数据的独立，从而令到返回值的一致性而不会造成外部HTTP缓存的碎片化。可通过修改此变量，来覆写该默认行为。尽管不推荐这样做，但可在牺牲缓存性能上，得到一些性能的提升。    |
| JSONIFY_PRETTYPRINT_REGULAR   | 在此配置项设置为`True`（也就是默认设置），同时在不是由一个XMLHttpRequest对象发起请求时（这是由`X-Requested-With`头部控制的），jsonify的响应就会是打印友好的。 |
| JSONIFY_MIMETYPE              | 用于jsonify响应的MIME类型。   |
| TEMPLATES_AUTO_RELOAD         | （略）    |
| EXPLAIN_TEMPLATE_LOADING      | （略）    |

>**更多关于`SERVER_NAME`的内容**：

>`SERVER_NAME`键用于子域名的支持。因为在不知道没有实际服务器名字的情况下，Flask是无法猜到子域名的，所以如打算用到子域名，就需要设置此配置。同时该配置还用于会话cookie。

>请记住不仅Flask有着此不知道子域名为何物的问题，web浏览器同样也不知道。大多数现代web浏览器没有计划允许将子域设置在不带点（`.`）的服务器名字上。所以如果服务器名字为`localhost`，那么是无法为`localhost`及其所有子域设置一个cookie的。在此情况下，就要选择一个不同的服务器名字，比如`myapplication.local`，并将此名字加上打算用到子域，加入到系统的host配置（'/etc/hosts'）或建立一个本地[bind](https://www.isc.org/downloads/bind/)服务器。

n version 0.4: `LOGGER_NAME`

New in version 0.5: `SERVER_NAME`

New in version 0.6: `MAX_CONTENT_LENGTH`

New in version 0.7: `PROPAGATE_EXCEPTIONS`, `PRESERVE_CONTEXT_ON_EXCEPTION`

New in version 0.8: `TRAP_BAD_REQUEST_ERRORS`, `TRAP_HTTP_EXCEPTIONS`, `APPLICATION_ROOT`, `SESSION_COOKIE_DOMAIN`, `SESSION_COOKIE_PATH`, `SESSION_COOKIE_HTTPONLY`, `SESSION_COOKIE_SECURE`

New in version 0.9: `PREFERRED_URL_SCHEME`

New in version 0.10: `JSON_AS_ASCII`, `JSON_SORT_KEYS`, `JSONIFY_PRETTYPRINT_REGULAR`

New in version 1.0: `SESSION_REFRESH_EACH_REQUEST`, `TEMPLATES_AUTO_RELOAD`, `LOGGER_HANDLER_POLICY`, `EXPLAIN_TEMPLATE_LOADING`


###来自文件的配置

如将配置存储在一个单独文件中，理想情况下在为与实际应用包的外部时，其就变得更为有用。这样做就令到通过多种Python包处理工具（[Deploy with Setuptools](http://flask.readthedocs.org/en/latest/patterns/distribute/#distribute-deployment)），对应用进行打包和分发，以及后期对配置文件的最终修改，成为可能。

那么常用的一种模式，是这样的：

```python
app = Flask(__name__)
app.config.from_object('yourapplication.default_settings')
app.config.from_envvar('YOURAPPLICATION_SETTINGS')
```

代码的第一处从*yourapplication.default_settings*模块装入配置，并随即使用`:envvar:YOURAPPLICATION_SETTINGS`这一环境变量所指向的配置文件，对这些配置值进行覆写。在Linux或Mac OS X系统上，可在启动服务器前，于shell中使用export命令，设置该环境变量：

```bash
$ export YOURAPPLICATION_SETTINGS=/path/to/settings.cfg
$ python run-app.py
 * Running on http://127.0.0.1:5000/
 * Restarting with reloader...
```

而在Windows上（略）。

这些配置文件本身实际上是一些Python文件。不过只有大写的值才会保存在随后会讲到的配置对象（the config object）中。所以对这些配置键，务必要使用大写字母。

这里是一个配置文件的示例：

```python
# Example configuration
DEBUG = False
SECRET_KEY = '?\xbf,\xb4\x8d\xa3"<\x9c\xb0@\x0f5\xab,w\xee\x8d$0\x13\x8b83'
```

还务必要在最早期就装入配置，这样做那些用到的扩展，才能在其启动时，访问到配置。当然还有其它一些从单独文件装入配置对象的方式。请阅读[`Config`](http://flask.readthedocs.org/en/latest/api/#flask.Config)对象的文档。

###配置的最佳实践

早前提到的方法，弊端在于其令到测试有点难度。而要令到测试容易，没有哪种100%解决问题的一般做法，但可以记住下面这几种令到测试容易进行的方法：

1. 在某个函数中创建应用，并在其上注册一些蓝图。那样就可以建立多个具有不同配置的应用，从而令到单元测试容易得多。可以采用这种办法将所需的配置传入到应用对象。

2. 不要编写在导入时需要用到配置的代码。而如将对配置的访问限制到只读水平，就可以在随后需要时对该对象进行重新配置。


###开发/生产阶段

大多数应用都需要不止一个的配置。至少需要单独的用于生产的配置，以及在开发阶段用到的配置。处理此问题的最容易方式，就是使用一个始终从版本控制装入的，且作为版本控制的一部分的默认配置，以及上面提到的一个必要的单独配置来覆写这些值：

```python
app = Flask(__name__)
app.config.from_object('yourapplication.default_settings')
app.config.from_envvar('YOURAPPLICATION_SETTINGS')
```

此时就只须假如一个单独的`config.py`，并export `YOURAPPLICATION_SETTINGS=/path/to/config.py`就可以了。但是还有更好的方法。比如可以使用导入或子类化（subclassing）。

在Django世界中，非常流行的就是将`from yourapplication.default_settings import *`加入到文件顶部，并手工覆写这些改变。还可以对一个诸如`YOURAPPLICATION_MODE`之类的环境变量进行检查，并将其设置为*production*、*development*等值，从而依据其导入不同的硬编码的文件。

而一种有趣的模式就是使用类及继承，来实现配置的处理：

```python
class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
```

此时要开启某个配置，只须将其调用到[`from_object()`](http://flask.readthedocs.org/en/latest/api/#flask.Config.from_object)中：

```python
app.config.from_object('configmodule.ProductionConfig')
```

配置处理方式有很多，采用何种方式，取决于打算怎样来管理配置文件。但仍有下面一些建议：

- 在版本控制中保存一份默认配置。并在对各个配置值进行覆写之前，以该默认配置生成应用配置或在配置文件中导入该默认配置。

- 使用一个环境变量，在各个配置之间进行切换。这可在Python解释器外部实现，同时因为可在一点也不触及到代码的情况下，快速而容易地在不同配置之间进行切换，从而可令到开发和部署都更为容易。而加入经常在不同项目上工作，就甚至可以建立用于运行（sourceing, `.`）激活一个virtualenv并导出开发配置的脚本（If you are working often on different projects you can even create your own script for sourcing that activates a virtualenv and exports the development configuration for you）。

- 在生产中使用一种诸如[fabric](http://www.fabfile.org/)的工具来单独地推入代码和配置到服务器。关于此方面更详细的内容，参见[Deploying with Fabric](http://flask.readthedocs.org/en/latest/patterns/fabric/#fabric-deployment)。


###实例文件夹

**版本0.8引入的新特性**。

Flask版本0.8引入了实例文件夹特性。Flask项目用了很长时间，才将直接到相对于应用文件夹的路径引用特性实现（通过`Flask.root_path`）（Flask for a long time made it possible to refer to paths relative to the application‘s folder directly(via `Flask.root_path`)）。此特性也是很多开发者将存储在应用隔壁的那些配置装入进来的方式。不幸的是，此特性仅在应用不是包的形式时才工作，而在应用是包时，根路径则是指向到该包的内容的（Unfortunately however this only works well if applications are not packages in which case the root path refers to the contents of the package）。

在Flask版本0.8中引入了一个新的属性：`Flask.instance_path`。其指的是一个新的概念“实例文件夹（instance folder）”。该实例文件夹被设计为不再版本控制系统之下，而只是针对部署的。它就是将那些在运行时改变的东西或配置文件放入到的完美场所。

既可以在建立Flask应用时显式地提供该实例文件夹的路径，也可以让Flask自动探测到该实例文件夹。下面就是使用*instance_path*参数，显式的配置：

```python
app = Flask(__name__, instance_path='/path/to/instance/folder')
```

请记住此路径在提供是*务必*要是绝对路径。

而在没有提供该*instance_path*参数时，会使用以下的这些默认位置：

- 对于未安装的模块：

```bash
/myapp.py
/instance
```

- 对于文安装的包：

```bash
/myapp
    /_init__.py
/instance
```

- 对于已安装的模块或包：

```bash
$PREFIX/python2.X/site-packages/myapp
$PREFIX/var/myapp-instance
```

>`$PREFIX`就是Python安装的前缀。其可以是`/usr`或到virtualenv的路径。可通过将`sys.prefix`的值进行打印输出（print），来查看该前缀被设置为什么。

因为配置对象（the config object）提供了从相对的文件名装入配置文件，所以就可以在需要时，通过相对于实例路径的不同文件名来改变此装入。在配置文件中的相对路径的表现，可通过应用构造器的*instance_relative_config*开关，在“相对于应用根路径（默认的）”与“相对于实例文件夹”两种形式之间翻转：

```python
app = Flask(__name__, instance_relative_config=True)
```

下面是一个如何将Flask配置为从一个模块预装入配置，并于随后又从一个配置文件夹中的一个文件，在该文件存在的情况下，对配置进行覆写的完整示例：

```python
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('yourapplication.default_settings')
app.config.from_pyfile('application.cfg', silent=True)
```

到示例文件夹的路径，可通过`Flask.instance_path`找到。Flask还提供了一个从实例文件夹打开文件的便捷方法：`Flask.open_instance_resource()`。

这两个属性与方法的使用示例如下：

```python
filename = os.path.join(app.instance_path, 'application.cfg')
with open(filename) as f:
    config = f.read()

# or via open_instance_resource:
with app.open_instance_resource('application.cfg') as f:
    config = f.read()
```



