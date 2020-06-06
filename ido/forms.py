from wtforms import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    face = StringField('face', validators=[DataRequired()])
    random = StringField('random')
    integral = IntegerField('integral')
    remainder = IntegerField('remainder')
    regtime = IntegerField('regtime')


