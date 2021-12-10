from flask import Flask, request, render_template, redirect, flash, session 
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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
    
    tags = Tag.query.all()
    
    return render_template('create_post.html', user=user, tags=tags)
    
@app.route('/users/<userId>/posts/new', methods=["POST"])
def create_post(userId):
    """Adds post to database and redirects to homepage"""
    title = request.form["post-title"]
    content = request.form["post-content"]
    tags = request.form.getlist("post-tag")
    
    # Create post object 
    newPost = Post(title=title, content=content, post_author=userId)
    
    # Add new post object to database 
    db.session.add(newPost)
    db.session.commit()
    
    # Add to posts_tags table 
    for tag in tags:
        currentTag = Tag.query.filter_by(name=tag).first()
        currentPost = Post.query.filter_by(title=title).first()
        newPostTag = PostTag(post_id=currentPost.id, tag_id=currentTag.id)
        db.session.add(newPostTag)
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
    
    tags = Tag.query.all()
    
    return render_template('post_edit.html', post=post, tags=tags)

@app.route('/posts/<postId>/edit', methods=["POST"])
def edit_post(postId):
    """Edits a post"""
    newPostTitle = request.form["post-title"]
    newPostContent = request.form["post-content"]
    newTags = request.form.getlist("post-tag")
    
    # Create new post object 
    newPost = Post.query.get(postId)
    
    newPost.title = newPostTitle
    newPost.content = newPostContent 
    
    # Add new post object to database 
    db.session.add(newPost)
    db.session.commit()
    
    # Get new post's tags 
    updatedPost = Post.query.filter_by(title=newPostTitle).first()
    currentTags = updatedPost.tags
    
    # Delete the current tags 
    for tag in currentTags:
        PostTag.query.filter_by(post_id=updatedPost.id, tag_id=tag.id).delete()
    
    # Add new tags to posts_tags table 
    for tag in newTags:
        currentTag = Tag.query.filter_by(name=tag).first()
        newPostTag = PostTag(post_id=updatedPost.id, tag_id=currentTag.id)
        db.session.add(newPostTag)
        db.session.commit()
    
    db.session.add(newPost)
    db.session.commit()
    
    return redirect('/')

@app.route('/posts/<postId>/delete')
def delete_post(postId):
    """Deletes a post"""
    Post.query.filter_by(id=postId).delete()
    
    db.session.commit()
    
    return redirect('/')

# Tags Routes 
@app.route('/tags/new')
def get_create_tags_page():
    """Gets the new tags form page"""
    return render_template("create_tag.html")

@app.route('/tags/new', methods=["POST"])
def create_tag():
    """Creates a new tag"""
    tagName = request.form["tag-name"]
    
    tag = Tag(name=tagName)
    
    db.session.add(tag)
    db.session.commit()
    
    return redirect('/')
    
@app.route('/tags/<tagId>/edit')
def get_edit_tags_page(tagId):
    """Gets the edit tag form page"""
    tag = Tag.query.get(tagId)
    
    return render_template("tag_edit.html", tag=tag)

@app.route('/tags/<tagId>/edit', methods=["POST"])
def edit_tag(tagId):
    """Edits a tag"""
    tag = Tag.query.get(tagId)
    
    newName = request.form["edit-tag-name"]
    
    tag.name = newName 
    
    db.session.add(tag)
    db.session.commit()
    return redirect('/')
    
@app.route('/tags')
def get_tags_page():
    """Gets the tags list"""
    tags = Tag.query.all()
    
    return render_template("tag_list.html", tags=tags)
    
@app.route('/tags/<tagId>')
def get_tag_details_page(tagId):
    """Gets the tag details page"""
    
    tag = Tag.query.get(tagId)

    return render_template("tag_details.html", tag=tag)
    
@app.route("/tags/<tagId>/delete")
def delete_tag(tagId):
    Tag.query.filter_by(id=tagId).delete()
    
    db.session.commit()
    
    return redirect("/")

