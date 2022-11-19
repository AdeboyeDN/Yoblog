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


@app.route('/delete/<int:id>')
def delete_blog(id):
    blog_to_delete = Blog.query.get_or_404(id)

    try:
        db.session.delete(blog_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting this article'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_blog(id):
    blog = Blog.query.get_or_404(id)

    if request.method == 'POST':
        blog.title = request.form['title']
        blog.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your blog post'

    else:
        return render_template('update.html', blog=blog)


if __name__ == "__main__":
    app.run(debug=True)