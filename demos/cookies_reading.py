from flask import request

@app.route('/')
def index():
    username = request.cookies.get('username')
    #这里使用了cookies.get(key)而不是cookies[key], 是
    #为了在cookie缺失时不会得到一个KeyError错误
