from flask.ext.wtf import Form, TextField, Required, PasswordField


class LoginForm(Form):
    email = TextField('email', validators=[Required()])
    password = PasswordField('password', validators=[Required()])


class RegisterForm(Form):
    email = TextField('email', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
