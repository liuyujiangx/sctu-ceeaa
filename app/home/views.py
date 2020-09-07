import datetime
import json
import os
import uuid
from functools import wraps
import time
import base64
import hmac
from flask import request, jsonify
from sqlalchemy import text
from sqlalchemy.orm import session
from werkzeug.security import generate_password_hash

from app import db, app
from app.model.models import T_students, T_innovation, T_classes, T_teachers, T_scientific, T_teachingr, T_coursetype, \
    T_cmodules, T_competition, T_prize, T_thesis, T_patent, T_research, T_courses, Admin
from app.utils.code_enum import Code
from . import home
from app.utils.common import login_required, SUCCESS


# def admin_login_req(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if "home" not in session:
#             return jsonify(
#                 {"code": 44,
#                  "msg": '请登录'
#                  }
#
#             )
#         return f(*args, **kwargs)
#
#     return decorated_function
#
#
# # 生成token 入参：用户id
# def generate_token(key, expire=3600):
#     ts_str = str(time.time() + expire)
#     ts_byte = ts_str.encode("utf-8")
#     sha1_tshexstr = hmac.new(key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
#     token = ts_str + ':' + sha1_tshexstr
#     b64_token = base64.urlsafe_b64encode(token.encode("utf-8"))
#     return b64_token.decode("utf-8")
#
#
# # 验证token 入参：用户id 和 token
# def certify_token(key, token):
#     if key is None or token is None:
#         return False
#     token_str = base64.urlsafe_b64decode(token).decode('utf-8')
#     token_list = token_str.split(':')
#     if len(token_list) != 2:
#         return False
#     ts_str = token_list[0]
#     if float(ts_str) < time.time():
#         # token expired
#         return False
#     known_sha1_tsstr = token_list[1]
#     sha1 = hmac.new(key.encode("utf-8"), ts_str.encode('utf-8'), 'sha1')
#     calc_sha1_tsstr = sha1.hexdigest()
#     if calc_sha1_tsstr != known_sha1_tsstr:
#         # token certification failed
#         return False
#     # token certification success
#     return True


@home.route('/test/')
@login_required()
def test():
    return jsonify({
        'code': -1,
        'msg': 'content',
    })


#@home.route('/login/', methods=['POST'])
# def login():
#     data = request.get_data()
#     data = str(data, 'utf-8')
#     data = json.loads(data)
#     admin = Admin.query.filter_by(name=data['username']).first()
#     if not admin:
#         return jsonify({
#             'code': -1,
#             'msg': '账号或密码错误',
#         })
#     if not admin.check_pwd(data['password']):
#         content = "账号或密码错误"
#         return jsonify({
#             'code': -1,
#             'msg': content,
#         })
#     else:
#         token = generate_token(data['username'])
#         return jsonify({
#             'code': 0,
#             'token': token,
#             'user': data['username'],
#             'msg': '登录成功'
#         })


# @home.route('/check_login/', methods=['POST'])
# def check_login():
#     data = request.get_data()
#     data = str(data, 'utf-8')
#     data = json.loads(data)
#     print(data)
#     if certify_token(data['user'], data['token']):
#         return jsonify(
#             {"code": 0,
#              "msg": '已登录'
#              }
#
#         )
#     else:
#         return jsonify(
#             {"code": -1,
#              "msg": '请登录'
#              }
#
#         )


# 学生列表
@home.route('/student/')
@login_required()
def student():
    student_count = T_students.query.count()
    data = request.args.to_dict()
    if data is not None:
        student_list = T_students.query.order_by(
            T_students.sno.asc()
        ).paginate(page=int(data.get('page')), per_page=int(data.get('limit')))
        return jsonify(
            {"code": 0,
             "msg": '',
             "count": student_count,
             "data": [
                 {"sno": user.sno, "sname": user.sname, "ssex": user.ssex, "sclass": user.sclass,
                  "scollege": user.scollege,
                  "smajor": user.smajor}
                 for user in student_list.items]
             }
        )
    else:
        return jsonify(
            {"code": -1,
             "msg": '错误',
             "data": []
             }
        )


