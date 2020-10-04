import os
from flask import Flask, render_template, session, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'learning makes me happy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/test?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    stu_num = db.Column(db.BigInteger(), unique=True, index=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64), unique=True)
    length = db.Column(db.Integer())
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class LoginForm(FlaskForm):
    username = StringField('Please input username', validators=[DataRequired()])
    password = StringField('Please input password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Please input username', validators=[DataRequired()])
    password = StringField('Please input password', validators=[DataRequired()])
    submit = SubmitField('Register')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    data = []
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
        if user is None:
            session['known'] = False
            return redirect(url_for('register'))
        else:
            session['known'] = True
            session['name'] = form.username.data
            return redirect(url_for('index'))
    if 'known' in session.keys():
        if session['known'] == True and session.get('name'):
            with open("./data/student_information.json", encoding='utf-8') as fin:
                data = json.loads(fin.read())['data']
    return render_template('index.html', data=data, form=form, name=session.get('name'),
                           known=session.get('known', False))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
        except:
            return render_template('500.html')

        return redirect(url_for('index'))
    return render_template('register.html', form=form)


# # 2.增加记录
# admin = User(username='admin', email='admin@example.com')
# guest = User(username='guest', email='guest@example.com')
# db.session.add(admin)
# db.session.add(guest)
# db.session.commit()
#
# # 3.查询记录,注意查询返回对象，如果查询不到返回None
# User.query.all()  # 查询所有
# User.query.filter_by(username='admin').first()  # 条件查询
# User.query.order_by(User.username).all()  # 排序查询
# User.query.limit(1).all()  # 查询1条
# User.query.get(id=123)  # 精确查询
#
# # 4.删除
# user = User.query.get(id=123)
# db.session.delete(user)
# db.session.commit()

if __name__ == '__main__':
    app.run(debug=False)
