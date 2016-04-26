from flask import request

with app.request_context(environ):
    assert request.method == 'POST'