# 大学生创新创业
@home.route('/innovation/')
@login_required()
def innovation():
    innovation_count = T_innovation.query.count()
    data = request.args.to_dict()
    innovation_list = T_innovation.query.order_by(
        T_innovation.id.asc()
    ).paginate(page=int(data.get('page')), per_page=int(data.get('limit')))
    return jsonify(
        {"code": 0,
         "msg": '',
         "count": innovation_count,
         "data": [
             {"sno": user.sno, "sname": user.sname, "grade": user.grade, "name": user.name, "level": user.level,
              "category": user.category}
             for user in innovation_list.items]
         }
    )


@home.route('/classes/')
@login_required()
def classes():
    classes_count = T_classes.query.count()
    data = request.args.to_dict()
    classes_list = T_classes.query.order_by(
        T_classes.id.asc()
    ).paginate(page=int(data.get('page')), per_page=int(data.get('limit')))
    return jsonify(
        {"code": 0,
         "msg": '',
         "count": classes_count,
         "data": [
             {"id": user.id, "name": user.name, "num": user.num}
             for user in classes_list.items]
         }
    )


#  增加班级
@home.route("/classes/add/", methods=["POST"])
@login_required()
def classes_add():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    t_classes = T_classes(
        name=data['name'],
        num=data['num'],
    )
    db.session.add(t_classes)
    db.session.commit()
    return jsonify({"code": 0, "info": "添加成功"})


@home.route("/classes/del/", methods=["POST"])
@login_required()
def classes_del():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    for i in data:
        t_classes = T_classes.query.filter_by(id=i['id']).first()
        db.session.delete(t_classes)
        db.session.commit()
    return jsonify({"code": 0, "info": "删除成功"})


#  增加学生
@home.route("/student/add/", methods=["POST"])
@login_required()
def student_add():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    t_students = T_students(
        sno=data['sno'],
        sname=data['sname'],
        ssex=data['sex'],
        sclass=data['sclass'],
        scollege=data['scollege'],
        smajor=data['smajor']
    )
    db.session.add(t_students)
    db.session.commit()
    return jsonify({"code": 0, "info": "添加成功"})


@home.route("/student/del/", methods=["POST"])
@login_required()
def student_del():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    for i in data:
        t_students = T_students.query.filter_by(sno=i['sno']).first()
        db.session.delete(t_students)
        db.session.commit()
    return jsonify({"code": 0, "info": "删除成功"})


#  增加大学生创新创业
@home.route("/innovation/add/", methods=["POST"])
@login_required()
def innovation_add():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    t_innovation = T_innovation(
        sno=data['sno'],
        sname=data['sname'],
        grade=data['grade'],
        name=data['name'],
        category=data['category'],
        level=data['level']
    )
    db.session.add(t_innovation)
    db.session.commit()
    return jsonify({"code": 0, "info": "添加成功"})


@home.route("/innovation/del/", methods=["POST"])
@login_required()
def innovation_del():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    for i in data:
        t_innovation = T_innovation.query.filter_by(sno=i['sno']).first()
        db.session.delete(t_innovation)
        db.session.commit()
    return jsonify({"code": 0, "info": "删除成功"})


#  教师信息管理
@home.route("/teachers/")
@login_required()
def teachers_list():
    data = request.args.to_dict()
    innovation_count = T_teachers.query.count()
    innovation_list = T_teachers.query.order_by(
        T_teachers.id.asc()
    ).paginate(page=int(data.get('page')), per_page=10)
    return jsonify(
        {"code": 0,
         "msg": '',
         "count": innovation_count,
         "data": [
             {"id": user.id, "name": user.name, "age": user.age, "title": user.title, "education": user.education,
              "degree": user.degree, "year": user.year}
             for user in innovation_list.items]
         }
    )


#  增加老师
@home.route("/teachers/add/", methods=["POST"])
@login_required()
def teachers_add():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
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
    return jsonify({"code": 0, "info": "添加成功"})


@home.route("/teachers/del/", methods=["POST"])
@login_required()
def teachers_del():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    for i in data:
        t_teachers = T_teachers.query.filter_by(name=i['name']).first()
        db.session.delete(t_teachers)
        db.session.commit()
    return jsonify({"code": 0, "info": "删除成功"})


