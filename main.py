import os 
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///articles.db'
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    style_class = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # New field


# Create Database
with app.app_context():
    db.create_all()

    if Article.query.count() == 0:
        sample_articles = [
            Article(title="AWS Cloud Best Practices", image="assets/images/pic01.jpg", 
                    description="Guide to AWS best practices for scalability and security.",
                    style_class="style1", link="generic.html", category="portfolio"),

            Article(title="Machine Learning Basics", image="assets/images/pic01.jpg", 
                    description="Introduction to supervised and unsupervised learning.",
                    style_class="style2", link="generic.html", category="portfolio"),

            Article(title="John 3:16 Reflection", image="assets/images/pic01.jpg", 
                    description="A personal reflection on faith and the love of God.",
                    style_class="style3", link="generic.html", category="reading"),

            Article(title="Proverbs on Wisdom", image="assets/images/pic01.jpg", 
                    description="Understanding wisdom in biblical teachings.",
                    style_class="style4", link="generic.html", category="reading")
        ]

        db.session.add_all(sample_articles)
        db.session.commit()




app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')

@app.route("/")
def index():
    articles = Article.query.all()
    return render_template("index.html", articles=articles)

@app.route("/portfolio/")
def portfolio():
    articles = Article.query.filter_by(category="portfolio").all()
    return render_template("index.html", articles=articles)

@app.route("/reading/")
def reading():
    articles = Article.query.filter_by(category="reading").all()
    return render_template("index.html", articles=articles)


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
