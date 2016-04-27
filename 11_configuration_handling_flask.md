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
| TRAP_BAD_REQUEST_ERRORS       | 
| PREFFERED_URL_SCHEME          |
| JSON_AS_ASCII                 |
| JSON_SORT_KEYS                |
| JSONIFY_PRETTYPRINT_REGULAR   |
| JSONIFY_MIMETYPE              |
| TEMPLATES_AUTO_RELOAD         |
| EXPLAIN_TEMPLATE_LOADING      |
