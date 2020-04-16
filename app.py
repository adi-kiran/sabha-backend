from flask import Flask, request, Response, jsonify
from initialize_database import initialize_db
from models import Post,User,Comment
from re import match
from flask_cors import CORS

app = Flask(__name__)
# configure database
app.config['MONGODB_SETTINGS'] = {
    'host': 'mongodb://localhost:27017/sabha_db'
}
initialize_db(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# add a user
# requires {"username":"a unique username for the user","password":"password for the account","full_name":"users full name"}
@app.route('/api/user/add', methods=['POST'])
def add_user():
    body = request.get_json()
    for i in ["username","password","full_name"]:
        if i not in body or body[i]=="":
            return i+" required",401
    user = User.objects(username=body["username"])
    if len(user)!=0:
        return "Username already exists",400
    user = User(**body).save()
    return "User succesfully added",200

# signin api
# requires {"username":username of user,"password":password of user}
@app.route('/api/user/signin', methods=["POST"])
def signin_user():
    body = request.get_json()
    if body["username"]=="" or body["password"]=="":
        return "username and password required",400
    user = User.objects(username=body["username"])
    if len(user)==0:
        return "invalid username",401
    user = user[0]
    if user["password"]!=body["password"]:
        return "wrong password",402
    return "Signed in successfully",200

# update a users role
# default role is "student", we could have other roles like "teacher", "expert", "champion", etc
# request body requires {"username":"username of user whose role is to be updated","role":"new role"}
@app.route('/api/user/role_update',methods=["POST"])
def update_role():
    body = request.get_json()
    for i in ["username","role"]:
        if i not in body:
            return i+" required",400
    user = User.objects(username=body["username"])
    if len(user)==0:
        return "User does not exist",400
    user = user[0]
    user.role = body["role"]
    user.save()
    return "Role Modified",200

# return a list of all users and their roles and full names
@app.route('/api/user/list',methods=["GET"])
def list_all_users():
    user = User.objects.exclude("id","password","dob")
    return jsonify(user),200

# returns all posts
# no requirements, just a get request returns a list of all posts
@app.route('/api/posts', methods=['GET'])
def get_all_posts():
    posts = Post.objects().order_by('-timestamp')
    return jsonify(posts),200

# returns a post with id = id (integer)
@app.route('/api/posts/<id>',methods=['GET'])
def get_post(id):
    if len(id)==24 and (match("[a-fA-F0-9]{24}",id)):
        post = Post.objects(id=id)
        if len(post)!=0:
            post = post[0]
            return jsonify(post),200
    return "Id does not match",404

# API to retrieve all posts by a user
# request body not required
# response is a list of all posts by the user
@app.route('/api/posts/user/<user_name>',methods=["GET"])
def get_users_posts(user_name):
    user = User.objects(username=user_name)
    if len(user)==0:
        return "User does not exist",400
    else:
        posts = Post.objects(author=user_name).order_by('-timestamp')
        return jsonify(posts),200

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

# upvote a post
# request body : {"post_id":<postid>,"user":<username of user who is upvoting>}
@app.route('/api/posts/upvote',methods=["POST"])
def upvote_post():
    body = request.get_json()
    for i in ["post_id","user"]:
        if i not in body:
            return i+" required",400
    post = Post.objects(id=body["post_id"])
    if len(post)==0:
        return "post does not exist",400
    user = User.objects(username=body["user"])
    if len(user)==0:
        return "User does not exist",400
    post=post[0]
    if (body["user"] in post["upvotes"]) or (body["user"] in post["downvotes"]):
        return "Already voted",201
    post.votes = post.votes + 1
    post.upvotes.append(body["user"])
    post.save()
    return "Upvoted Successfully",200

# downvote a post
# request body : {"post_id":<postid>,"user":<username of user who is downvoting>}
@app.route('/api/posts/downvote',methods=["POST"])
def downvote_post():
    body = request.get_json()
    for i in ["post_id","user"]:
        if i not in body:
            return i+" required",400
    post = Post.objects(id=body["post_id"])
    if len(post)==0:
        return "post does not exist",400
    user = User.objects(username=body["user"])
    if len(user)==0:
        return "User does not exist",400
    post=post[0]
    if (body["user"] in post["upvotes"]) or (body["user"] in post["downvotes"]):
        return "Already voted",201
    post.votes = post.votes - 1
    post.downvotes.append(body["user"])
    post.save()
    return "Downvoted Successfully",200

# API to retrieve all posts with a keyword
# request body not required
# response is a list of all posts with keyword
@app.route('/api/posts/keyword/<key_word>',methods=["GET"])
def get_posts_by_keyword(key_word):
    posts = Post.objects.search_text(key_word).order_by('-timestamp')
    if len(posts)==0:
        return "No posts exist exist",400
    else:
        return jsonify(posts),200

app.run(debug=True)