# 教师科研成果
@home.route('/scientific/')
@login_required()
def scientific():
    scientific_count = T_scientific.query.count()
    data = request.args.to_dict()
    scientific_list = T_scientific.query.order_by(
        T_scientific.id.asc()
    ).paginate(page=int(data.get('page')), per_page=int(data.get('limit')))
    return jsonify(
        {"code": 0,
         "msg": '',
         "count": scientific_count,
         "data": [
             {"id": user.id, "name": user.name, "t_name": user.t_name, "nature": user.nature, "category": user.category,
              "sort": user.sort, "funds": user.funds, "number": user.number}
             for user in scientific_list.items]
         }
    )


#  增加教师科研成果
@home.route("/scientific/add/", methods=["POST"])
@login_required()
def scientific_add():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    t_scientific = T_scientific(
        name=data['name'],
        t_name=data['t_name'],
        nature=data['nature'],
        category=data['category'],
        sort=data['sort'],
        funds=data['funds'],
        number=data['number']
    )
    db.session.add(t_scientific)
    db.session.commit()
    return jsonify({"code": 0, "info": "添加成功"})


@home.route("/scientific/del/", methods=["POST"])
@login_required()
def scientific_del():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    for i in data:
        t_scientific = T_scientific.query.filter_by(id=i['id']).first()
        db.session.delete(t_scientific)
        db.session.commit()
    return jsonify({"code": 0, "info": "删除成功"})


# 教师教研成果
@home.route('/teachingr/')
@login_required()
def teachingr():
    teachingr_count = T_teachingr.query.count()
    data = request.args.to_dict()
    teachingr_list = T_teachingr.query.order_by(
        T_teachingr.id.asc()
    ).paginate(page=int(data.get('page')), per_page=int(data.get('limit')))
    return jsonify(
        {"code": 0,
         "msg": '',
         "count": teachingr_count,
         "data": [
             {"id": user.id, "name": user.name, "t_name": user.t_name, "level": user.level, "t_num": user.t_num,
              "funds": user.funds, "number": user.number}
             for user in teachingr_list.items]
         }
    )


#  增加教师教研成果
@home.route("/teachingr/add/", methods=["POST"])
@login_required()
def teachingr_add():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
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
    return jsonify({"code": 0, "info": "添加成功"})


@home.route("/teachingr/del/", methods=["POST"])
@login_required()
def teachingr_del():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    for i in data:
        t_teachingr = T_teachingr.query.filter_by(id=i['id']).first()
        db.session.delete(t_teachingr)
        db.session.commit()
    return jsonify({"code": 0, "info": "删除成功"})


# 课程类型
@home.route('/coursetype/')
@login_required()
def coursetype():
    coursetype_count = T_coursetype.query.count()
    data = request.args.to_dict()
    coursetype_list = T_coursetype.query.order_by(
        T_coursetype.id.asc()
    ).paginate(page=int(data.get('page')), per_page=int(data.get('limit')))
    return jsonify(
        {"code": 0,
         "msg": '',
         "count": coursetype_count,
         "data": [
             {"id": user.id, "name": user.name}
             for user in coursetype_list.items]
         }
    )


#  增加课程类型
@home.route("/coursetype/add/", methods=["POST"])
@login_required()
def coursetype_add():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    t_coursetype = T_coursetype(
        name=data['name'],
    )
    db.session.add(t_coursetype)
    db.session.commit()
    return jsonify({"code": 0, "info": "添加成功"})


@home.route("/coursetype/del/", methods=["POST"])
@login_required()
def coursetype_del():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    for i in data:
        t_coursetype = T_coursetype.query.filter_by(id=i['id']).first()
        db.session.delete(t_coursetype)
        db.session.commit()
    return jsonify({"code": 0, "info": "删除成功"})


