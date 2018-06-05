import re
import requests, json, random, string
from flask import Flask, render_template, request, redirect, url_for, abort, session, json, jsonify 
from flask.ext.wtf import Form
from wtforms import Form, BooleanField, TextField, PasswordField, validators, StringField, SubmitField, HiddenField
from wtforms.validators import Required
from flask.ext.mail import Message, Mail
mail = Mail()
app = Flask(__name__)
app.config['SECRET_KEY'] = '435345fdsg3vdfg3r4dsdfd'

app.config.update(dict(
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'rahulraman.abes@gmail.com',
    MAIL_PASSWORD = 'Rahul123'
))

mail.init_app(app)
class MessageForm(Form):
    message = TextField(u'message', [validators.Length(min=4, max=25)])
    email = TextField('Email Address', [validators.Length(min=6, max=35)])
    fb_id = HiddenField('Facebook Id')
    submit = SubmitField('Submit')

SIMPLE_CHARS = string.ascii_letters + string.digits

def get_random_string(length=8):
    return ''.join(random.choice(SIMPLE_CHARS) for i in xrange(length))

def is_email_address_valid(email):
    """Validate the email address using a regex."""
    if not re.match("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$", email):
        return False
    return True

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender='rahulraman.abes@gmail.com'
    )
    mail.send(msg)

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
			url = 'https://graph.facebook.com/'+fb_id_data+'?fields=id,name,picture,link'
			fb_data = requests.get(url)
			pwd = get_random_string()
			html = render_template('mail.html', data = json.loads(fb_data.content), email = email_data, pwd = pwd)
			send_email(email_data, "Your Message Post Successfully", html)
#			msg = Message("Your Message post successfully",
 #                 sender=app.config['MAIL_DEFAULT_SENDER'],
  #                recipients=[email_data],
   #               html = html)
	#		msg.body = "testing1"
	#		msg.html = "<b>testing2</b>"
	#		mail.send(msg)
			return "Executed Successfully"
   #     user = User(form.username.data, form.email.data,
    #                form.password.data)
   #     db_session.add(user)
    #    flash('Thanks for registering')
     #   return 'email'
    return render_template('register.html', form=form,user = request.args.get('user_id',''))


if __name__ == '__main__':
    app.run(debug=True)
