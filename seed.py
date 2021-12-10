"""Seed file to make sample user data for blogly db."""

from models import User, Post, db 
from app import app 

# Create all tables 
db.drop_all()
db.create_all()

# If table isn't empty, empty it 
User.query.delete()

# Add users 
matt = User(first_name="Matt", last_name="DeMichele", image_url="https://media-exp1.licdn.com/dms/image/D5635AQGl2MEQlb9RfQ/profile-framedphoto-shrink_200_200/0/1629318225753?e=1639170000&v=beta&t=lGyoRyccx2ZfZ2dzbRiemOXpjaKtuham_7bzUW41vt0")

stephen = User(first_name="Stephen", last_name="Curry", image_url="https://cdn.vox-cdn.com/thumbor/DD5IycTj3MzmxVcx2vTe-z1taLc=/0x0:4392x3295/1200x800/filters:focal(2090x329:2792x1031)/cdn.vox-cdn.com/uploads/chorus_image/image/70242544/usa_today_17307929.0.jpg")

# Add new objects to session, so they'll persist 
db.session.add(matt)
db.session.add(stephen)

# Commit--otherwise, this never gets saved!
db.session.commit()

# Add two posts 
post1 = Post(title="example post", content="This post is incredible!", post_author=1)
post2 = Post(title="another post", content="Wow another good one. Omy goodness.", post_author=2)

db.session.add(post1)
db.session.add(post2)

db.session.commit()