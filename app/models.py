from app import db
from datetime import datetime
import re


def slugify(title):
    pattern = r"[^\w+]"
    return re.sub(pattern, "-", title).lower()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return f"<Post id: {self.id}, title: {self.title}>"


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return f"Tag id: {self.id}, name: {self.name}"
