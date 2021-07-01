from app import app, db
from posts.blueprint import posts
import view


app.register_blueprint(posts, url_prefix="/create_blog")

if __name__ == "__main__":
    app.run()
