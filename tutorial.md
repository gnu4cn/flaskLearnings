打算要使用Python和Flask框架开发一个应用了？这里就可以通过例子进行学习。在本教程中，将建立一个简单的微博客应用（a simple microblogging application）。其只支持一个用户，且只能创建文本条目，同时没有源或评论（no feeds or comments），但仍旧具备了对于起步所需的那些特性。这里将使用到Flask，并将SQLite作为数据库（SQLite是Python自带的），因此而不需要其它的库了。

如需完整的事先写好的代码或作对比用途，可下载到[example source](https://github.com/pallets/flask/tree/master/examples/flaskr/)。

##关于Flaskr

这里将这个博客应用叫做Flaskr，但取一个不那么Web-2.0式的（Web-2.0-ish）名字也都是可以的；）这里基本上要该应用完成下面的功能：

1. 令到用户可以使用在配置文件中指定的凭据进行登入登出操作。只支持一个用户。

2. 在用户登入后，就可以加入包含了一个文本标题及内容的一些HTML的新文章到页面。并未对这些HTML进行清理（sanitized），因为这里是信任用户的。

3. 在首页以新旧顺序显示所有的文章（最新的在顶部），同时用户如已登入，就可以在首页加入新文章。

这里将直接使用SQLite3，因为对于这样大小的应用，其已足够好了。对于大型应用，则使用到SQLAlchemy就很有必要，因为其处理数据库连接的方式更为明智，允许同时利用不同的关系型数据库等特性。而如果数据更适合于NoSQL数据库，就要考虑使用一些流行的此类数据库了。

下面是该应用最终的一个屏幕截图：

![flaskr](./images/flaskr.png)

##步骤0：建立各个文件夹

在起步前，要建立该应用所需的文件夹：

```bash
/flaskr
    /static
    /templates
```

该`flaskr`文件夹并不是一个Python包，而仅是一个要放入一些文件的地方。随后将放入数据库图式及主模块（database schema as well as main module）到此文件夹。该应用是按下面地方式完成的。位于`static`文件夹中的文件，通过HTTP投递到应用的用户。CSS及JavaScript文件是放在这里的。而在`templates`文件夹中，Flask将查找Jinja2模版。本教程后面所创建的模版，都将放在这里。


##步骤1：数据库图式

首先，这里要创建出数据库图式。本应用只需一个简单的表，同时只打算支持SQLite，所以数据库图式的创建是相当容易的。只需将下面的内容放入到刚才所建立的*flaskr*文件夹下的一个名为*schema.sql*中：

```sql
drop table if exists entries;
create table entries (
    id integer primary key autoincrement,
    title text not null,
    'text' text not null
);
```

该图式又一个名为`entries`的单一表构成。该表中每行记录都有一个`id`、`title`和`text`。`id`是一个自动增加的整数，同时作为一个主键（a primary key），其它两个字段都是非空的字符串（strings that must not be null）。

##步骤2：应用的设置代码，Application Setup Code


