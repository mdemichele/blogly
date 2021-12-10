from flask_sqlalchemy import SQLAlchemy 
import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    db.app = app 
    db.init_app(app)

# User Model 
class User(db.Model):
    """Defines a user"""
    
    __tablename__ = "users"
    
    def __repr__(self):
        return f"<User id={self.id} first_name={self.first_name} last_name={self.last_name}>"
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    
# Post Model 
class Post(db.Model):
    """Defines a post"""
    
    __tablename__ = "posts"
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(500), nullable=False)
    content = db.Column(db.String(50000), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    post_author = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', backref='posts')
    
    tags = db.relationship('Tag', secondary='posts_tags', backref='posts')
    
# Tag Model 
class Tag(db.Model):
    """Defines a tag"""
    
    __tablename__ = "tags"
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    
    
# PostTag model
class PostTag(db.Model):
    """Defines a post-tag"""
    
    __tablename__ = "posts_tags"
    
    post_id = db.Column(db.Integer, 
                        db.ForeignKey("posts.id"), 
                        primary_key=True,
                        nullable=False)
    tag_id = db.Column(db.Integer, 
                        db.ForeignKey("tags.id"), 
                        primary_key=True, 
                        nullable=False)

    
        
                        
    