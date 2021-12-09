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
    
    def test_home_page(self):
        """Tests that requests to / redirect"""
        with app.test_client() as client:
            response = client.get('/', follow_redirects=True)
            html = response.get_data(as_text=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1 id="home-title">Users</h1>', html)
        
    def test_users_list(self):
        """Tests that the users page sucessfully shows up"""
        with app.test_client() as client:
            response = client.get('/users')
            html = response.get_data(as_text=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('<h1 id="home-title">Users</h1>', html)
        
    def test_add_user(self):
        """Tests adding a user"""
        with app.test_client() as client:
            data = {"first-name": "Tommy", "last-name": "Timmy", "image-url": "dumb.com"}
            response = client.post('/users/new', data=data, follow_redirects=True)
            html = response.get_data(as_text=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn('<a href="/users/5">Tommy Timmy</a>', html)
        
    def test_delete_user(self):
        """Tests deleting a user"""
        with app.test_client() as client:
            response = client.get('/users/1/delete', follow_redirects=True)
            html = response.get_data(as_text=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertNotIn('<a href="/users/1">Matt DeMichele</a>', html)