
from flask import Flask, render_template, request, session, make_response,flash
from src.common.database import Database
from src.common.utils import Utils
from src.models.blog import Blog
from src.models.post import Post
from src.models.user import User

app=Flask(__name__)
app.secret_key="rohit"


@app.route('/')
def home_template():
    return render_template('home.html')

@app.route('/login')
def login_template():
    return render_template('login.html')

@app.route('/logout')
def logout_template():
    User.logout()
    return render_template('home.html')

@app.route('/about')
def about_template():
    return render_template('about.html')

@app.route('/contact')
def contact_template():
    return render_template('contact.html')

@app.route('/register')
def register_template():
    return render_template('register.html')

@app.before_first_request
def initialise_database():
    Database.initialise()

@app.route('/auth/login',methods=['POST'])
def login_user():
    email=request.form['email']
    password=request.form['password']

    if (email is "") or (password is ""):
        flash("Please fill email id and password")
        return render_template('login.html')

    if User.login_valid(email,password):
        User.login(email)
    else:
        flash("Invalid credentials")
        session['email']=None
        return render_template('login.html')


    return render_template('profile.html',email=session['email'])

@app.route('/auth/register',methods=['POST'])
def register_user():
    email=request.form['email']
    password=request.form['password']
    if (email is "") or (password is ""):
        flash("Please fill email id and password")
    else:
        user_data = Database.find_one('users', {'email': email})
        if not Utils.email_is_valid(email):
            flash("Your email has a invalid format.")
        elif user_data is not None:
            flash("User email id already exists!")
        else:
            User.register(email,password)
            return render_template('profile.html', email=session['email'])

    return render_template('register.html')


@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id=None):
    if user_id is not None:
        user=User.get_by_id(user_id)

    else:
        user=User.get_by_email(session['email'])

    blogs = user.get_blogs()
    return render_template("user_blogs.html",email=user.email,blogs=blogs)

@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):
    blog=Blog.from_mongo(blog_id)
    posts=blog.get_posts()

    return render_template("posts.html",posts=posts,blog_title=blog.title,blog_id=blog._id)

@app.route('/blogs/new',methods=['GET','POST'])
def create_new_blog():
    if request.method=='GET':
        return render_template('new_blog.html')
    else:
        title=request.form['title']
        description=request.form['description']
        user=User.get_by_email(session['email'])
        blog=Blog(user.email,title,description,user._id)
        blog.save_to_mongo()
        return make_response(user_blogs(user._id))

@app.route('/posts/new/<string:blog_id>',methods=['GET','POST'])
def create_new_post(blog_id):
    if request.method=='GET':
        return render_template('new_post.html',blog_id=blog_id)
    else:
        title=request.form['title']
        content=request.form['content']
        user=User.get_by_email(session['email'])
        new_post=Post(blog_id,title,content,user.email)
        new_post.save_to_mongo()
        return make_response(blog_posts(blog_id))


if __name__== '__main__':
    app.run(port=4995,debug=True)
