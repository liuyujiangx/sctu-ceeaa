from . import admin

from flask import render_template, redirect, url_for, flash, session, request
from functools import wraps
from app import db, app
from werkzeug.utils import secure_filename
import os
import uuid
import datetime


def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


@admin.route("/")
def index():
    return render_template("admin/index.html")


# 登录
@admin.route("/login/", methods=["GET", "POST"])
def login():
    return render_template("admin/login.html")


# 退出
@admin.route("/logout/")
def logout():
    session.pop("account", None)
    return redirect(url_for("admin.login"))


# 修改密码
@admin.route("/pwd/")
def pwd():
    return render_template("admin/pwd.html")


# 添加标签
@admin.route("/tag/add/", methods=["GET", "POST"])
def tag_add():
    return render_template("admin/tag_add.html")


# 编辑标签
@admin.route("/tag/edit/<int:id>/", methods=["GET", "POST"])
def tag_edit(id):
    return render_template("admin/tag_edit.html")


# 标签列表
@admin.route("/tag/list/<int:page>", methods=["GET"])
def tag_list(page=None):
    return render_template("admin/tag_list.html")


# 标签删除
@admin.route("/tag/del/<int:id>", methods=["GET"])
def tag_del(id=None):
    return redirect(url_for('admin.tag_list'))


# 添加电影
@admin.route("/movie/add/", methods=["GET", "POST"])
def movie_add():
    return render_template("admin/movie_add.html")


# 电影删除
@admin.route("/movie/del/<int:id>", methods=["GET"])
def movie_del(id=None):
    return redirect(url_for('admin.movie_list'))


# 预告修改
@admin.route("/preview/edit/<int:id>/", methods=["GET", "POST"])
def preview_edit(id=None):
    return render_template("admin/preview_edit.html")


# 电影修改
@admin.route("/movie/edit/<int:id>/", methods=["GET", "POST"])
def movie_edit(id=None):
    return render_template("admin/movie_edit.html")


# 电影列表
@admin.route("/movie/list/<int:page>/", methods=["GET"])
def movie_list(page=None):
    return render_template("admin/movie_list.html")


# 添加预告
@admin.route("/preview/add/", methods=["GET", "POST"])
def preview_add():
    return render_template("admin/preview_add.html")


# 预告列表
@admin.route("/preview/list/<int:page>/")
def preview_list(page=None):
    return render_template("admin/preview_list.html")


# 预告删除
@admin.route("/preview/del/<int:id>", methods=["GET"])
def preview_del(id=None):
    return redirect(url_for('admin.preview_list'))


# 会员详情
@admin.route("/user/view/<int:id>")
def user_view(id=None):
    return render_template("admin/user_view.html")


# 会员列表
@admin.route("/user/list/<int:page>/")
def user_list(page=None):
    return render_template("admin/user_list.html",)


@admin.route("/comment/list/")
def comment_list():
    return render_template("admin/comment_list.html")


@admin.route("/moviecol/list/")
def moviecol_list():
    return render_template("admin/moviecol_list.html")


@admin.route("/oplog/list/")
def oplog_list():
    return render_template("admin/oplog_list.html")


@admin.route("/adminloginlog/list/")
def adminloginlog_list():
    return render_template("admin/adminloginlog_list.html")


@admin.route("/userloginlog/list/")
def userloginlog_list():
    return render_template("admin/userloginlog_list.html")


@admin.route("/auth/add/")
def auth_add():
    return render_template("admin/auth_add.html")


@admin.route("/auth/list/")
def auth_list():
    return render_template("admin/auth_list.html")


@admin.route("/role/add/")
def role_add():
    return render_template("admin/role_add.html")


@admin.route("/role/list/")
def role_list():
    return render_template("admin/role_list.html")


@admin.route("/admin/add/")
def admin_add():
    return render_template("admin/admin_add.html")


@admin.route("/admin/list/")
def admin_list():
    return render_template("admin/admin_list.html")
