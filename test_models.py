from unittest import TestCase
from app import app 
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTests(TestCase):
    
    def setUp(self):
        """Clean up any existing users."""
        User.query.delete()
        
        user1 = User(first_name="Matt", last_name="DeMichele", image_url="eaaafdfa.com")
        user2 = User(first_name="Dan", last_name="Hooker", image_url="afdadfaal.com")
        
        # post1 = Post(title="Simple Post", content="It is what it is.", post_author=1)
        # post2 = Post(title="Another Post", content="Again, so it is.", post_author=2)
        
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
        # db.session.add(post1)
        # db.session.add(post2)
        # db.session.commit()
        
        
    def tearDown(self):
        """Clean up any fouled transactions"""
        
        db.session.rollback()
        
    # Test get all users
    def test_get_users(self):
        """Test should get all users in database"""
        # Get all users 
        users = User.query.all()
        
        # Check that there are exactly 2 users in the database 
        self.assertEquals(len(users), 2)
    # 
    # def test_get_posts(self):
    #     """Test should get all posts in database"""
    #     # Get all posts 
    #     posts = Post.query.all()
        
        # check that there are exactly 2 posts in the database
    
        
        
    
    
    
    
     
     