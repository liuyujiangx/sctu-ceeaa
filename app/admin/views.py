import json
import time

from werkzeug.security import check_password_hash

from app.admin.forms import ClassesForm, CmodulesForm
from app.models import T_classes, T_courses, T_students, T_cshedules, T_cmodules, T_competition, Admin, \
    T_teachers, T_scientific, T_teachingr, T_coursetype, T_innovation, T_prize
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


# 课程类型列表
@admin.route("/coursetype/list/<int:page>/", methods=["GET", "POST"])
@admin_login_req
def coursetype_list(page=None):
    if page is None:
        page = 1
    page_data = T_coursetype.query.order_by(
        T_coursetype.id.asc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/coursetype_list.html", page_data=page_data)


#  增加课程类型
@admin.route("/coursetype/add/", methods=["POST","GET"])
@admin_login_req
def coursetype_add():
    if request.method == "GET":
        return render_template("admin/coursetype_add.html")
    else:
        data = request.form
        t_coursetype = T_coursetype(
            name=data['name'],
        )
        db.session.add(t_coursetype)
        db.session.commit()
        flash("添加成功", "ok")
        return redirect(url_for('admin.coursetype_list', page=1))



#  删除课程类型
@admin.route("/coursetype/del/<int:id>", methods=["GET"])
@admin_login_req
def coursetype_del(id=None):
    t_coursetype = T_coursetype.query.filter_by(id=id).first()
    db.session.delete(t_coursetype)
    db.session.commit()
    flash("删除成功", "ok")
    return redirect(url_for('admin.coursetype_list', page=1))


#  修改课程类型
@admin.route("/coursetype/edit/<int:id>", methods=["GET", "POST"])
@admin_login_req
def coursetype_edit(id=None):
    if request.method == "POST":
        data = request.form
        t_coursetype = T_coursetype.query.filter_by(id=id).first()
        t_coursetype.name = data['name']

        db.session.add(t_coursetype)
        db.session.commit()
        flash("修改成功", "ok")
        return redirect(url_for('admin.coursetype_list', page=1))
    else:
        t_coursetype = T_coursetype.query.filter_by(id=id).first()
        return render_template("admin/coursetype_edit.html", data=t_coursetype)



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





# 大学生科研项目
@admin.route("/research/list/<int:page>", methods=["GET", "POST"])
@admin_login_req
def research_list(page=None):
    if page is None:
        page = 1
    page_data = T_scientific.query.order_by(
        T_scientific.id.asc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/research_list.html",page_data=page_data)

# 大学生创新创业项目
@admin.route("/innovation/list/<int:page>", methods=["GET", "POST"])
@admin_login_req
def innovation_list(page=None):
    if page is None:
        page = 1
    page_data = T_innovation.query.order_by(
        T_innovation.id.asc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/innovation_list.html",page_data=page_data)


#  增加大学生创新创业
@admin.route("/innovation/add/", methods=["POST","GET"])
@admin_login_req
def innovation_add():
    if request.method == "GET":
        return render_template("admin/innovation_add.html")
    else:
        data = request.form
        t_innovation = T_innovation(
            name=data['name'],
            sname=data['sname'],
            level=data['level'],
            grade=data['grade'],
            category=data['category'],
            sno=data['sno']
        )
        db.session.add(t_innovation)
        db.session.commit()
        flash("添加成功", "ok")
        return redirect(url_for('admin.innovation_list', page=1))



#  删除大学生创新创业
@admin.route("/innovation/del/<int:id>", methods=["GET"])
@admin_login_req
def innovation_del(id=None):
    t_innovation = T_innovation.query.filter_by(id=id).first()
    db.session.delete(t_innovation)
    db.session.commit()
    flash("删除成功", "ok")
    return redirect(url_for('admin.innovation_list', page=1))


#  修改大学生创新创业
@admin.route("/innovation/edit/<int:id>", methods=["GET", "POST"])
@admin_login_req
def innovation_edit(id=None):
    if request.method == "POST":
        data = request.form
        t_innovation = T_innovation.query.filter_by(id=id).first()
        t_innovation.sno = data['sno']
        t_innovation.sname = data['sname']
        t_innovation.name = data['name']
        t_innovation.level = data['level']
        t_innovation.grade = data['grade']
        t_innovation.category = data['category']
        db.session.add(t_innovation)
        db.session.commit()
        flash("修改成功", "ok")
        return redirect(url_for('admin.innovation_list', page=1))
    else:
        t_innovation = T_innovation.query.filter_by(id=id).first()
        return render_template("admin/innovation_edit.html", data=t_innovation)

# 竞赛获奖
@admin.route("/prize/list/<int:page>", methods=["GET", "POST"])
@admin_login_req
def prize_list(page = None):
    if page is None:
        page = 1
    page_data = T_prize.query.order_by(
        T_prize.id.asc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/prize_list.html",page_data=page_data)


#  增加获奖
@admin.route("/prize/add/", methods=["POST","GET"])
@admin_login_req
def prize_add():
    if request.method == "GET":
        return render_template("admin/prize_add.html")
    else:
        data = request.form
        t_prize = T_prize(
            name=data['name'],
            sname=data['sname'],
            level=data['level'],
            grade=data['grade'],
            award=data['award'],
            sno=data['sno'],
            p_time=data['p_time']
        )
        db.session.add(t_prize)
        db.session.commit()
        flash("添加成功", "ok")
        return redirect(url_for('admin.prize_list', page=1))



#  删除获奖
@admin.route("/竞赛获奖/del/<int:id>", methods=["GET"])
@admin_login_req
def prize_del(id=None):
    t_prize = T_prize.query.filter_by(id=id).first()
    db.session.delete(t_prize)
    db.session.commit()
    flash("删除成功", "ok")
    return redirect(url_for('admin.prize_list', page=1))


#  修改获奖
@admin.route("/prize/edit/<int:id>", methods=["GET", "POST"])
@admin_login_req
def prize_edit(id=None):
    if request.method == "POST":
        data = request.form
        t_prize = T_prize.query.filter_by(id=id).first()
        t_prize.sno = data['sno']
        t_prize.sname = data['sname']
        t_prize.name = data['name']
        t_prize.level = data['level']
        t_prize.grade = data['grade']
        t_prize.p_time = data['p_time']
        t_prize.award = data['award']
        db.session.add(t_prize)
        db.session.commit()
        flash("修改成功", "ok")
        return redirect(url_for('admin.prize_list', page=1))
    else:
        t_prize = T_prize.query.filter_by(id=id).first()
        return render_template("admin/prize_edit.html", data=t_prize)

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


#  教师信息管理
@admin.route("/teachers/list/<int:page>", methods=["GET", "POST"])
@admin_login_req
def teachers_list(page=None):
    if page is None:
        page = 1
    page_data = T_teachers.query.order_by(
        T_teachers.id.asc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/teachers_list.html", page_data=page_data)


#  增加教师
@admin.route("/teachers/add/", methods=["POST","GET"])
@admin_login_req
def teachers_add():
    if request.method == "GET":
        return render_template("admin/teachers_add.html")
    else:
        data = request.form
        t_teachers = T_teachers(
            name=data['name'],
            age=data['age'],
            title=data['title'],
            education=data['education'],
            degree=data['degree'],
            year=data['year']
        )
        db.session.add(t_teachers)
        db.session.commit()
        flash("添加成功", "ok")
        return redirect(url_for('admin.teachers_list', page=1))



#  删除教师
@admin.route("/teachers/del/<int:id>", methods=["GET"])
@admin_login_req
def teachers_del(id=None):
    t_teachers = T_teachers.query.filter_by(id=id).first()
    db.session.delete(t_teachers)
    db.session.commit()
    flash("删除成功", "ok")
    return redirect(url_for('admin.teachers_list', page=1))


#  修改教师
@admin.route("/teachers/edit/<int:id>", methods=["GET", "POST"])
@admin_login_req
def teachers_edit(id=None):
    if request.method == "POST":
        data = request.form
        t_teachers = T_teachers.query.filter_by(id=id).first()
        t_teachers.name = data['name']
        t_teachers.age = data['age']
        t_teachers.title = data['title']
        t_teachers.education = data['education']
        t_teachers.degree = data['degree']
        t_teachers.year = data['year']

        db.session.add(t_teachers)
        db.session.commit()
        flash("修改成功", "ok")
        return redirect(url_for('admin.teachers_list', page=1))
    else:
        t_teachers = T_teachers.query.filter_by(id=id).first()
        return render_template("admin/teachers_edit.html", data=t_teachers)





#  科研成果
@admin.route("/scientific/list/<int:page>", methods=["GET", "POST"])
@admin_login_req
def scientific_list(page=None):
    if page is None:
        page = 1
    page_data = T_scientific.query.order_by(
        T_scientific.id.asc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/scientific_list.html", page_data=page_data)


#  增加科研
@admin.route("/scientific/add/", methods=["POST","GET"])
@admin_login_req
def scientific_add():
    if request.method == "GET":
        return render_template("admin/scientific_add.html")
    else:
        data = request.form
        t_scientific = T_scientific(
            name=data['name'],
            t_name=data['t_name'],
            number=data['number'],
            nature=data['nature'],
            category=data['category'],
            sort=data['sort'],
            funds=data['funds']
        )
        db.session.add(t_scientific)
        db.session.commit()
        flash("添加成功", "ok")
        return redirect(url_for('admin.scientific_list', page=1))



#  删除科研
@admin.route("/scientific/del/<int:id>", methods=["GET"])
@admin_login_req
def scientific_del(id=None):
    t_scientific = T_scientific.query.filter_by(id=id).first()
    db.session.delete(t_scientific)
    db.session.commit()
    flash("删除成功", "ok")
    return redirect(url_for('admin.scientific_list', page=1))


#  修改科研
@admin.route("/scientific/edit/<int:id>", methods=["GET", "POST"])
@admin_login_req
def scientific_edit(id=None):
    if request.method == "POST":
        data = request.form
        t_scientific = T_scientific.query.filter_by(id=id).first()
        t_scientific.name = data['name']
        t_scientific.t_name = data['t_name']
        t_scientific.nature = data['nature']
        t_scientific.category = data['category']
        t_scientific.sort = data['sort']
        t_scientific.funds = data['funds']
        t_scientific.number = data['number']

        db.session.add(t_scientific)
        db.session.commit()
        flash("修改成功", "ok")
        return redirect(url_for('admin.scientific_list', page=1))
    else:
        t_scientific = T_scientific.query.filter_by(id=id).first()
        return render_template("admin/scientific_edit.html", data=t_scientific)


#  教研成果
@admin.route("/teachingr/list/<int:page>", methods=["GET", "POST"])
@admin_login_req
def teachingr_list(page=None):
    if page is None:
        page = 1
    page_data = T_teachingr.query.order_by(
        T_teachingr.id.asc()
    ).paginate(page=page, per_page=10)
    return render_template("admin/teachingr_list.html", page_data=page_data)


#  增加教研
@admin.route("/teachingr/add/", methods=["POST","GET"])
@admin_login_req
def teachingr_add():
    if request.method == "GET":
        return render_template("admin/teachingr_add.html")
    else:
        data = request.form
        t_teachingr = T_teachingr(
            name=data['name'],
            t_name=data['t_name'],
            level=data['level'],
            t_num=data['t_num'],
            funds=data['funds'],
            number=data['number']
        )
        db.session.add(t_teachingr)
        db.session.commit()
        flash("添加成功", "ok")
        return redirect(url_for('admin.teachingr_list', page=1))



#  删除教研
@admin.route("/teachingr/del/<int:id>", methods=["GET"])
@admin_login_req
def teachingr_del(id=None):
    t_teachingr = T_teachingr.query.filter_by(id=id).first()
    db.session.delete(t_teachingr)
    db.session.commit()
    flash("删除成功", "ok")
    return redirect(url_for('admin.teachingr_list', page=1))


#  修改教研
@admin.route("/teachingr/edit/<int:id>", methods=["GET", "POST"])
@admin_login_req
def teachingr_edit(id=None):
    if request.method == "POST":
        data = request.form
        t_teachingr = T_teachingr.query.filter_by(id=id).first()
        t_teachingr.name = data['name']
        t_teachingr.t_name = data['t_name']
        t_teachingr.level = data['level']
        t_teachingr.t_num = data['t_num']
        t_teachingr.funds = data['funds']
        t_teachingr.number = data['number']

        db.session.add(t_teachingr)
        db.session.commit()
        flash("修改成功", "ok")
        return redirect(url_for('admin.teachingr_list', page=1))
    else:
        t_teachingr = T_teachingr.query.filter_by(id=id).first()
        return render_template("admin/teachingr_edit.html", data=t_teachingr)