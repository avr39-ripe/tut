from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, DecimalField, FloatField
from wtforms.validators import Required

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)

class ConfigForm(Form):
    temp_set = DecimalField('temp_set')
    temp_delta = DecimalField('temp_delta')
    valve_work = DecimalField('valve_work')
    valve_delta = DecimalField('valve_delta')
