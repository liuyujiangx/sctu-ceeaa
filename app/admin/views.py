import json
import time

from werkzeug.security import check_password_hash

from app.admin.forms import ClassesForm, CmodulesForm
from app.models import T_classes, T_courses, T_students, T_cshedules, T_cmodules, T_competition, Admin
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
@admin_login_req
def index():
    return render_template("admin/index.html")



# 登录
@admin.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        if len(data['user']) == 0 or len(data['pwd']) == 0:
            flash("请输入账号或密码",'err')
            print('12312')
            return redirect(url_for("admin.login"))
        admin = Admin.query.filter_by(name=data["user"]).first()
        admincount = Admin.query.filter_by(name=data["user"]).count()
        if admincount == 0:
            flash("密码账号或错误", 'err')
            return redirect(url_for("admin.login"))
        if not admin.check_pwd(data["pwd"]):
            flash("密码账号或错误",'err')
            return redirect(url_for("admin.login"))
        session["admin"] = data["user"]
        return redirect(request.args.get('next', url_for('admin.index')))


    return render_template("admin/login.html")


# 退出
@admin.route("/logout/")
@admin_login_req
def logout():
    session.pop("admin", None)
    return redirect(url_for("admin.login"))


# 修改密码
@admin.route("/pwd/")
@admin_login_req
def pwd():
    return render_template("admin/pwd.html")


# 添加班级
@admin.route("/class/add/", methods=["GET", "POST"])
@admin_login_req
def classes_add():
    return render_template("admin/classes_add.html")


# 编辑班级
@admin.route("/class/edit/<int:id>/", methods=["GET", "POST"])
@admin_login_req
def classes_edit(id):
    return render_template("admin/classes_edit.html")


