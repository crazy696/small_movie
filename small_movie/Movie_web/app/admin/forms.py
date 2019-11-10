# coding:utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, SelectMultipleField, FileField, TextAreaField, \
    RadioField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from app.models import Admin, Tag, Role, Auth

tag_list = Tag.query.all()
auth_list = Auth.query.all()
role_list = Role.query.all()


class LoginForm(FlaskForm):
    account = StringField(
        label='账号',
        validators=[DataRequired('请输入账号!')],
        description='账号',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入账号...',
            # 'required': 'required'
        }
    )

    password = PasswordField(
        label='密码',
        validators=[DataRequired('请输入密码!')],
        description='密码',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入密码...",
            # 'required': 'required'
        }
    )

    submit = SubmitField(
        '登入',
        render_kw={
            'class': "btn btn-primary btn-block btn-flat",
            'style': "text-align:center"
        }
    )

    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError('账号不存在！')


class TagForm(FlaskForm):
    name = StringField(
        label='名称',
        validators=[DataRequired('请输入标签!')],
        description='标签',
        render_kw={
            'class': 'form-control',
            'id': 'input',
            'placeholder': '请输入标签...',
            # 'required': 'required'
        }
    )

    submit = SubmitField(
        '提交',
        render_kw={
            'class': "btn btn-primary"
        }
    )


class MovieForm(FlaskForm):
    title = StringField(
        label='片名',
        validators=[DataRequired('请输入片名!')],
        description='片名',
        render_kw={
            'class': 'form-control',
            'id': 'input_title',
            'placeholder': '请输入片名...'
        }
    )

    url = FileField(
        label='文件',
        validators=[DataRequired('请上传文件!')],
        description='文件',
    )

    # info = TextAreaField(
    #     label='简介',
    #     validators=[DataRequired('请输入简介!')],
    #     description='简介',
    #     render_kw={
    #         'class': 'form-control',
    #         'rows': 10
    #     }
    # )

    logo = FileField(
        label='封面',
        validators=[DataRequired('请上传封面!')],
        description='封面',
    )

    # star = SelectField(
    #     label='星级',
    #     validators=[DataRequired('请选择星级!')],
    #     coerce=int,
    #     choices=[(1, '1星'), (2, '2星'), (3, '3星'), (4, '4星'), (5, '5星')],
    #     description='星级',
    #     render_kw={
    #         'class': 'form-control',
    #     }
    # )

    tag_id = SelectField(
        label='标签',
        validators=[DataRequired('请选择标签!')],
        coerce=int,
        choices=[(v.id, v.title) for v in tag_list],
        description='标签',
        render_kw={
            'class': 'form-control',
        }
    )

    # area = StringField(
    #     label='地区',
    #     validators=[DataRequired('请输入地区！')],
    #     description='片名',
    #     render_kw={
    #         'class': 'form-control',
    #         'placeholder': '请输入地区...'
    #     }
    # )

    # length = StringField(
    #     label='片长',
    #     validators=[DataRequired('请输入片长！')],
    #     description='片长',
    #     render_kw={
    #         'class': 'form-control',
    #         'placeholder': '请输入片长...'
    #     }
    # )

    movie_head = StringField(
        label='片头时间',
        validators=[DataRequired('请输入片头！')],
        description='片头',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入片头...'
        }
    )

    movie_tail = StringField(
        label='片尾时间',
        validators=[DataRequired('请输入片尾！')],
        description='片尾',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入片尾...'
        }
    )

    # release_time = StringField(
    #     label='上映时间',
    #     validators=[DataRequired('请选择上映时间！')],
    #     description='上映时间',
    #     render_kw={
    #         'class': 'form-control',
    #         'placeholder': '请选择上映时间...',
    #         'id': 'input_release_time',
    #     }
    # )

    submit = SubmitField(
        '提交',
        render_kw={
            'class': "btn btn-primary"
        }
    )


# 预告
class PreviewForm(FlaskForm):
    title = StringField(
        label='片名',
        validators=[DataRequired('请输入片名!')],
        description='片名',
        render_kw={
            'class': 'form-control',
            'id': 'input_title',
            'placeholder': '请输入片名...'
        }
    )

    logo = FileField(
        label='封面',
        validators=[DataRequired('请上传封面!')],
        description='封面',
    )

    submit = SubmitField(
        '提交',
        render_kw={
            'class': "btn btn-primary"
        }
    )


class RoleForm(FlaskForm):
    name = StringField(
        label='角色名称',
        validators=[DataRequired('请输入角色名称!')],
        description='角色名称',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入角色名称...',
        }
    )

    auths = SelectMultipleField(
        label='权限列表',
        validators=[DataRequired('请选择权限列表!')],
        coerce=int,
        choices=[(v.id, v.name) for v in auth_list],
        description='权限列表',
        render_kw={
            'class': 'form-control',
        }
    )

    submit = SubmitField(
        '提交',
        render_kw={
            'class': "btn btn-primary"
        }
    )

    def validate_account(self, field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError('账号不存在！')


class AdminForm(FlaskForm):
    name = StringField(
        label='管理员名称',
        validators=[DataRequired('请输入管理员名称!')],
        description='管理员名称',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入管理员名称...',
        }
    )

    password = PasswordField(
        label='密码',
        validators=[DataRequired('请输入密码!')],
        description='密码',
        render_kw={
            'class': "form-control",
            'placeholder': "请输入密码...",
        }
    )

    repeat_password = PasswordField(
        label='重复密码',
        validators=[DataRequired('请输入重复密码!'), EqualTo('password', message='两次密码不一致')],
        description='重复密码',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入重复密码...',
        }
    )

    is_super = RadioField(
        label='是否为超级管理员',
        # validators=[DataRequired()],
        choices=[('0', '是'), ('1', '否')],
    )

    role = SelectField(
        label='所属角色',
        coerce=int,
        choices=[(v.id, v.name) for v in role_list],
        render_kw={
            'class': "form-control",
        }
    )

    submit = SubmitField(
        '提交',
        render_kw={
            'class': "btn btn-primary"
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
        '编辑',
        render_kw={
            'class': "btn btn-primary"
        }
    )

    def validate_old_password(self, field):
        from flask import session
        password = field.data
        name = session['admin']
        admin = Admin.query.filter_by(
            name=name
        ).first()
        if not admin.check_password(password):
            raise ValidationError('旧密码错误！')


class AuthForm(FlaskForm):
    name = StringField(
        label='权限名称',
        validators=[
            DataRequired('请输入权限名称!')
        ],
        description='权限名称',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入权限名称!'
        }
    )

    url = StringField(
        label='权限地址',
        validators=[
            DataRequired('请输入权限地址!')
        ],
        description='权限地址',
        render_kw={
            'class': 'form-control',
            'placeholder': '请输入权限地址!'
        }
    )

    submit = SubmitField(
        '提交',
        render_kw={
            'class': "btn btn-primary"
        }
    )


