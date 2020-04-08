from initialize_database import db
import datetime

class Comment(db.EmbeddedDocument):
    author = db.StringField(required=True)
    description = db.StringField(required=True)
    timestamp = db.DateTimeField(default=datetime.datetime.now)
    

class Post(db.Document):
    author = db.StringField(required=True)
    title = db.StringField(required=True)
    description = db.StringField(required=True)
    comments = db.ListField(db.EmbeddedDocumentField(Comment))
    votes = db.IntField(default=0)
    upvotes = db.ListField(db.StringField())
    downvotes = db.ListField(db.StringField())
    timestamp = db.DateTimeField(default=datetime.datetime.now)

    meta = {'indexes': [
        {'fields': ['$title', '$description'],
         'default_language': 'english',
        }
    ]}

class User(db.Document):
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    role = db.StringField(default="student")
    full_name = db.StringField(required=True)
    email = db.StringField(default="")
    dob = db.DateTimeField(default=datetime.datetime.now)
    phone = db.StringField(default="")