#写给经验丰富程序员的前言

##Flask中的Thread-Locals

Flask中的一个设计决定，就是简单任务应保持简单；它们不应占用大量代码，也不应令到使用者束手束脚。因此，Flask有着少量一些人认为感到惊喜或不那么正统的设计抉择（Flask has a few design choices that some people might find surprising or unorthodox）。比如Flask内如应用到thread-local对象，因此在某个请求中不必为了保持线程安全，而在函数之间进行对象的传递。此方式较为方便，但却为了依赖注入，或在尝试重用那些用到与该请求挂钩的值的代码是，要求此请求务必是有效的。Flask项目对thread-locals是坦诚的，没有遮掩，在用到thread-locals的代码和文档中，都有指出。

##特别留意web开发

在构建web应用时，应总是将安全牢记心间。

在编写web应用时，总是会允许用户注册并将其数据留存在服务器上。这些用户拿数据来托付给你。就算只有你自己会将数据留存在应用中，也是想要这些数据都是安全存储的吧。

不幸的是，突破web应用安全防范的方法有很多。Flask保护你免受现代web应用最常见的安全问题：跨站点脚本执行攻击（cross-site scripting, XSS）。除非故意将不安全的HTML标记为安全的，Flask与其采用的Jinja2模版引擎一道，都能将你保护起来。但仍然有着很多其它导致安全问题的方式。

本文档将就一些web开发中需要安全注意方面，给出一些警告。这些安全关注点的复杂程度，超出一般人的想象，且有时我们都低估了漏洞利用的可能性 -- 直到高明的攻击者找出了攻击我们的应用的方法。同时不要认为你的应用还没有重要到能吸引来攻击者。依据攻击种类的不同，可能有自动化机器人在探测着往你的数据库中填充垃圾信息、链接到恶意软件等类似方法。

Flask与其它需要开发者留意安全问题的框架没有什么差别，在为需求构建应用时，需要注意漏洞利用问题。

##关于Python 3的支持

当前Python社区正在为支持新一代的Python编程语言，而改进诸多的库。尽管情况已有极大改观，但现在对于使用者来说，仍有一些很难迁移到Python 3的问题。这些问题一部分是由该语言中的一些改变在很长时间没有得到评议造成，一部分是因为我们仍然没有完成为解决Python 3中Unicode方面的差异，而进行的一些低级别的API的修改。

我们强烈建议在开发中采用带有激活了Python 3警告的Python 2.7。如计划在近期升级到Python 3，强烈建议阅读[How to write forwards compatible Python code](http://lucumr.pocoo.org/2011/1/22/forwards-compatible-python/)。

如已经想要投身Python 3，则请参见[Python 3 Support](http://flask.readthedocs.org/en/latest/python3/#python3-support)页面。

请继续阅读[Installation](./installation_flask.md)，或者[Quickstart](./quickstart_flask.md)。


