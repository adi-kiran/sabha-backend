from flask import Flask, request, Response, jsonify
from initialize_database import initialize_db
from models import Post,User,Comment
from re import match

app = Flask(__name__)
# configure database
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost:27017/hello'
}
initialize_db(app)

# add a user
# requires {"username":"a unique username for the user","password":"password for the account","full_name":"users full name"}
@app.route('/api/user/add', methods=['PUT'])
def add_user():
    body = request.get_json()
    for i in ["username","password","full_name"]:
        if i not in body:
            return i+" required",400
    user = User.objects(username=body["username"])
    if len(user)!=0:
        return "Username already exists",400
    user = User(**body).save()
    return "User succesfully added",200

# returns all posts
# no requirements, just a get request returns a list of all posts
@app.route('/api/posts', methods=['GET'])
def get_all_posts():
    posts = Post.objects()
    return jsonify(posts),200

# returns a post with id = id (integer)
@app.route('/api/posts/<id>',methods=['GET'])
def get_post(id):
    if len(id)==24 and (match("[a-fA-F0-9]{24}",id)):
        post = Post.objects(id=id)
        if len(post)!=0:
            return jsonify(post),200
    return "Id does not match",404

# add a post
# requires {"author":"username of post writer","title":"title of post","description":"post details"}
# returns "id". this id must be added to post frontend, and everytime someone upvotes/downvotes/comments, the id must be sent back
@app.route('/api/posts/add', methods=['POST'])
def add_post():
    body = request.get_json()
    for i in ["author","title","description"]:
        if i not in body:
            return i+" required",400
    user = User.objects(username=body["author"])
    if len(user)==0:
        return "User does not exist",400
    post = Post(**body).save()
    id = post.id
    return jsonify({'id': str(id)}), 200


# add a comment to a post
# requires {"post_id":"id of post to which comment is added", "author":"username of comment writer", "description":"comment beng added"}
@app.route('/api/posts/comment/add',methods=["POST"])
def add_comment():
    body = request.get_json()
    for i in ["author","description","post_id"]:
        if i not in body:
            return i+" required",400
    user = User.objects(username=body["author"])
    if len(user)==0:
        return "User does not exist",400
    comment = Comment(author=body['author'], description=body['description'])
    post = Post.objects(id=body["post_id"])
    if len(post)==0:
        return "Post does not exist (maybe deleted)",400
    post=post[0] #it returns a list with a single post
    post.comments.append(comment)
    post.save()
    return "Comment added successfully",200

app.run()