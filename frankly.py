import re
from flask import Flask, render_template, request, redirect, url_for, abort, session
from flask.ext.wtf import Form
from wtforms import Form, BooleanField, TextField, PasswordField, validators, StringField, SubmitField, HiddenField
from wtforms.validators import Required
from flask.ext.mail import Message, Mail
mail = Mail()
app = Flask(__name__)
app.config['SECRET_KEY'] = '435345fdsg3vdfg3r4dgdf'

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'rahulraman.abes@gmail.com',
    MAIL_PASSWORD = 'Rahul10?'
))

mail.init_app(app)
class MessageForm(Form):
    message = TextField(u'message', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    fb_id = HiddenField('Facebook Id')
    submit = SubmitField('Submit')


def is_email_address_valid(email):
    """Validate the email address using a regex."""
    if not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email):
        return False
    return True

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("test.html", form = 'esdf')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = MessageForm(request.form)
    form.fb_id.data = request.args.get('user_id','')
    if request.method == 'POST' and form.validate():
 #   	form = request.form
		email_data = form.email.data
		message_data = form.message.data
		fb_id_data = form.fb_id.data
		if not is_email_address_valid(email_data):
 			return render_template("register.html", errors = 'Kindly enter a valid email',form=form)
		else:
			msg = Message("Hello",
                  sender="rahulraman.abes@gmail.com",
                  recipients=["007rahulraman@gmail.com"])
			msg.body = "testing"
			msg.html = "<b>testing</b>"
			mail.send(msg)
			return 'test'
   #     user = User(form.username.data, form.email.data,
    #                form.password.data)
   #     db_session.add(user)
    #    flash('Thanks for registering')
     #   return 'email'
    return render_template('register.html', form=form,user = request.args.get('user_id',''))


if __name__ == '__main__':
    app.run(debug=True)