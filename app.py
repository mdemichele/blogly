from flask import Flask, request, render_template, redirect, flash, session 
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True 
app.config['SECRET_KEY'] = 'anothersecretanotherseason'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
app.config['TESTING'] = True
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page():
    """Shows Home page"""
    return redirect('/users')
    
@app.route('/users')
def users_page():
    users = User.query.all()
    
    return render_template('user_list.html', users=users)
    
@app.route('/users/new')
def get_create_user_page():
    return render_template('create_user.html')
    
@app.route('/users/new', methods=["POST"])
def create_new_user():
    # Get data from request 
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]
    
    # Create new user object to insert into database 
    newUser = User(first_name=first_name, last_name=last_name, image_url=image_url)
    
    # Insert new user into database 
    db.session.add(newUser)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<userId>')
def get_user_details_page(userId):
    """Get the user details page"""
    # Get the user from the data 
    user = User.query.get(userId)
    
    # Get the user's posts 
    posts = user.posts
    
    return render_template('user_details.html', user=user, posts=posts)
    
@app.route('/users/<userId>/edit')
def get_edit_user_page(userId):
    # Find user in database 
    user = User.query.get(userId)
    
    return render_template('user_edit.html', user=user)
    
@app.route('/users/<userId>/edit', methods=["POST"])
def edit_user(userId):
    # Find user in database 
    user = User.query.get(userId)
    
    # Get new data from request 
    new_first_name = request.form["first-name"]
    new_last_name = request.form["last-name"]
    new_image_url = request.form["image-url"]
    
    # Update existing user 
    user.first_name = new_first_name
    user.last_name = new_last_name 
    user.image_url = new_image_url 
    
    # Add updated user to database 
    db.session.add(user)
    db.session.commit()
    
    return redirect('/users')
    
@app.route('/users/<userId>/delete')
def delete_user(userId):
    
    # Find user in database 
    User.query.filter_by(id=userId).delete()

    # update db session 
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<userId>/posts/new')
def get_create_post_page(userId):
    """Shows form to add a post for the specified user"""
    user = User.query.get(userId)
    
    return render_template('create_post.html', user=user)
    
@app.route('/users/<userId>/posts/new', methods=["POST"])
def create_post(userId):
    """Adds post to database and redirects to homepage"""
    title = request.form["post-title"]
    content = request.form["post-content"]
    
    # Create post object 
    newPost = Post(title=title, content=content, post_author=userId)
    
    # Add new post object to database 
    db.session.add(newPost)
    db.session.commit()
    
    return redirect('/')

@app.route('/posts/<postId>')
def get_post_details_page(postId):
    """Gets the post details page for the specified post"""
    post = Post.query.get(postId)
    
    return render_template('post_details.html', post=post)
    
@app.route('/posts/<postId>/edit')
def get_post_edit_page(postId):
    """Gets the post edit page for the specified post"""
    post = Post.query.get(postId)
    
    return render_template('post_edit.html', post=post)

@app.route('/posts/<postId>/edit', methods=["POST"])
def edit_post(postId):
    """Edits a post"""
    newPostTitle = request.form["post-title"]
    newPostContent = request.form["post-content"]
    
    newPost = Post.query.get(postId)

    newPost.title = newPostTitle
    newPost.content = newPostContent 
    
    db.session.add(newPost)
    db.session.commit()
    
    return redirect('/')

@app.route('/posts/<postId>/delete')
def delete_post(postId):
    """Deletes a post"""
    Post.query.filter_by(id=postId).delete()
    
    db.session.commit()
    
    return redirect('/')


