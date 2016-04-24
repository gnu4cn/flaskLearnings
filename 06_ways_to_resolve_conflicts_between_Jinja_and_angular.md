1. 使用flask-triangle

示例，*app.py*：


```python
from flask import Flask, render_template
from flask.ext.triangle import Triangle

app = Flask(__name__, static_path='/static')

Triangle(app)

@app.route('/')
def index():
    return render_template('index.html')if __name__ == '__main__':
    app.run()
```

*templates/index.html*：

```html
<!DOCTYPE html>
 <html data-ng-app>
 <head>
 <meta charset="utf-8">
 <script src="/static/js/angular.min.js"></script>
 <title>Flask-Triangle - Tutorial</title>
 </head>
 <body>
 <label>Name:</label>
 <input type="text" data-ng-model="yourName" placeholder="Enter a name here">
 <hr>
 <h1>Hello {{yourName|angular}}!</h1>
 </body>
 </html>
```

2、3出自[这里](http://lorenhoward.com/blog/how-to-get-angular-to-work-with-jinja/)

2. 使用verbatim暂停Jinja2的解析：

```html
{% raw %}
<h1 class="user-name">{{ user.name }}</h1>
{% endraw %}
```

3. 将angular模版使用的符号修改为`{[`

在前端上初始化Angular应用后，可以告诉Angular去搜寻另一种绑定标记（不同于原先的`{{`及`}}`）。

```javascript
var app = angular.module('myApp', []);

app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[');
  $interpolateProvider.endSymbol(']}');
}]);
```

这个代码片断就是告诉angular去查找`{[`作为开始标记，以及`]}`作为结束标记。

现在就可以同时使用Angular和Jinja了。

```html
<h1 class="{{ some_class }}">{[ foo.bar ]}</h1>
```

可以看到，h1元素的类将在后端由Jinja与Flask/Django来渲染。当其发送到浏览器时，看起来将是这样的：

```html
<h1 class="some-class">{[ foo.bar ]}</h1>
```

到这里，Angular将看到`{[ foo.bar ]}`应是一个绑定，而相应地更新该视图。
