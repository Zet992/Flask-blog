from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect, url_for
from wtforms import Form, StringField, TextAreaField
from flask_security import login_required

from app import db
from models import Post


posts = Blueprint("posts", __name__,
                  template_folder="templates",
                  static_folder="static")


class PostForm(Form):
    title = StringField("Title")
    body = TextAreaField("Body")


@posts.route("/", methods=["POST", "GET"])
@login_required
def index():
    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")
        if title is not None and body is not None:
            try:
                post = Post(title=title, body=body)
                db.session.add(post)
                db.session.commit()
            except Exception as err:
                print(err)

            return redirect(url_for("blogs"))

    return render_template("posts/index.html")


@posts.route("/1", methods=["POST", "GET"])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("body")
        if title is not None and body is not None:
            try:
                post = Post(title=title, body=body)
                db.session.add(post)
                db.session.commit()
            except Exception as err:
                print(err)

            return redirect(url_for("blogs"))

    form = PostForm()
    return render_template("posts/create_post.html", form=form)
