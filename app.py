from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yoblog.db'
with app.app_context():
    db = SQLAlchemy(app)


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<blog %r>' % self.id


@app.route('/')
def index():
    get_blogs = Blog.query.order_by(Blog.date_created).all()
    return render_template('index.html', posts=get_blogs)


@app.route('/add', methods=['POST'])
def add_blog():
    get_title = request.form.get('title')
    get_content = request.form.get('content')
    new_blog = Blog(title=get_title, content=get_content)
    
    try:
        db.session.add(new_blog)
        db.session.commit()
        return redirect("/")
    except:
        return 'There was an issue uploading your article'

if __name__ == "__main__":
    app.run(debug=True)