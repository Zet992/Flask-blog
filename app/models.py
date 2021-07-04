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
post_comments = db.Table("post_comments",
                         db.Column("post_id", db.Integer,
                                   db.ForeignKey("post.id")),
                         db.Column("comment_id", db.Integer,
                                   db.ForeignKey("comment.id"))
                         )


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.Text)
    slug = db.Column(db.String(140), unique=True)
    created = db.Column(db.DateTime, default=datetime.now())
    comments = db.relationship("Comment", secondary=post_comments,
                               backref=db.backref("posts", lazy="dynamic"))

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
        if self.name:
            self.slug = slugify(self.name)

    def __repr__(self):
        return f"Tag id: {self.id}, name: {self.name}"


roles_users = db.Table("roles_users",
                       db.Column("user_id", db.Integer(),
                                 db.ForeignKey("user.id")),
                       db.Column("role_id", db.Integer(),
                                 db.ForeignKey("role.id"))
                       )
comments_users = db.Table("comments_users",
                       db.Column("user_id", db.Integer(),
                                 db.ForeignKey("user.id")),
                       db.Column("comment_id", db.Integer(),
                                 db.ForeignKey("comment.id"))
                       )
comments_disliked_users = db.Table("comment_disliked_users",
                                   db.Column("user_id", db.Integer(),
                                             db.ForeignKey("user.id")),
                                   db.Column("comment_id", db.Integer(),
                                             db.ForeignKey("comment.id"))
                                   )
comments_liked_users = db.Table("comment_liked_users",
                                   db.Column("user_id", db.Integer(),
                                             db.ForeignKey("user.id")),
                                   db.Column("comment_id", db.Integer(),
                                             db.ForeignKey("comment.id"))
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
    comments = db.relationship("Comment", secondary=comments_users,
                               backref=db.backref("users", lazy="dynamic"))
    profile_image = db.Column(db.String(140), default="default.png")
    rating = db.Column(db.Integer(), default=0)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def generate_slug(self):
        if self.name:
            self.slug = slugify(self.name)

    def __repr__(self):
        return f"User id: {self.id}, name: {self.name}"


class Role(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(140), unique=True)
    description = db.Column(db.String(140))

    def __repr__(self):
        return f"Role id: {self.id}, name: {self.name}"


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.Text)
    rating = db.Column(db.Integer(), default=0)
    created = db.Column(db.DateTime, default=datetime.now())
    disliked_users = db.relationship("User", secondary=comments_disliked_users,
                               backref=db.backref("disliked_comments",
                                                  lazy="dynamic"))
    liked_users = db.relationship("User", secondary=comments_liked_users,
                               backref=db.backref("liked_comments",
                                                  lazy="dynamic"))

    def __repr__(self):
        return f"Comment id: {self.id} rating: {self.rating}"
