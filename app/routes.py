from app import app
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    user = {
        'username': 'John',
        'password': 'pass'
    }
    posts = [
        {
            'author': {
                'username': 'Michel'
            },
            'body': "The weather is great"
        },
        {
            'author': {
                'username': 'Patrick'
            },
            'body': "I love Python"
        }

    ]
    return render_template('index.html', user=user, posts=posts)

