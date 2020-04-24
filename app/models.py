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
    name = db.Column(db.String(100),primary_key=True,unique=True)  # 班级
    num = db.Column(db.Integer)  # 学生人数

    def __repr__(self):
        return "<T_classes %r>" % self.cname


class T_cmodules(db.Model):
    __tablename__ = 't_cmodules'
    name = db.Column(db.String(100), primary_key=True)  # 模块名称
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
        return "<T_cshedules %r>" % self.cname


class T_courses(db.Model):
    __tablename__ = 't_courses'
    cno = db.Column(db.String(100), primary_key=True)  # 课程代码
    cname = db.Column(db.String(100),unique = True)  # 课程名
    credit = db.Column(db.Integer)  # 总学分
    theory_credit = db.Column(db.Integer)  # 理论学分
    practice_credit = db.Column(db.Integer)  # 实践学分
    hour = db.Column(db.Integer)  # 学时
    year = db.Column(db.String(2))  # 学年
    term = db.Column(db.String(2))  # 学期
    methods = db.Column(db.String(10))  # 学期


    def __repr__(self):
        return "<T_courses %r>" % self.cname


# if __name__ == "__main__":
#     db.create_all()
