import os 
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor, CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap5
import secrets


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articles.db'
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", os.urandom(24).hex())

bootstrap = Bootstrap5(app)
ckeditor = CKEditor(app)
db = SQLAlchemy(app)

class ArticleDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    thumbnail_image = db.Column(db.String(200), nullable=False)
    banner_image = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(400), nullable=False)
    body = db.Column(db.Text, nullable=False)

class ArticleForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    thumbnail_image = StringField("Thumbnail Image", validators=[DataRequired(), URL()])
    banner_image = StringField("Banner Image", validators=[DataRequired(), URL()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    body = CKEditorField("Body", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create Database
with app.app_context():
    db.create_all()

    if ArticleDB.query.count() == 0:
        sample_articles = [
            ArticleDB(title="AWS Cloud Best Practices",  thumbnail_image="https://th.bing.com/th/id/OIP.axQ6oXfHg3Hw6f2lWc7h5QHaEK?rs=1&pid=ImgDetMain", banner_image="https://th.bing.com/th/id/OIP.axQ6oXfHg3Hw6f2lWc7h5QHaEK?rs=1&pid=ImgDetMain", 
                    subtitle="Guide to AWS best practices for scalability and security.", body="CKEBODYGuide to AWS best practices for scalability and security."
                    ),

            ArticleDB(title="Machine Learning Basics",  thumbnail_image="https://th.bing.com/th/id/OIP.axQ6oXfHg3Hw6f2lWc7h5QHaEK?rs=1&pid=ImgDetMain", banner_image="https://th.bing.com/th/id/OIP.axQ6oXfHg3Hw6f2lWc7h5QHaEK?rs=1&pid=ImgDetMain", 
                    subtitle="Introduction to supervised and unsupervised learning.", body="CKEBODYGuide to AWS best practices for scalability and security."
                    ),

            ArticleDB(title="John 3:16 Reflection",  thumbnail_image="https://th.bing.com/th/id/OIP.axQ6oXfHg3Hw6f2lWc7h5QHaEK?rs=1&pid=ImgDetMain", banner_image="https://th.bing.com/th/id/OIP.axQ6oXfHg3Hw6f2lWc7h5QHaEK?rs=1&pid=ImgDetMain", 
                    subtitle="A personal reflection on faith and the love of God.", body="CKEBODYGuide to AWS best practices for scalability and security."
                    ),

            ArticleDB(title="Proverbs on Wisdom",  thumbnail_image="https://th.bing.com/th/id/OIP.axQ6oXfHg3Hw6f2lWc7h5QHaEK?rs=1&pid=ImgDetMain", banner_image="https://th.bing.com/th/id/OIP.axQ6oXfHg3Hw6f2lWc7h5QHaEK?rs=1&pid=ImgDetMain", 
                    subtitle="Understanding wisdom in biblical teachings.", body="CKEBODYGuide to AWS best practices for scalability and security."
                    )
        ]

        db.session.add_all(sample_articles)
        db.session.commit()





@app.route("/")
def index():
    articles = db.session.query(ArticleDB).all()
    articles = [article for article in articles]
    return render_template("index.html", articles=articles)


@app.route('/article/<int:article_id>/', methods=['GET'])
def article(article_id):
    article = ArticleDB.query.get(article_id)
    return render_template('article.html', article=article)



@app.route('/new_article/', methods=['GET', 'POST'])
def new_article():
    article_form = ArticleForm()
    if article_form.validate_on_submit():
        new_article = ArticleDB(
            title=article_form.title.data,
            thumbnail_image=article_form.thumbnail_image.data,
            banner_image=article_form.banner_image.data,
            subtitle=article_form.subtitle.data,
            body=article_form.body.data
        )
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editor.html', article_form=article_form)


@app.route('/edit_article/<int:article_id>/', methods=['GET', 'POST'])
def edit_article(article_id):
    existing_article = db.get_or_404(ArticleDB,article_id)
    article_form = ArticleForm(
        title = existing_article.title,
        thumbnail_image = existing_article.thumbnail_image,
        banner_image = existing_article.banner_image,
        subtitle = existing_article.subtitle,
        body = existing_article.body
      )
    
    if article_form.validate_on_submit():
        
        existing_article.title = article_form.title.data
        existing_article.thumbnail_image = article_form.thumbnail_image.data
        existing_article.banner_image = article_form.banner_image.data
        existing_article.subtitle = article_form.subtitle.data
        existing_article.body = article_form.body.data
        db.session.commit()
        print(existing_article.body)
        return redirect(url_for('article', article_id=article_id))
    return render_template('editor.html', article_form=article_form)


@app.route('/delete_article/<int:article_id>/', methods=['GET'])
def delete_article(article_id):
    article = db.get_or_404(ArticleDB, article_id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/about/')
def about():
    return render_template('about.html')
@app.route('/contact/')
def contact():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
