# coding:utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SelectField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, ValidationError
from app.models import User


class RegistForm(FlaskForm):
    name = StringField(
        label='昵称',
        validators=[DataRequired('请输入昵称!')],
        description='昵称',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入昵称...',
        }
    )

    email = StringField(
        label='邮箱',
        validators=[
            DataRequired('请输入邮箱!'),
            Email('邮箱格式不正确！')
        ],
        description='邮箱',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入邮箱...',
        }
    )

    phone = StringField(
        label='手机',
        validators=[
            DataRequired('请输入手机!'),
            Regexp('1[3458]\\d{9}', message='手机号码格式不正确！')
        ],
        description='手机',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入手机...',
        }
    )

    password = PasswordField(
        label='密码',
        validators=[DataRequired('请输入密码!')],
        description='密码',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请输入密码...",
        }
    )

    repeat_password = PasswordField(
        label='重复密码',
        validators=[DataRequired('请输入重复密码!'), EqualTo('password', message='两次密码不一致')],
        description='重复密码',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入重复密码...',
        }
    )

    submit = SubmitField(
        '注册',
        render_kw={
            'class': "btn btn-lg btn-success btn-block"
        }
    )


class LoginForm(FlaskForm):
    name = StringField(
        label='账号',
        validators=[DataRequired('请输入账号/昵称!')],
        description='账号',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入账号/昵称...',
        }
    )
    password = PasswordField(
        label='密码',
        validators=[DataRequired('请输入密码!')],
        description='密码',
        render_kw={
            'class': "form-control input-lg",
            'placeholder': "请输入密码...",
        }
    )
    submit = SubmitField(
        '登入',
        render_kw={
            'class': "btn btn-lg btn-primary btn-block"
        }
    )

    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user == 0:
            raise ValidationError('账号不存在！')


class UserdetailForm(FlaskForm):
    name = StringField(
        label='昵称',
        validators=[DataRequired('请输入昵称!')],
        description='昵称',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入昵称...',
        }
    )

    email = StringField(
        label='邮箱',
        validators=[
            DataRequired('请输入邮箱!'),
            Email('邮箱格式不正确！')
        ],
        description='邮箱',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入邮箱...',
        }
    )

    phone = StringField(
        label='手机',
        validators=[
            DataRequired('请输入手机!'),
            Regexp('1[3458]\\d{9}', message='手机号码格式不正确！')
        ],
        description='手机',
        render_kw={
            'class': 'form-control input-lg',
            'placeholder': '请输入手机...',
        }
    )

    face = FileField(
        label='头像',
        validators=[DataRequired('请上传头像!')],
        description='头像',
    )

    info = TextAreaField(
        label='简介',
        validators=[DataRequired('请输入简介!')],
        description='简介',
        render_kw={
            'class': 'form-control',
            'rows': 10
        }
    )

    submit = SubmitField(
        '保存修改',
        render_kw={
            'class': "btn btn-success"
        }
    )


class PasswordForm(FlaskForm):
    old_password = PasswordField(
        label='旧密码',
        validators=[
            DataRequired('请输入旧密码!')
        ],
        description='旧密码',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入旧密码!'
        }
    )

    new_password = PasswordField(
        label='新密码',
        validators=[
            DataRequired('请输入新密码!')
        ],
        description='新密码',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入新密码!'
        }
    )

    repeat_password = PasswordField(
        label='重复密码',
        validators=[DataRequired('请输入重复密码!'), EqualTo('new_password', message='两次密码不一致')],
        description='重复密码',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入重复密码...',
        }
    )

    submit = SubmitField(
        '提交',
        render_kw={
            'class': "btn btn-primary"
        }
    )

    def validate_old_password(self, field):
        from flask import session
        password = field.data
        name = session['user']
        user = User.query.filter_by(
            name=name
        ).first()
        if not user.check_password(password):
            raise ValidationError('旧密码错误！')


class CommentForm(FlaskForm):
    comment = TextAreaField(
        label='内容',
        validators=[
            DataRequired('请输入评论内容!')
        ],
        description='内容',
        render_kw={
            # 'class': 'form-control',
            'id': 'input_content',
            'class': 'edui-default'
            'style'
        }
    )

    submit = SubmitField(
        '提交评论',
        render_kw={
            'class': "btn btn-success",
            'id': 'btn-sub'
        }
    )
