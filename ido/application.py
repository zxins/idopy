import hashlib
from sqlalchemy import desc
from ido.models import Members, AccessTokens, Categories, Articles
from ido import utils


class UserApplication:

    def login(self, **kwargs):
        openid = kwargs.get('openid')
        name = kwargs.get('name')
        face = kwargs.get('face')
        random = kwargs.get('random') or utils.uniqid()

        model = Members.query.filter_by(openid=openid).first()
        if not model:
            member = Members(openid=openid, name=name, face=face, random=random)
            member.save()
            return member
        return model

    def gen_access_token(self):
        """ 生成一条access token """
        token = utils.uniqid()

        token = AccessTokens(token=token, time=utils.timestamp())
        token.save()
        return token

    @staticmethod
    def check_sign(sign):
        """ 校验签名"""
        try:
            md5_token, token_code = sign.split('-')
            token = AccessTokens.query.filter_by(token=token_code).first()

            m1 = hashlib.md5()
            m1.update('{}{}'.format(token_code, token.time).encode())
            md5_token_copy = m1.hexdigest()

            if md5_token == md5_token_copy:
                # 删除签名
                token.delete()
                return True
            return False

        except Exception as e:
            return False

    def get_categories(self, pid):
        if pid == '':
            categories = Categories.query.all()
        else:
            categories = Categories.query.filter_by(pid=pid).all()

        return categories

    def add_article(self, **kwargs):
        # params = {
        #     'title': kwargs.get('title'),
        #     'content': kwargs.get('content'),
        #     'cate': kwargs.get('cate'),
        #     'uid': kwargs.get('uid')
        # }
        title = kwargs.get('title')
        content = kwargs.get('content')
        cate = kwargs.get('cate')
        uid = kwargs.get('uid')
        random = kwargs.get('random')

        # 校验用户合法性
        user = Members.query.filter_by(openid=uid).one()
        if user.random != random:
            raise Exception('用户不合法')

        article = Articles(title=title, content=content, cate=cate, uid=user.id)
        article.save()

        user.integral += 10
        user.save()
        return article

    def delete_article(self, **kwargs):
        uid = kwargs.get('uid')
        random = kwargs.get('random')
        aid = kwargs.get('aid')

        # 校验用户合法性
        user = Members.query.filter_by(openid=uid, random=random).first()
        if not user:
            raise Exception('用户不合法')

        article = Articles.query.filter_by(id=aid).one()
        article.delete()

        return article

    def update_article(self, **kwargs):
        title = kwargs.get('title')
        content = kwargs.get('content')
        cate = kwargs.get('cate')
        uid = kwargs.get('uid')
        random = kwargs.get('random')
        aid = kwargs.get('aid')

        # 校验用户合法性
        user = Members.query.filter_by(openid=uid, random=random).first()
        if not user:
            raise Exception('用户不合法')

        article = Articles.query.filter_by(id=aid).one()
        article.title = title
        article.content = content
        article.cate = cate
        article.save()

        return article

    def get_article(self, **kwargs):
        aid = kwargs.get('aid')
        article = Articles.query.filter_by(id=aid).one()
        return article

    def get_articles(self, **kwargs):
        uid = kwargs.get('uid')
        random = kwargs.get('random')
        page = kwargs.get('page')
        cate = kwargs.get('cate')

        if uid and random:
            user = Members.query.filter_by(openid=uid, random=random).first()
            if not user:
                raise Exception('用户不合法')

        nums = 10
        query = Articles.query
        if cate and int(cate) != 0:
            query = query.filter_by(cate=cate)
        articles = query.order_by(desc('id')).offset((page - 1) * nums).limit(nums).all()
        return articles

    def get_user(self, **kwargs):
        uid = kwargs.get('uid')
        random = kwargs.get('random')

        user = Members.query.filter_by(openid=uid).one()
        if user.random != random:
            raise Exception('用户不合法')

        return user

    def get_user_by_id(self, uid):
        user = Members.query.filter_by(id=uid).one()
        return user

    def get_articles_count(self):
        count = Articles.query.count()
        return count
