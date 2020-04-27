from app.admin.forms import ClassesForm
from app.models import T_classes, T_courses, T_students, T_cshedules
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


# 添加班级
@admin.route("/class/add/", methods=["GET", "POST"])
def classes_add():
    return render_template("admin/classes_add.html")


# 编辑班级
@admin.route("/class/edit/<int:id>/", methods=["GET", "POST"])
def classes_edit(id):
    return render_template("admin/classes_edit.html")


# 班级列表
@admin.route("/class/list/<int:page>", methods=["GET", "POST"])
def classes_list(page=None):
    if page is None:
        page = 1
    page_data = T_classes.query.order_by(
        T_classes.id.asc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/classes_list.html", page_data=page_data)


# 班级删除
@admin.route("/class/del/<int:id>", methods=["GET"])
def classes_del(id=None):
    return redirect(url_for('admin.classes_list'))


# 添加课程
@admin.route("/course/add/", methods=["GET", "POST"])
def courses_add():
    return render_template("admin/courses_add.html")


# 课程删除
@admin.route("/course/del/<int:id>", methods=["GET"])
def courses_del(id=None):
    return redirect(url_for('admin.courses_list'))


# 预告修改
@admin.route("/preview/edit/<int:id>/", methods=["GET", "POST"])
def preview_edit(id=None):
    return render_template("admin/preview_edit.html")


# 课程修改
@admin.route("/course/edit/<int:id>/", methods=["GET", "POST"])
def courses_edit(id=None):
    return render_template("admin/courses_edit.html")


# 课程列表
@admin.route("/course/list/<int:page>/", methods=["GET"])
def courses_list(page=None):
    if page is None:
        page = 1
    page_data = T_courses.query.order_by(
        T_courses.cno.asc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/courses_list.html", page_data=page_data)


# 添加课程安排
@admin.route("/cshedules/add/", methods=["GET", "POST"])
def cshedules_add():
    return render_template("admin/cshedules_add.html")


# 课程安排列表
@admin.route("/cshedules/list/<int:page>/")
def cshedules_list(page=None):
    if page is None:
        page = 1
    page_data = T_cshedules.query.order_by(
        T_cshedules.id.asc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/cshedules_list.html", page_data=page_data)


# 预告删除
@admin.route("/preview/del/<int:id>", methods=["GET"])
def preview_del(id=None):
    return redirect(url_for('admin.preview_list'))


# 会员详情
@admin.route("/user/view/<int:id>")
def user_view(id=None):
    return render_template("admin/user_view.html")


# 学生管理 开始
# 学生列表
@admin.route("/students/list/<int:page>/", methods=["GET", "POST"])
def students_list(page=None):
    form = ClassesForm()
    if page is None:
        page = 1
    page_data = T_students.query.order_by(
        T_students.sclass.asc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/students_list.html", page_data=page_data, form=form)


# #  学生分班列表
# @admin.route("/students/search/<int:page>", methods=["GET", "POST"])
# def students_search(page=None):
#     form = ClassesForm()
#     if page is None:
#         page = 1
#     if request.method == "POST":
#         data = form.data
#         classes = T_classes.query.filter_by(id=data['classes']).first()
#         page_data = T_students.query.filter_by(sclass=classes.name).order_by(T_students.sno.asc()).paginate(
#             page=page, per_page=10)
#         session['classes'] = classes.name
#         return render_template("admin/student_search.html", page_data=page_data, form=form)
#     else:
#         page_data = T_students.query.filter_by(sclass=session['classes']).order_by(T_students.sno.asc()).paginate(
#             page=page, per_page=10)
#         return render_template("admin/student_search.html", page_data=page_data, form=form)
#  学生搜索列表
@admin.route("/students/search/<int:page>", methods=["GET", "POST"])
def students_search(page=None):
    form = ClassesForm()
    if page is None:
        page = 1
    if request.method == "POST":
        data = form.data
        if data['classes'] is not None:
            classes = T_classes.query.filter_by(id=data['classes']).first()
            session['classes'] = classes.name
        else:
            data = request.form.get('table_search')
            session['classes'] = data
    t_classes = T_classes.query.all()
    ls = [i.name for i in t_classes]
    if session['classes'] in ls:
        page_data = T_students.query.filter(
                    T_students.sclass.like("%" + session['classes'] + "%") if session['classes'] is not None else "",
                ).order_by(T_students.sno.asc()).paginate(
            page=page, per_page=10)
    else:
        page_data = T_students.query.filter(
                T_students.sname.like("%" + session['classes'] + "%") if session['classes'] is not None else "",
            ).order_by(T_students.sno.asc()).paginate(
        page=page, per_page=10)
    return render_template("admin/student_search.html", page_data=page_data, form=form)

# 大学生创新创业项目
@admin.route("/innovation/list/")
def innovation_list():
    return render_template("admin/innovation_list.html")


# 大学生科研项目
@admin.route("/research/list/")
def research_list():
    return render_template("admin/research_list.html")


# 竞赛获奖
@admin.route("/prize/list/")
def prize_list():
    return render_template("admin/prize_list.html")


# 学术论文
@admin.route("/thesis/list/")
def thesis_list():
    return render_template("admin/thesis_list.html")


# 专利
@admin.route("/patent/list/")
def patent_list():
    return render_template("admin/patent_list.html")


# 职业证书
@admin.route("/certificate/list/")
def certificate_list():
    return render_template("admin/certificate_list.html")


# 学生管理 结束
@admin.route("/auth/add/")
def auth_add():
    return render_template("admin/auth_add.html")


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
