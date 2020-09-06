from flask import jsonify

from app import app

from app.utils.code_enum import Code


#@app.errorhandler(Exception)
def handle_error(err):
    """自定义处理错误方法"""
    # 这个函数的返回值会是前端用户看到的最终结果
    try:
        if err.code == 404:
            app.logger.error(err)
            return jsonify(code=Code.NOT_FOUND.value, msg="服务器异常,404")
        elif err.code == 400:
            app.logger.error(err)
            return jsonify(code=Code.REQUEST_ERROR.value, msg="服务器异常,400")
        elif err.code == 500:
            app.logger.error(err)
            return jsonify(code=Code.INTERNAL_ERROR.value, msg="服务器异常,500")
        else:
            return jsonify(code=err.code, msg=f"服务器异常,{err.code}")
    except:
        return jsonify(code=Code.INTERNAL_ERROR.value, msg=f"服务器异常,{err}")


if __name__ == "__main__":
    app.run(debug=True)
