利用nginx的alias功能，如下所示：

```ini
    # for angularJS web application
    location / {
        alias /home/peng/flask/infoFMP/www-root/;
    }

```

此外还要在`/etc/nginx/nginx.conf`中，加入一行：

```
user peng peng;
```

表明以用户peng及组peng允许nginx。

