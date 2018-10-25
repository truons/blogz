from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1200))

    def __init__(self, title):
        self.title = title
        self.body = False

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
     
    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if request.method == 'POST':
        blog_name = request.form['blog']
        new_post = Blog(blog_name)
        db.session.add(new_post)
        db.session.commit()

    blogs = Blog.query.filter_by(completed=False).all()
    completed_blogs = Blog.query.filter_by(completed=True).all()
    return render_template('newblog.html',title="Bluid A Blog", 
        tasks=tasks, completed_tasks=completed_tasks)


@app.route('/newpost', methods=['POST'])
def newpost():

    blog_id = int(request.form['blog-id'])
    blog = Blog.query.get(blog_id)
    blog.completed = True
    db.session.add(blog)
    db.session.commit()

    return redirect('/')


if __name__ == '__main__':
    app.run()