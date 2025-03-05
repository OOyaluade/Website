import os 
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor, CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articles.db'
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", os.urandom(24).hex())

login_manager = LoginManager()
login_manager.init_app(app)
bootstrap = Bootstrap5(app)
ckeditor = CKEditor(app)
db = SQLAlchemy(app)


class ArticleDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    thumbnail_image = db.Column(db.String(200), nullable=False)
    banner_image = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(400), nullable=False)
    date = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)

class ArticleForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    thumbnail_image = StringField("Thumbnail Image", validators=[DataRequired(), URL()])
    banner_image = StringField("Banner Image", validators=[DataRequired(), URL()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    # date = StringField("Date", validators=[DataRequired()])
    # author_id = StringField("Author ID", validators=[DataRequired()])
    body = CKEditorField("Body", validators=[DataRequired()])
    submit = SubmitField("Submit")


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    user_name = db.Column(db.String(100), unique=True)    
    user_articles = db.relationship('ArticleDB', backref='author', lazy=True)

class UserForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    user_name = StringField("User Name", validators=[DataRequired()])
    submit = SubmitField("Submit")

class ContactForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    message = CKEditorField("Message", validators=[DataRequired()])

# Create Database
with app.app_context():
    db.create_all()




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register/', methods=['GET', 'POST'])
def register():
    user_form = UserForm()
    if user_form.validate_on_submit():
        new_user = User(
            email=user_form.email.data,
            password=user_form.password.data,
            first_name=user_form.first_name.data,
            last_name=user_form.last_name.data,
            user_name=user_form.user_name.data
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template('register.html', user_form=user_form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = db.session.query(User).filter_by(email=email, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/")
def index():
    articles = db.session.query(ArticleDB).all()
    articles = [article for article in articles]
    return render_template("index.html", articles=articles, is_authenticated=current_user.is_authenticated)


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
            # body=article_form.body.data,
            # date=article_form.date.data,
            author_id=current_user.id
        )
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('editor.html', article_form=article_form, is_authenticated=current_user.is_authenticated)


@app.route('/edit_article/<int:article_id>/', methods=['GET', 'POST'])
def edit_article(article_id):
    existing_article = db.get_or_404(ArticleDB,article_id)
    article_form = ArticleForm(
        title = existing_article.title,
        thumbnail_image = existing_article.thumbnail_image,
        banner_image = existing_article.banner_image,
        subtitle = existing_article.subtitle,
        body = existing_article.body,
        date = existing_article.date,
        author_id = existing_article.author_id
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
