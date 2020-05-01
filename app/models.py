from datetime import datetime

from app import db


class T_students(db.Model):
    __tablename__ = 't_students'
    sno = db.Column(db.String(10), primary_key=True)  # 学号
    sname = db.Column(db.String(10))  # 名字
    ssex = db.Column(db.String(4))  # 性别
    sclass = db.Column(db.String(100))  # 班级
    scollege = db.Column(db.String(100))  # 学院
    smajor = db.Column(db.String(100))  # 专业

    def __repr__(self):
        return "<T_students %r>" % self.sname


class T_classes(db.Model):
    __tablename__ = 't_classes'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),unique=True)  # 班级
    num = db.Column(db.Integer)  # 学生人数

    def __repr__(self):
        return "<T_classes %r>" % self.name


class T_cmodules(db.Model):
    __tablename__ = 't_cmodules'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))  # 模块名称
    cno = db.Column(db.String(100))  # 课程代码
    cname = db.Column(db.String(100))  # 课程名称

    def __repr__(self):
        return "<T_cmodules %r>" % self.name


class T_cshedules(db.Model):
    __tablename__ = 't_cshedules'
    id = db.Column(db.Integer, primary_key=True)
    no = db.Column(db.String(100))  # 课程代码
    name = db.Column(db.String(100))  # 课程名称
    time = db.Column(db.DateTime, index=True)  # 上课时间
    place = db.Column(db.String(100))  # 上课地点
    number = db.Column(db.Integer)  # 上课人数
    cclass = db.Column(db.String(100))  # 上课班级

    def __repr__(self):
        return "<T_cshedules %r>" % self.name


class T_courses(db.Model):
    __tablename__ = 't_courses'
    cno = db.Column(db.String(100), primary_key=True)  # 课程代码
    cname = db.Column(db.String(100),unique = True)  # 课程名
    credit = db.Column(db.Float)  # 总学分
    theory_hour = db.Column(db.Integer)  # 理论学时
    practice_hour = db.Column(db.Integer)  # 实践学时
    hour = db.Column(db.Integer)  # 学时
    year = db.Column(db.String(2))  # 学年
    term = db.Column(db.String(2))  # 学期
    methods = db.Column(db.String(10))  # 考核方式


    def __repr__(self):
        return "<T_courses %r>" % self.cname



class T_competition(db.Model):
    __tablename__ = 't_competition'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))  # 竞赛全称
    af_name = db.Column(db.String(100))  # 简称
    organizer = db.Column(db.String(100), index=True)  # 主办单位
    undertaker = db.Column(db.String(100))  # 承办单位
    co_organizer = db.Column(db.String(100))  # 协办单位
    url = db.Column(db.String(100))  # 主页链接

    def __repr__(self):
        return "<T_competition %r>" % self.name

class T_teachers(db.Model):
    __tablename__ = 't_teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))  # 教师名字
    age = db.Column(db.Integer)  # 年龄
    title = db.Column(db.String(100))  # 专业技术职称
    education = db.Column(db.String(100))  # 学历
    degree = db.Column(db.String(100))  # 最高学位
    year = db.Column(db.String(100))  # 从事专业教学时间

    def __repr__(self):
        return "<T_teachers %r>" % self.name



class T_scientific(db.Model):
    __tablename__ = 't_scientific'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))  # 项目名称
    t_name = db.Column(db.String(100))  # 主持人姓名
    nature = db.Column(db.String(100))  # 项目性质
    category = db.Column(db.String(100))  # 纵向项目类别
    sort = db.Column(db.String(100))  # 立项单位排序
    funds = db.Column(db.Float)  # 项目经费（万元）
    number = db.Column(db.String(100))  # 立项编号

    def __repr__(self):
        return "<T_teachers %r>" % self.name




class T_teachingr(db.Model):
    __tablename__ = 't_teachingr'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))  # 项目名称
    t_name = db.Column(db.String(100))  # 主持人姓名
    level = db.Column(db.String(100))  # 级别
    t_num = db.Column(db.Integer)  # 参与教师数
    funds = db.Column(db.Float)  # 项目经费（万元）
    number = db.Column(db.String(100))  # 立项编号

    def __repr__(self):
        return "<T_teachers %r>" % self.name

# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    pwd = db.Column(db.String(100))  # 管理员密码
    is_super = db.Column(db.SmallInteger)  # 是否是超级管理员 0为超级管理员
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# if __name__ == "__main__":
#      db.create_all()
