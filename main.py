import os 
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor, CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articles.db'

ckeditor = CKEditor(app)
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    thumbnail_image = db.Column(db.String(200), nullable=False)
    banner_image = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(400), nullable=False)
    body = db.Column(db.Text, nullable=False)

class article(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    thumbnail_image = StringField("Thumbnail Image", validators=[DataRequired()])
    banner_image = StringField("Banner Image", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    body = CKEditorField("Body", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create Database
with app.app_context():
    db.create_all()

    if Article.query.count() == 0:
        sample_articles = [
            Article(title="AWS Cloud Best Practices",  thumbnail_image="https://th.bing.com/th/id/OIP.axQ6oXfHg3Hw6f2lWc7h5QHaEK?rs=1&pid=ImgDetMain", banner_image="https://th.bing.com/th/id/OIP.axQ6oXfHg3Hw6f2lWc7h5QHaEK?rs=1&pid=ImgDetMain", 
                    subtitle="Guide to AWS best practices for scalability and security.", body="CKEBODYGuide to AWS best practices for scalability and security."
                    ),

            Article(title="Machine Learning Basics",  thumbnail_image="https://th.bing.com/th/id/OIP.axQ6oXfHg3Hw6f2lWc7h5QHaEK?rs=1&pid=ImgDetMain", banner_image="https://th.bing.com/th/id/OIP.axQ6oXfHg3Hw6f2lWc7h5QHaEK?rs=1&pid=ImgDetMain", 
                    subtitle="Introduction to supervised and unsupervised learning.", body="CKEBODYGuide to AWS best practices for scalability and security."
                    ),

            Article(title="John 3:16 Reflection",  thumbnail_image="https://th.bing.com/th/id/OIP.axQ6oXfHg3Hw6f2lWc7h5QHaEK?rs=1&pid=ImgDetMain", banner_image="https://th.bing.com/th/id/OIP.axQ6oXfHg3Hw6f2lWc7h5QHaEK?rs=1&pid=ImgDetMain", 
                    subtitle="A personal reflection on faith and the love of God.", body="CKEBODYGuide to AWS best practices for scalability and security."
                    ),

            Article(title="Proverbs on Wisdom",  thumbnail_image="https://th.bing.com/th/id/OIP.axQ6oXfHg3Hw6f2lWc7h5QHaEK?rs=1&pid=ImgDetMain", banner_image="https://th.bing.com/th/id/OIP.axQ6oXfHg3Hw6f2lWc7h5QHaEK?rs=1&pid=ImgDetMain", 
                    subtitle="Understanding wisdom in biblical teachings.", body="CKEBODYGuide to AWS best practices for scalability and security."
                    )
        ]

        db.session.add_all(sample_articles)
        db.session.commit()




app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')

@app.route("/")
def index():
    articles = Article.query.all()
    articles = [article for article in articles]
    return render_template("index.html", articles=articles)


@app.route('/article/<int:article_id>/', methods=['GET'])
def article(article_id):
    article = Article.query.get(article_id)
    return render_template('article.html', article=article)


@app.route('/about/')
def about():
    return render_template('about.html')
@app.route('/contact/')
def contact():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
