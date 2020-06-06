import json
import requests
from functools import wraps
from flask import Blueprint, jsonify, request

from ido.application import UserApplication
from ido.config import WX_APPID, WX_SECRET

api = Blueprint('api', __name__, url_prefix='/api/v1')


def auth_sign(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # 校验签名，记得封装成装饰器
        sign = request.values.get('sign')
        if not UserApplication.check_sign(sign):
            return {}, 401
        return f(*args, **kwargs)

    return wrapper


@api.route('/login', methods=['POST'])
@auth_sign
def login():
    params = {
        'openid': request.form.get('openid'),
        'name': request.form.get('name'),
        'face': request.form.get('face'),
    }

    user_app = UserApplication()
    user = user_app.login(**params)
    data = {
        'openid': user.openid,
        'name': user.name,
        'face': user.face,
        'random': user.random,
        'remainder': user.remainder,
        'regtime': user.regtime,

    }
    return jsonify(data)


@api.route('/wxsession')
def get_wx_session():
    # https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code
    jscode = request.args.get('jscode')
    url = ' https://api.weixin.qq.com/sns/jscode2session?' \
          'appid={APPID}&secret={SECRET}&js_code={JSCODE}' \
          '&grant_type=authorization_code'.format(
        APPID=WX_APPID, SECRET=WX_SECRET, JSCODE=jscode)

    res = requests.get(url).json()
    data = {
        'session_key': res.get('session_key'),
        'expires_in': res.get('expires_in'),
        'openid': res.get('openid')
    }
    return jsonify(data)


@api.route('/token')
def get_access_token():
    user_app = UserApplication()
    token = user_app.gen_access_token()
    data = {
        'token': token.token,
        'time': token.time
    }
    return jsonify(data)


@api.route('/categories')
def get_categories():
    pid = request.args.get('pid', 0)

    user_app = UserApplication()
    categories = user_app.get_categories(pid)

    if not categories:
        return []

    return jsonify([category.name for category in categories])


@api.route('/article', methods=['POST'])
@auth_sign
def add_article():
    params = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'uid': request.form.get('uid'),
        'random': request.form.get('random'),
        'cate': request.form.get('cate')  # 这个是分类id
    }
    user_app = UserApplication()
    article = user_app.add_article(**params)
    data = {
        'title': article.title,
        'content': article.content,
        'cate': article.cate
    }
    return jsonify(data)


@api.route('/article', methods=['DELETE'])
def delete_article():
    params = {
        'uid': request.form.get('uid'),
        'random': request.form.get('random'),
        'aid': request.form.get('aid'),
    }

    app = UserApplication()
    app.delete_article(**params)

    data = {
        'deleted': True
    }
    return jsonify(data)

@api.route('/article', methods=['PUT'])
@auth_sign
def update_article():
    params = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        'uid': request.form.get('uid'),
        'random': request.form.get('random'),
        'cate': request.form.get('cate'),
        'aid': request.form.get('aid')
    }
    user_app = UserApplication()
    article = user_app.update_article(**params)
    data = {
        'title': article.title,
        'content': article.content,
        'cate': article.cate
    }
    return jsonify(data)

@api.route('/article', methods=['GET'])
def get_article_info():
    from ido import utils

    params = {
        'aid': request.args.get('aid'),
    }

    app = UserApplication()
    article = app.get_article(**params)

    user = app.get_user_by_id(article.uid)

    data = {
        'title': article.title,
        'content': article.content,
        'cate': article.cate,
        'aid': article.id,
        'create_time': utils.strftime(article.create_time),
        'u_face': user.face,
        'u_name': user.name
    }
    return jsonify(data)


@api.route('/articles', methods=['GET'])
def get_article_list():
    params = {
        'uid': request.args.get('uid'),
        'random': request.args.get('random'),
        'page': int(request.args.get('page', 1)),
        'cate': request.args.get('cate')
    }

    app = UserApplication()
    articles = app.get_articles(**params)

    data_list = []
    for article in articles:
        data = {
            'aid': article.id,
            'cate': article.cate,
            'title': article.title,
            'content': article.content,
            'create_time': article.create_time
        }
        data_list.append(data)

    return jsonify(data_list)


@api.route('/img', methods=['POST'])
def upload_img():
    from ido import utils, BASE_DIR
    from werkzeug.utils import secure_filename

    img_file = request.files.get('file')
    ext_name = '.' + img_file.filename.rsplit('.', 1)[1]
    upload_path = '/static/imgs/' + secure_filename(utils.uniqid() + ext_name)
    img_file.save(BASE_DIR + upload_path)
    return {'path': upload_path}


@api.route('/info')
def get_user_info():
    params = {
        'uid': request.args.get('uid'),
        'random': request.args.get('random')
    }

    user_app = UserApplication()
    user = user_app.get_user(**params)
    art_count = user_app.get_articles_count()

    data = {
        'art_count': art_count,
        'name': user.name,
        'face': user.face,
        'openid': user.openid,
        'random': user.random,
        'integral': user.integral,
        'remainder': user.remainder
    }

    return jsonify(data)
