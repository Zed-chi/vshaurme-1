import os
import random

from PIL import Image, ImageDraw
from faker import Faker
from flask import current_app
from sqlalchemy.exc import IntegrityError

from vshaurme.extensions import db
from vshaurme.models import User, Photo, Tag, Comment, Notification

fake = Faker("ru_RU")


def fake_admin():
    admin = User(name='Grey Li',
                 username='greyli',
                 email='admin@helloflask.com',
                 bio=fake.sentence(),
                 website='http://greyli.com',
                 confirmed=True)
    admin.set_password('helloflask')
    notification = Notification(message='Привет, добро пожаловать в сервис Вшаурме.', receiver=admin)
    db.session.add(notification)
    db.session.add(admin)
    db.session.commit()


def fake_user(count=10):
    for user_number in range(count):
        #
        name = fake.name()
        username = fake.user_name()
        location = fake.city_name()
        bio = 'Меня зовут {} и я живу в городе {}.'.format(name, location)
        website = fake.url()
        email = fake.email()
        #
        user = User(name=name,
                    confirmed=True,
                    username=username,
                    bio=bio,
                    location=location,
                    website=website,
                    email=email)
        user.set_password('123456')
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_follow(count=30):
    for _ in range(count):
        user = User.query.get(random.randint(1, User.query.count()))
        user.follow(User.query.get(random.randint(1, User.query.count())))
    db.session.commit()


def fake_tag(count=20):
    for tag_number in range(count):
        tag = Tag(name=fake.word())
        db.session.add(tag)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_photo(count=30):
    # photos
    upload_path = current_app.config['VSHAURME_UPLOAD_PATH']
    for photo_number in range(count):
        filename = 'random_%d.jpg' % photo_number
        # TODO: generate image
        
        color = (
            random.randint(0,255),
            random.randint(0,255),
            random.randint(0,255)
        )
        img = Image.new('RGB', (320, 240), color)
        imgDrawer = ImageDraw.Draw(img)
        
        img.save(os.path.join(upload_path,filename))
        photo = Photo(
            description=fake.text(),
            filename=filename,
            filename_m=filename,
            filename_s=filename,
            author=User.query.get(random.randint(1, User.query.count())),
            timestamp=fake.date_time_this_year()
        )

        # tags
        for j in range(random.randint(1, 5)):
            tag = Tag.query.get(random.randint(1, Tag.query.count()))
            if tag not in photo.tags:
                photo.tags.append(tag)

        db.session.add(photo)
    db.session.commit()


def fake_collect(count=50):
    for i in range(count):
        user = User.query.get(random.randint(1, User.query.count()))
        user.collect(Photo.query.get(random.randint(1, Photo.query.count())))
    db.session.commit()


def fake_comment(count=100):
    for i in range(count):
        comment = Comment(
            author=User.query.get(random.randint(1, User.query.count())),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            photo=Photo.query.get(random.randint(1, Photo.query.count()))
        )
        db.session.add(comment)
    db.session.commit()
