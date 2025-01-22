from flask import Flask, render_template
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/post/')
def post():
    return render_template('post.html')
@app.route('/about/')
def about():
    return render_template('about.html')
@app.route('/contact/')
def contact():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
