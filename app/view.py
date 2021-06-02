from app import app
from flask import render_template
from models import Post


@app.route("/")
def home_page():
    name = "Ivan"
    return render_template("home_page.html", name=name)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/blogs")
def blogs():
    posts = Post.query.all()
    return render_template("blogs.html", posts=posts)


@app.route("/<slug>")
def post_detail(slug):
    post = Post.query.filter(Post.slug==slug).first()
    return render_template("detail.html", post=post)