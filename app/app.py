from flask import Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate
from flask_script import Manager

from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from flask_security import SQLAlchemyUserDatastore
from flask_security import Security, current_user

from config import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

from models import Post, Tag, User, Role


class AdminMixin:
    def is_accessible(self):
        return current_user.has_role("admin")

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("security.login", next=request.url))


class BaseModelView(ModelView):
    def on_model_change(self, form, model, is_created):
        model.generate_slug()
        return super().on_model_change(form, model, is_created)


class AdminView(AdminMixin, ModelView):
    pass


class HomeAdminView(AdminMixin, AdminIndexView):
    pass


class PostAdminView(AdminMixin, BaseModelView):
    form_columns = ["title", "body", "tags"]


class TagAdminView(AdminMixin, BaseModelView):
    form_columns = ["name", "posts"]


class UserAdminView(AdminMixin, BaseModelView):
    form_columns = ["name", "password", "email", "roles"]


admin = Admin(app, "FlaskApp", url="/", index_view=HomeAdminView(name="Home"))
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))
admin.add_view(UserAdminView(User, db.session))
admin.add_view(AdminView(Role, db.session))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
