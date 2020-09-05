import hashlib
from datetime import datetime

from sqlalchemy import func

from app import db
from app.model.BaseModel import BaseModel


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



#  课程类型
class T_coursetype(db.Model):
    __tablename__ = 't_coursetype'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))  # 课程类型


class T_innovation(db.Model):
    __tablename__ = 't_innovation'
    id = db.Column(db.Integer, primary_key=True)
    sno = db.Column(db.String(100))  # 学号
    sname = db.Column(db.String(100))  # 学生姓名
    grade = db.Column(db.String(100))  # 年级
    name = db.Column(db.String(100))  # 项目名称
    level = db.Column(db.String(100))  # 项目级别
    category = db.Column(db.String(100))  # 项目类别

    def __repr__(self):
        return "<T_innovation %r>" % self.name

class T_prize(db.Model):
    __tablename__ = 't_prize'
    id = db.Column(db.Integer, primary_key=True)
    sno = db.Column(db.String(100))  # 学号
    sname = db.Column(db.String(100))  # 学生姓名
    grade = db.Column(db.String(100))  # 年级
    name = db.Column(db.String(100))  # 竞赛名称
    level = db.Column(db.String(100))  # 获奖级别
    award = db.Column(db.String(100))  # 获奖等级
    p_time = db.Column(db.String(100))  # 获奖时间
    img = db.Column(db.String()) #获奖证书图片

    def __repr__(self):
        return "<T_prize %r>" % self.name



class T_thesis(db.Model):
    __tablename__ = 't_thesis'
    id = db.Column(db.Integer, primary_key=True)
    sno = db.Column(db.String(100))  # 学号
    sname = db.Column(db.String(100))  # 学生姓名
    grade = db.Column(db.String(100))  # 年级
    name = db.Column(db.String(100))  # 竞赛名称
    periodical = db.Column(db.String(100))  # 发表期刊
    time = db.Column(db.String(100))  # 发表时间
    inclusion = db.Column(db.String(100))  # 收录情况

    def __repr__(self):
        return "<T_thesis %r>" % self.name


class T_patent(db.Model):
    __tablename__ = 't_patent'
    id = db.Column(db.Integer, primary_key=True)
    sno = db.Column(db.String(100))  # 学号
    sname = db.Column(db.String(100))  # 学生姓名
    grade = db.Column(db.String(100))  # 年级
    name = db.Column(db.String(100))  # 竞赛名称
    category = db.Column(db.String(100))  # 类别
    num = db.Column(db.String(100))  # 授权号
    time = db.Column(db.String(100))  # 发表时间
    f_inventor = db.Column(db.String(100))  # 是否第一发明人

    def __repr__(self):
        return "<T_patent %r>" % self.name


class T_research(db.Model):
    __tablename__ = 't_research'
    id = db.Column(db.Integer, primary_key=True)
    sno = db.Column(db.String(100))  # 学号
    sname = db.Column(db.String(100))  # 学生姓名
    grade = db.Column(db.String(100))  # 年级
    name = db.Column(db.String(100))  # 项目名称
    head = db.Column(db.String(100))  # 项目负责人
    company = db.Column(db.String(100))  # 项目负责人单位

    def __repr__(self):
        return "<T_research %r>" % self.name





class User(BaseModel):
    """
    用户表
    """
    __tablename__ = "t_user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="用户ID")
    nickname = db.Column(db.String(30), comment="用户昵称")
    user_name = db.Column(db.String(30), comment="登录账号")
    user_type = db.Column(db.Boolean, default=1, comment="用户类型（1系统用户")
    email = db.Column(db.String(50), comment="用户邮箱")
    phone = db.Column(db.String(20), comment="手机号")
    phonenumber = db.Column(db.String(11), comment="手机号码")
    sex = db.Column(db.INTEGER, default=1, comment="用户性别（1男 2女 3未知）")
    avatar = db.Column(db.String(100), comment="头像路径")
    password = db.Column(db.String(50), comment="密码")
    salt = db.Column(db.String(20), comment="盐加密")
    status = db.Column(db.INTEGER, default=1, comment="帐号状态（1正常 2禁用")
    dept_id = db.Column(db.INTEGER, comment="部门id")
    del_flag = db.Column(db.INTEGER, default=1, comment="删除标志（1代表存在 2代表删除）")
    login_ip = db.Column(db.String(50), comment="最后登陆IP")
    login_date = db.Column(db.TIMESTAMP, comment="最后登陆时间", nullable=False,
                           onupdate=func.now())
    role_user = db.relationship("User_Role",backref="t_user")


    def check_password(self, passwd):
        '''
        检查密码
        :param passwd:
        :return: 0/1
        '''
        # 创建md5对象
        m = hashlib.md5()
        b = passwd.encode(encoding='utf-8')
        m.update(b)
        str_md5 = m.hexdigest()
        if self.password == str_md5:
            return 1
        else:
            return 0
    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, pwd)

class Role(BaseModel):
    __tablename__ = "t_role"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="角色ID")
    role_name = db.Column(db.String(30),comment="角色名称")
    role_key = db.Column(db.String(100),comment="角色权限字符串")
    role_sort = db.Column(db.Integer(),comment="显示顺序")
    data_scope = db.Column(db.Integer(),comment="数据范围（1：全部数据权限 2：自定数据权限）")
    status = db.Column(db.Integer(),comment="角色状态（1正常 2停用）")
    create_by = db.Column(db.String(64),comment="创建者")
    created_at = db.Column(db.DateTime,comment="创建时间")
    updated_at = db.Column(db.DateTime,comment="更新时间")
    update_by = db.Column(db.String(64),comment="更新者")
    remark = db.Column(db.DateTime(500),comment="备注")
    role_user = db.relationship("User_Role",backref="t_role")


class User_Role(BaseModel):
    __tablename__ = "t_user_role"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,db.ForeignKey("t_user.id"))
    role_id = db.Column(db.Integer,db.ForeignKey("t_role.id"))
    create_by = None
    created_at = None
    update_by = None
    updated_at = None
    remark = None




class Menu(BaseModel):
    """
    菜单权限表
    """
    __tablename__ = "t_menu"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="菜单ID")
    menu_name = db.Column(db.String(50), comment="菜单名称")
    parent_id = db.Column(db.Integer, comment="父菜单ID")
    order_num = db.Column(db.Integer, comment="显示顺序")
    url = db.Column(db.String(200), comment="请求地址")
    menu_type = db.Column(db.Integer, default=1, comment="菜单类型（1,目录 2,菜单 3,按钮")
    visible = db.Column(db.Integer, default=1, comment="菜单状态（1显示 2隐藏）")
    perms = db.Column(db.String(100), comment="权限标识")
    icon = db.Column(db.String(100), comment="菜单图标")
    is_frame = db.Column(db.Integer, default=2, comment="是否外链")
    route_name = db.Column(db.String(100), default="", comment="路由名称")
    route_path = db.Column(db.String(100), default="", comment="路由地址")
    route_cache = db.Column(db.Integer, default=0, comment="路由缓存")
    route_component = db.Column(db.String(100), default="", comment="路由组件")





class Role_Menu(BaseModel):
    """
    角色菜单关联表
    """
    __tablename__ = "t_role_menu"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="ID")
    role_id = db.Column(db.Integer, comment="角色ID")
    menu_id = db.Column(db.Integer, comment="菜单ID")
    create_by = None
    created_at = None
    update_by = None
    updated_at = None
    remark = None
# if __name__ == "__main__":
#      db.create_all()
