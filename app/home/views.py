from . import home
@home.route('/')
def index():
    return 'hello home'