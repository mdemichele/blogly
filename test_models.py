from unittest import TestCase
from app import app 
from models import db, User

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
        
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        
        
    def tearDown(self):
        """Clean up any fouled transactions"""
        
        db.session.rollback()
        
    # Test get all users
    def test_get_users(self):
        """Test should get all users in database"""
        # Get all users 
        users = User.query.all()
        
        # Check that there is exactly 1 user in the database 
        self.assertEquals(len(users), 2)
    
        
        
    
    
    
    
     
     