# 课程模块
@home.route('/cmodules/')
@login_required()
def cmodules():
    cmodules_count = T_cmodules.query.count()
    data = request.args.to_dict()
    cmodules_list = T_cmodules.query.order_by(
        T_cmodules.id.asc()
    ).paginate(page=int(data.get('page')), per_page=int(data.get('limit')))
    return jsonify(
        {"code": 0,
         "msg": '',
         "count": cmodules_count,
         "data": [
             {"id": user.id, "name": user.name, "cno": user.cno, "cname": user.cname}
             for user in cmodules_list.items]
         }
    )


#  增加课程模块
@home.route("/cmodules/add/", methods=["POST"])
@login_required()
def cmodules_add():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    t_cmodules = T_cmodules(
        name=data['name'],
        cno=data['cno'],
        cname=data['cname'],
    )
    db.session.add(t_cmodules)
    db.session.commit()
    return jsonify({"code": 0, "info": "添加成功"})


@home.route("/cmodules/del/", methods=["POST"])
@login_required()
def cmodules_del():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    for i in data:
        t_cmodules = T_cmodules.query.filter_by(id=i['id']).first()
        db.session.delete(t_cmodules)
        db.session.commit()
    return jsonify({"code": 0, "info": "删除成功"})


# 竞赛管理
@home.route('/competition/')
@login_required()
def competition():
    competition_count = T_competition.query.count()
    data = request.args.to_dict()
    competition_list = T_competition.query.order_by(
        T_competition.id.asc()
    ).paginate(page=int(data.get('page')), per_page=int(data.get('limit')))
    return jsonify(
        {"code": 0,
         "msg": '',
         "count": competition_count,
         "data": [
             {"id": user.id, "name": user.name, "af_name": user.af_name, "organizer": user.organizer,
              "undertaker": user.undertaker
                 , "co_organizer": user.co_organizer, "url": user.url}
             for user in competition_list.items]
         }
    )


#  增加竞赛
@home.route("/competition/add/", methods=["POST"])
@login_required()
def competition_add():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    t_competition = T_competition(
        name=data['name'],
        af_name=data['af_name'],
        organizer=data['organizer'],
        undertaker=data['undertaker'],
        co_organizer=data['co_organizer'],
        url=data['url'],
    )
    db.session.add(t_competition)
    db.session.commit()
    return jsonify({"code": 0, "info": "添加成功"})


@home.route("/competition/del/", methods=["POST"])
@login_required()
def competition_del():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    for i in data:
        t_competition = T_competition.query.filter_by(id=i['id']).first()
        db.session.delete(t_competition)
        db.session.commit()
    return jsonify({"code": 0, "info": "删除成功"})


# 大学生获奖
@home.route('/prize/')
@login_required()
def prize():
    prize_count = T_prize.query.count()
    data = request.args.to_dict()
    if data is None:
        data = {"page": 1, "limit": 10}
    prize_list = T_prize.query.order_by(
        T_prize.id.asc()
    ).paginate(page=int(data.get('page')), per_page=int(data.get('limit')))
    return jsonify(
        {"code": Code.SUCCESS.value,
         "msg": '',
         "count": prize_count,
         "data": [
             {"sno": user.sno, "sname": user.sname, "grade": user.grade, "name": user.name, "level": user.level,
              "p_time": user.p_time, "award": user.award, "img": user.img, "id": user.id}
             for user in prize_list.items]
         }
    )


#  增加获奖
@home.route("/prize/add/", methods=["POST"])
@login_required()
def prize_add():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    t_prize = T_prize(
        sno=data['sno'],
        sname=data['sname'],
        grade=data['grade'],
        name=data['name'],
        p_time=data['p_time'],
        level=data['level'],
        award=data['award'],
    )
    db.session.add(t_prize)
    db.session.commit()
    return jsonify({"code": 0, "info": "添加成功"})


# 修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


@home.route('/prize/upload/', methods=["POST"])
@login_required()
def prize_upload():
    img = request.files.get("img")
    img_filename = change_filename(img.filename)
    img.save(app.config["UP_DIR"] + 'imgs/' + img_filename)
    data = request.form.to_dict()
    print(data)
    print(data['id'])
    print(type(data['id']))
    t_prize = T_prize.query.filter_by(id=int(data['id'])).first()
    t_prize.img = 'http://www.yujl.top:2020/' + img_filename
    db.session.add(t_prize)
    db.session.commit()
    return jsonify({"code": 0, "msg": "上传成功"})


