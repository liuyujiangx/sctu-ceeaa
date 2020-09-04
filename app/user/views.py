from flask import request, jsonify

from app.model.models import User, Role, User_Role
from . import user
from app.utils.common import login_required, create_token, SUCCESS, verify_token, AUTH_ERR, REQUEST_ERROR, OTHER_LOGIN, \
    NO_PARAMETER
from app.utils.code_enum import Code
from app import app
from app.utils.redis_utils import Redis

@user.route('/test')
# @login_required('admin')
def test():
    return SUCCESS()


@user.route('/login', methods=["POST"])
def login():
    '''
    用户登录
    :return:token
    '''
    res_dir = request.get_json()
    if res_dir is None:
        return NO_PARAMETER()
    # 获取前端传过来的参数
    username = res_dir.get("username")
    password = res_dir.get("password")
    # 校验参数
    if not all([username, password]):
        return jsonify(code=Code.NOT_NULL.value, msg="用户名和密码不能为空")
    try:
        user = User.query.filter_by(user_name=username).first()
    except Exception as e:
        print("login error：{}".format(e))
        return jsonify(code=Code.REQUEST_ERROR.value, msg="获取信息失败")
    if user is None or not user.check_pwd(password) or user.del_flag == 2 or user.status == 2:
        return jsonify(code=Code.ERR_PWD.value, msg="用户名或密码错误")

    # 获取用户信息，传入生成token的方法，并接收返回的token
    # 获取用户角色
    user_role = Role.query.join(User_Role, Role.id == User_Role.role_id).join(User,
                                                                              User_Role.user_id == user.id).filter(
        User.id == user.id).all()
    role_list = [i.role_key for i in user_role]
    print(role_list)
    token = create_token(user.id, user.user_name, role_list)
    data = {'token': token, 'userId': user.id, 'userName': user.user_name, 'nickname': user.nickname}
    # 记录登录ip将token存入rerdis
    # try:
    #     user.login_ip = request.remote_addr
    #     print(user.login_ip)
    #     user.update()
    #     Redis.write(f"token_{user.user_name}", token)
    #     print(token)
    #
    # except Exception as e:
    #     print(e)
    #     return jsonify(code=Code.UPDATE_DB_ERROR.value, msg="登录失败")
    if token:
        # 把token返回给前端
        return jsonify(code=Code.SUCCESS.value, msg="登录成功", data=data)
    else:
        return jsonify(code=Code.REQUEST_ERROR.value, msg="请求失败", data=token)


@user.route('/logout', methods=["POST"])
@login_required()
def logout():
    '''
    注销方法：redis删除token
    :return:
    '''
    try:
        token = request.headers["Authorization"]
        user = verify_token(token)
        if user:
            key = f"token_{user.get('name')}"
            redis_token = Redis.read(key)
            if redis_token:
                Redis.delete(key)
            return SUCCESS()
        else:
            return AUTH_ERR()
    except Exception as e:
        app.logger.error(f"注销失败")
        return REQUEST_ERROR()


@user.route('/check_token', methods=["POST"])
def check_token():
    # 在请求头上拿到token
    token = request.headers["Authorization"]
    user = verify_token(token)
    if user:
        key = f"token_{user.get('name')}"
        redis_token = Redis.read(key)
        if redis_token == token:
            return SUCCESS(data=user.get('id'))
        else:
            return OTHER_LOGIN()
    else:
        return AUTH_ERR()
