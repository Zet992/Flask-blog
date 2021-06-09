from flask import Blueprint
from flask import render_template


posts = Blueprint("posts", __name__,
                  template_folder="templates",
                  static_folder="static")

@posts.route("/")
def index():
    return render_template("posts/index.html")
