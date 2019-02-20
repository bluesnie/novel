from wtforms import Form, TextField, StringField,PasswordField, validators, SubmitField

class LoginForm(Form):
    username = StringField("username", [validators.Required()])
    password = PasswordField("password", [validators.Required()])
    submit = SubmitField(u"登录")

