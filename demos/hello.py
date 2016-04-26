from flask import Flask
app = Flask(__name__)

@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s\n' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post: %d\n' % post_id

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'