@home.route("/prize/del/", methods=["POST"])
@login_required()
def prize_del():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    for i in data:
        t_prize = T_prize.query.filter_by(sno=i['sno']).first()
        db.session.delete(t_prize)
        db.session.commit()
    return jsonify({"code": 0, "info": "删除成功"})


# 大学生发表论文情况
@home.route('/thesis/')
@login_required()
def thesis():
    thesis_count = T_thesis.query.count()
    data = request.args.to_dict()
    thesis_list = T_thesis.query.order_by(
        T_thesis.id.asc()
    ).paginate(page=int(data.get('page')), per_page=int(data.get('limit')))
    return jsonify(
        {"code": 0,
         "msg": '',
         "count": thesis_count,
         "data": [
             {"id": user.id, "sno": user.sno, "sname": user.sname, "grade": user.grade, "name": user.name,
              "periodical": user.periodical,
              "time": user.time, "inclusion": user.inclusion}
             for user in thesis_list.items]
         }
    )


#  增加论文
@home.route("/thesis/add/", methods=["POST"])
@login_required()
def thesis_add():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    t_thesis = T_thesis(
        sno=data['sno'],
        sname=data['sname'],
        grade=data['grade'],
        name=data['name'],
        time=data['time'],
        periodical=data['periodical'],
        inclusion=data['inclusion'],
    )
    db.session.add(t_thesis)
    db.session.commit()
    return jsonify({"code": 0, "info": "添加成功"})


@home.route("/thesis/del/", methods=["POST"])
@login_required()
def thesis_del():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    for i in data:
        t_thesis = T_thesis.query.filter_by(id=i['id']).first()
        db.session.delete(t_thesis)
        db.session.commit()
    return jsonify({"code": 0, "info": "删除成功"})


# 大学生专利情况
@home.route('/patent/')
@login_required()
def patent():
    patent_count = T_patent.query.count()
    data = request.args.to_dict()
    patent_list = T_patent.query.order_by(
        T_patent.id.asc()
    ).paginate(page=int(data.get('page')), per_page=int(data.get('limit')))
    return jsonify(
        {"code": 0,
         "msg": '',
         "count": patent_count,
         "data": [
             {"id": user.id, "sno": user.sno, "sname": user.sname, "grade": user.grade, "name": user.name,
              "category": user.category, "time": user.time, "f_inventor": user.f_inventor, "num": user.num}
             for user in patent_list.items]
         }
    )


#  增加论文
@home.route("/patent/add/", methods=["POST"])
@login_required()
def patent_add():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    t_patent = T_patent(
        sno=data['sno'],
        sname=data['sname'],
        grade=data['grade'],
        name=data['name'],
        time=data['time'],
        f_inventor=data['f_inventor'],
        num=data['num'],
        category=data['category'],
    )
    db.session.add(t_patent)
    db.session.commit()
    return jsonify({"code": 0, "info": "添加成功"})


@home.route("/patent/del/", methods=["POST"])
@login_required()
def patent_del():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    for i in data:
        t_patent = T_patent.query.filter_by(id=i['id']).first()
        db.session.delete(t_patent)
        db.session.commit()
    return jsonify({"code": 0, "info": "删除成功"})


# 大学生科研项目
@home.route('/research/')
@login_required()
def research():
    research_count = T_research.query.count()
    data = request.args.to_dict()
    research_list = T_research.query.order_by(
        T_research.id.asc()
    ).paginate(page=int(data.get('page')), per_page=int(data.get('limit')))
    return jsonify(
        {"code": 0,
         "msg": '',
         "count": research_count,
         "data": [
             {"id": user.id, "sno": user.sno, "sname": user.sname, "grade": user.grade, "name": user.name,
              "head": user.head,
              "company": user.company}
             for user in research_list.items]
         }
    )


#  增加大学生创新创业
@home.route("/research/add/", methods=["POST"])
@login_required()
def research_add():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    t_research = T_research(
        sno=data['sno'],
        sname=data['sname'],
        grade=data['grade'],
        name=data['name'],
        head=data['head'],
        company=data['company']
    )
    db.session.add(t_research)
    db.session.commit()
    return jsonify({"code": 0, "info": "添加成功"})