# 班级列表
@admin.route("/class/list/<int:page>", methods=["GET", "POST"])
@admin_login_req
def classes_list(page=None):
    if page is None:
        page = 1
    page_data = T_classes.query.order_by(
        T_classes.id.asc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/classes_list.html", page_data=page_data)


# 班级删除
@admin.route("/class/del/<int:id>", methods=["GET"])
@admin_login_req
def classes_del(id=None):
    return redirect(url_for('admin.classes_list'))


# 添加课程
@admin.route("/course/add/", methods=["GET", "POST"])
@admin_login_req
def courses_add():
    return render_template("admin/courses_add.html")


# 课程删除
@admin.route("/course/del/<int:id>", methods=["GET"])
@admin_login_req
def courses_del(id=None):
    return redirect(url_for('admin.courses_list'))


# 预告修改
@admin.route("/preview/edit/<int:id>/", methods=["GET", "POST"])
@admin_login_req
def preview_edit(id=None):
    return render_template("admin/preview_edit.html")


# 课程修改
@admin.route("/course/edit/<int:id>/", methods=["GET", "POST"])
@admin_login_req
def courses_edit(id=None):
    return render_template("admin/courses_edit.html")


# 课程列表
@admin.route("/course/list/<int:page>/", methods=["GET"])
@admin_login_req
def courses_list(page=None):
    if page is None:
        page = 1
    page_data = T_courses.query.order_by(
        T_courses.cno.asc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/courses_list.html", page_data=page_data)


# 添加课程安排
@admin.route("/cshedules/add/", methods=["GET", "POST"])
@admin_login_req
def cshedules_add():
    return render_template("admin/cshedules_add.html")


# 课程安排列表
@admin.route("/cshedules/list/<int:page>/")
@admin_login_req
def cshedules_list(page=None):
    if page is None:
        page = 1
    page_data = T_cshedules.query.order_by(
        T_cshedules.id.asc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/cshedules_list.html", page_data=page_data)


# 预告删除
@admin.route("/preview/del/<int:id>", methods=["GET"])
@admin_login_req
def preview_del(id=None):
    return redirect(url_for('admin.preview_list'))


# 会员详情
@admin.route("/user/view/<int:id>")
@admin_login_req
def user_view(id=None):
    return render_template("admin/user_view.html")


# 学生管理 开始
# 学生列表
@admin.route("/students/list/<int:page>/", methods=["GET", "POST"])
@admin_login_req
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
@admin_login_req
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
@admin_login_req
def innovation_list():
    return render_template("admin/innovation_list.html")


# 大学生科研项目
@admin.route("/research/list/")
@admin_login_req
def research_list():
    return render_template("admin/research_list.html")


# 竞赛获奖
@admin.route("/prize/list/")
@admin_login_req
def prize_list():
    return render_template("admin/prize_list.html")


# 学术论文
@admin.route("/thesis/list/")
@admin_login_req
def thesis_list():
    return render_template("admin/thesis_list.html")


# 专利
@admin.route("/patent/list/")
@admin_login_req
def patent_list():
    return render_template("admin/patent_list.html")


# 职业证书
@admin.route("/certificate/list/")
@admin_login_req
def certificate_list():
    return render_template("admin/certificate_list.html")


# 学生管理 结束
@admin.route("/auth/add/")
@admin_login_req
def auth_add():
    return render_template("admin/auth_add.html")


@admin.route("/role/add/")
@admin_login_req
def role_add():
    return render_template("admin/role_add.html")


#  课程模块
@admin.route("/cmodules/list/<int:page>", methods=["GET", "POST"])
@admin_login_req
def cmodules_list(page=None):
    form = CmodulesForm()
    page_data = T_cmodules.query.order_by(
        T_cmodules.id.asc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/cmodules_list.html", page_data=page_data, form=form)


#  课程模块搜索
@admin.route("/cmodules/search/<int:page>", methods=["GET", "POST"])
@admin_login_req
def cmodules_search(page=None):
    form = CmodulesForm()
    if page is None:
        page = 1
    if request.method == "POST":
        data = form.data
        cmodule_name = T_cmodules.query.filter_by(id=data['cmodules']).first()
        session['cmodule'] = cmodule_name.name
    page_data = T_cmodules.query.filter_by(name=session['cmodule']).order_by(
        T_cmodules.id.asc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/cmodules_search.html", page_data=page_data, form=form)





@admin.route("/admin/add/", methods=["POST","GET"])
@admin_login_req
def admin_add():
    if request.method == "POST":
        data = request.form
        admin_name = Admin.query.filter_by(name=data['name']).count()
        if admin_name!=0:
            flash('用户名已存在','err')
            return redirect(url_for('admin.admin_add'))
        if data['pwd'] != data.get('repwd'):
            flash('两次密码不一致','err')
            return redirect(url_for('admin.admin_add'))
        from werkzeug.security import generate_password_hash
        admin = Admin(
            name = data['name'],
            pwd = generate_password_hash(data['pwd']),
            is_super = 0
        )
        db.session.add(admin)
        db.session.commit()
        flash('添加成功', 'ok')
        return redirect(url_for('admin.admin_add'))
    return render_template("admin/admin_add.html")


@admin.route("/admin/list/")
@admin_login_req
def admin_list():
    return render_template("admin/admin_list.html")


#  竞赛管理
@admin.route("/competition/list/<int:page>", methods=["GET", "POST"])
@admin_login_req
def competition_list(page=None):
    if page is None:
        page = 1
    page_data = T_competition.query.order_by(
        T_competition.id.asc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/competition_list.html", page_data=page_data)


#  增加竞赛
@admin.route("/competition/add/", methods=["POST","GET"])
@admin_login_req
def competition_add():
    if request.method == "GET":
        return render_template("admin/competition_add.html")
    else:
        data = request.form
        t_competition = T_competition(
            name=data['name'],
            af_name=data['af_name'],
            organizer=data['organizer'],
            undertaker=data['undertaker'],
            co_organizer=data['co_organizer'],
            url=data['url']
        )
        db.session.add(t_competition)
        db.session.commit()
        flash("添加成功", "ok")
        return redirect(url_for('admin.competition_list', page=1))



#  删除竞赛
@admin.route("/competition/del/<int:id>", methods=["GET"])
@admin_login_req
def competition_del(id=None):
    t_competition = T_competition.query.filter_by(id=id).first()
    db.session.delete(t_competition)
    db.session.commit()
    flash("删除成功", "ok")
    return redirect(url_for('admin.competition_list', page=1))


#  修改竞赛
@admin.route("/competition/edit/<int:id>", methods=["GET", "POST"])
@admin_login_req
def competition_edit(id=None):
    if request.method == "POST":
        data = request.form
        t_competition = T_competition.query.filter_by(id=id).first()
        t_competition.name = data['name']
        t_competition.af_name = data['af_name']
        t_competition.organizer = data['organizer']
        t_competition.undertaker = data['undertaker']
        t_competition.co_organizer = data['co_organizer']
        t_competition.url = data['url']

        db.session.add(t_competition)
        db.session.commit()
        flash("修改成功", "ok")
        return redirect(url_for('admin.competition_list', page=1))
    else:
        t_competition = T_competition.query.filter_by(id=id).first()
        return render_template("admin/competition_edit.html", data=t_competition)
