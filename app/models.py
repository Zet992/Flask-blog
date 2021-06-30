from datetime import datetime
import re

from flask_security import UserMixin, RoleMixin

from app import db


def slugify(title):
    pattern = r"[^\w+]"
    return re.sub(pattern, "-", title).lower()


post_tags = db.Table("post_tags",
                     db.Column("post_id", db.Integer,
                               db.ForeignKey("post.id")),
                     db.Column("tag_id", db.Integer,
                               db.ForeignKey("tag.id"))
                     )


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.Text)
    slug = db.Column(db.String(140), unique=True)
    created = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    tags = db.relationship('Tag', secondary=post_tags,
                           backref=db.backref('posts', lazy="dynamic"))

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return f"<Post id: {self.id}, title: {self.title}>"


class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(140), unique=True)

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return f"Tag id: {self.id}, name: {self.name}"


roles_users = db.Table("roles_users",
                       db.Column("user_id", db.Integer(),
                                 db.ForeignKey("user.id")),
                       db.Column("role_id", db.Integer(),
                                 db.ForeignKey("role.id"))
                       )

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(140))
    password = db.Column(db.String(140))
    email = db.Column(db.String(140), unique=True)
    slug = db.Column(db.String(140), unique=True)
    created = db.Column(db.DateTime, default=datetime.now())
    active = db.Column(db.Boolean())
    roles = db.relationship("Role", secondary=roles_users,
                            backref=db.backref("users", lazy="dynamic"))

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return f"User id: {self.id}, name: {self.name}"


class Role(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(140), unique=True)
    description = db.Column(db.String(140))

    def __repr__(self):
        return f"Role id: {self.id}, name: {self.name}"