@home.route("/research/del/", methods=["POST"])
@login_required()
def research_del():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    for i in data:
        t_research = T_research.query.filter_by(id=i['id']).first()
        db.session.delete(t_research)
        db.session.commit()
    return jsonify({"code": 0, "info": "删除成功"})


# 课程
@home.route('/courses/')
@login_required()
def courses():
    courses_count = T_courses.query.count()
    data = request.args.to_dict()
    courses_list = T_courses.query.order_by(
        T_courses.cno.asc()
    ).paginate(page=int(data.get('page')), per_page=int(data.get('limit')))
    return jsonify(
        {"code": 0,
         "msg": '',
         "count": courses_count,
         "data": [
             {"cno": user.cno, "cname": user.cname, "credit": user.credit, "theory_hour": user.theory_hour,
              "practice_hour": user.practice_hour, "hour": user.hour, "term": user.term, "methods": user.methods,
              "year": user.year}
             for user in courses_list.items]
         }
    )


#  增加课程
@home.route("/courses/add/", methods=["POST"])
@login_required()
def courses_add():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    t_courses = T_courses(
        cno=data['cno'],
        cname=data['cname'],
        credit=data['credit'],
        theory_hour=data['theory_hour'],
        practice_hour=data['practice_hour'],
        hour=data['hour'],
        term=data['term'],
        methods=data['methods'],
        year=data['year'],
    )
    db.session.add(t_courses)
    db.session.commit()
    return jsonify({"code": 0, "info": "添加成功"})


@home.route("/courses/del/", methods=["POST"])
@login_required()
def courses_del():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    for i in data:
        t_courses = T_courses.query.filter_by(cno=i['cno']).first()
        db.session.delete(t_courses)
        db.session.commit()
    return jsonify({"code": 0, "info": "删除成功"})


@home.route('/data/')
def data():
    school_student_count = T_students.query.filter(text("SUBSTR(sno,1,2) != 14 and SUBSTR(sno,1,2) != 15")).count()
    graduate_count = T_students.query.filter(text("SUBSTR(sno,1,2) = 14 or SUBSTR(sno,1,2) = 15")).count()
    teaching_count = T_teachers.query.count()
    teachingr_count = T_teachingr.query.count()
    scientific_count = T_scientific.query.count()
    courses_count = T_courses.query.count()
    innovation_count = T_innovation.query.count()
    research_count = T_research.query.count()
    prize_count = T_prize.query.count()
    thesis_count = T_thesis.query.count()
    patent_count = T_patent.query.count()
    Student_outcomes = innovation_count + research_count + prize_count + thesis_count + patent_count
    return jsonify({"code": 0,
                    "data": [{
                        "school_student_count": school_student_count,
                        "graduate_count": graduate_count,
                        "teaching_count": teaching_count,
                        "teachingr_count": teachingr_count,
                        "scientific_count": scientific_count,
                        "courses_count": courses_count,
                        "Student_outcomes": Student_outcomes

                    }
                    ]
                    })


# 管理员管理
@home.route('/admin/')
@login_required()
def admin():
    admin_count = Admin.query.count()
    data = request.args.to_dict()
    admin_list = Admin.query.order_by(
        Admin.id.asc()
    ).paginate(page=int(data.get('page')), per_page=int(data.get('limit')))
    return jsonify(
        {"code": 0,
         "msg": '',
         "count": admin_count,
         "data": [
             {"id": user.id, "name": user.name, "is_super": user.is_super, "add_time": user.addtime}
             for user in admin_list.items]
         }
    )


#  增加管理员
@home.route("/admin/add/", methods=["POST"])
@login_required()
def admin_add():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    check_admin = Admin.query.filter_by(name=data['name']).count()
    if check_admin == 1:
        return jsonify({"code": -1, "info": "已存在此管理员"})
    pwd = generate_password_hash(data['pwd'])
    admin = Admin(
        name=data['name'],
        pwd=pwd,
        is_super=data['is_super'],

    )
    db.session.add(admin)
    db.session.commit()
    return jsonify({"code": 0, "info": "添加成功"})


