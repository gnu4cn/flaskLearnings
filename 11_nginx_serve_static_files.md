利用nginx的alias功能，如下所示：

```ini
    # angularJS partials
    location /partials/ {
        alias /home/unisko/flask/demos/restful/partials/;
    }
```

**注意**： 要使用

```
$sudo chown -R www-data:www-data /path/to/static/files
```

将该目录变更为nginx所用到的系统用户及组别。
