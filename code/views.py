from flask import Blueprint, render_template, request,flash, url_for, redirect, Flask, send_file
from flask_login import login_required, current_user
import os
from .models import User, Post, Comment
from . import db, current_app
from werkzeug.utils import secure_filename

views = Blueprint("views", __name__)


@views.route('/')
def begin():
  return render_template("index.html")

@views.route('/home')
@login_required
def home():
  posts = Post.query.all()
  return render_template('homepage.html', posts=posts)

@views.route('/create-project', methods=["GET", "POST"])
@login_required
def create_post():
  if request.method == "POST":
    text = request.form.get("text")
    title = request.form.get("title")
    instuctions = request.form.get("instructions")
    #uploaded_file = request.files['file']
    post = Post(title=title,text=text, author=current_user.id,instuctions=instuctions)
    db.session.add(post)
    db.session.commit()

    id = post.id
    uploaded_file = request.files['file']

    filename = "code/static/post_imgs/" + str(id) + ".zip"
    if uploaded_file.filename != '':
        uploaded_file.save(filename)
    else:
      return "No zip given"

    
    return redirect(url_for("views.home"))

  return render_template("create_post.html")






@views.route('/give-feedback/<postid>', methods=["GET", "POST"])
@login_required
def create_comment(postid):

  post = Post.query.filter_by(id=postid).first()

  if not post:
    return "Post ID not found"
    
  if request.method == "POST":
    text = request.form.get("text")
    title = request.form.get("title")
    rating = request.form.get("rating1")



    if(int(rating) > 5):
      rating = "5"

    comment = Comment(title=title,text=text, author=current_user.id,rating = int(rating), post_id=int(postid))
    db.session.add(comment)
    db.session.commit()

    #setattr(rost, 'rating', x)


    
    return redirect(f"/post/{postid}")

  return render_template("create_comment.html")




@views.route("/post/<postid>")
def postcheck(postid): 
  post = Post.query.filter_by(id=postid).first()

  if not post:
    return "Post ID not found"


  user = current_user.id


  z =  os.path.join('static', 'post_imgs')


  x = os.path.join(z, str(post.id) + ".zip")

  img = "/"+x

  comments  = post.commments
  

  return render_template("post.html",post=post,user=user, img=img,comments=comments)


@views.route("/remove/comment/<postid>", methods=["POST","GET"])
def remove_com(postid):
  post = Comment.query.filter_by(id=postid).first()
  if not post:
    return render_template("message.html",msg="The comment ID is invalid")

  if(current_user.id != post.author):
    return render_template("message.html",msg="We don't think your the owner")

  x = str(current_user.username)
  z = str(post.title)
  z = x + "/" + z

  db.session.delete(post)
  db.session.commit()


  return redirect(f"/post/{post.post_id}")



@views.route("/remove/<postid>", methods=["POST","GET"])
def remove(postid):
  post = Post.query.filter_by(id=postid).first()
  if not post:
    return "Post ID invalid"

  if(current_user.id != post.author):
    return "YOU IS NOT OWNER"

  x = str(current_user.username)
  z = str(post.title)
  z = x + "/" + z


  db.session.delete(post)
  db.session.commit()
  os.system("pwd")
  os.system("rm code/static/post_imgs/" + str(post.id) + ".zip")


  return redirect("/home")

@views.route("/download/<postid>")
def download_img(postid):
  post = Post.query.filter_by(id=postid).first()

  if not post:
    return "Post ID not found"

  if not os.path.exists("code/static/post_imgs/" + str(post.id) + ".zip"):
    return "Post does not have an attached image"
  

  secure_filename("code/static/post_imgs/" + str(post.id) + ".zip")

  
  return send_file("static/post_imgs/" + str(post.id) + ".zip", as_attachment=True, download_name=f"BetaDownload.zip")
  


@views.route("/edit/<postid>",methods=["POST","GET"])
def edit_post(postid):
  post = Post.query.filter_by(id=postid).first()

  if not post:
    return "Post ID not found"

  if(current_user.id != post.author):
    return "YOU IS NOT OWNER"

  if(request.method == "POST"):

    setattr(post, 'title', request.form.get("title"))
    setattr(post, 'text', request.form.get("text"))
    db.session.commit()


    return "OK"

  else:
  

    z = post.title
    x = post.text

    return render_template("edit.html",title=z,text=x)

@views.route("/follow/<userid>", methods=["POST","GET"])
def add_follower(userid):
  followers = Follower.query.filter_by(id=userid).first()

  if not followers:
    return "User not found!"
  
  if(current_user.id == followers.id):
    return "Can't follow self!"

  if request.method == "POST":
    follower = Follower(follower=current_user.id)
    db.session.add(follower)
    db.session.commit()

    return redirect(url_for("views.home"))

    


@views.route("/tc")
def tc():
  return render_template('tc.html')