@home.route("/admin/del/", methods=["POST"])
@login_required()
def admin_del():
    data = request.get_data()
    data = str(data, 'utf-8')
    data = json.loads(data)
    for i in data:
        admin = Admin.query.filter_by(id=i['id']).first()
        db.session.delete(admin)
        db.session.commit()
    return jsonify({"code": 0, "info": "删除成功"})


@home.route('/search/',methods=['POST'])
def search():
    data = request.get_data()
    data = str(data,'utf-8')
    data = json.loads(data)
    data1 = {
        '姓名':'刘玉江',
        '学号':'14',
        '性别':'男',
        '班级':'18信管03',
        '竞赛获奖':{
            '竞赛名称':'xxx',
            '获奖时间':'xxx',
            '获奖级别':'xxx',
            '获奖等级':'xxx',
            '证书':'xxx'
        },
        '大学生创新创业':{
            '项目名称':'xxx',
            '项目级别':'xxx',
            '项目类别':'xxx'
        },
        '大学生科研项目':{
            '项目名称':'xxx',
            '项目级别':'xxx',
            '项目类别':'xxx'
        },
        '学术论文':{
            '项目名称':'xxx',
            '项目级别':'xxx',
            '项目类别':'xxx'
        },
        '专利':{
            '项目名称':'xxx',
            '项目级别':'xxx',
            '项目类别':'xxx'
        },
        '职业证书':{
            '项目名称':'xxx',
            '项目级别':'xxx',
            '项目类别':'xxx'
        }

    }
    res=[]
    stus = T_students.query.filter_by(sname=data['content']).all()
    for stu in stus:
        dic={}
        dic['姓名'] = stu.sname
        dic['学号'] = stu.sno
        dic['性别'] = stu.ssex
        dic['班级'] = stu.sclass

        prize_dics=[]
        prize_list = T_prize.query.filter_by(sname=stu.sname).all()
        for prize in prize_list:
            prize_dic = {}
            prize_dic['竞赛名称']=prize.name
            prize_dic['获奖时间']=prize.p_time
            prize_dic['获奖级别']=prize.level
            prize_dic['获奖等级']=prize.award
            prize_dic['证书']=prize.img
            prize_dics.append(prize_dic)
        dic['竞赛获奖'] = prize_dics

        innovation_dics=[]
        innovation_list = T_innovation.query.filter_by(sname=stu.sname).all()
        for nnovation in innovation_list:
            nnovation_dic = {}
            nnovation_dic['项目名称']=nnovation.name
            nnovation_dic['项目级别']=nnovation.level
            nnovation_dic['项目类别']=nnovation.category
            innovation_dics.append(nnovation_dic)
        dic['大学生创新创业'] = innovation_dics

        research_dics = []
        research_list = T_research.query.filter_by(sname=stu.sname).all()
        for research in research_list:
            research_dic = {}
            research_dic['项目名称']=research.name
            research_dic['负责人']=research.head
            research_dic['负责人单位']=research.company
            research_dics.append(research_dic)
        dic['大学生科研项目'] = research_dics

        thesis_dics = []
        thesis_list = T_thesis.query.filter_by(sname=stu.sname).all()
        for thesis in thesis_list:
            thesis_dic = {}
            thesis_dic['名称'] = thesis.name
            thesis_dic['发表期刊'] = thesis.periodical
            thesis_dic['发表时间'] = thesis.time
            thesis_dic['收录情况'] = thesis.inclusion
            thesis_dics.append(thesis_dic)
        dic['学术论文'] = thesis_dics

        patent_dics = []
        patent_list = T_patent.query.filter_by(sname=stu.sname).all()
        for thesis in patent_list:
            patent_dic = {}
            patent_dic['名称'] = patent.name
            patent_dic['类别'] = patent.category
            patent_dic['授权号'] = patent.num
            patent_dic['发表时间'] = patent.time
            patent_dic['是否第一发明人'] = patent.f_inventor
            patent_dics.append(patent_dic)
        dic['专利'] = patent_dics

        res.append(dic)
    return SUCCESS(data=res)



