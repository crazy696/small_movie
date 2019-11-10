# coding:utf8
from datetime import datetime
from app import db

# 会员注册
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 昵称
    password = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100), unique=True)  # 邮箱
    phone = db.Column(db.String(11), unique=True)  # 手机
    face = db.Column(db.String(255), unique=True)  # 头像
    info = db.Column(db.Text)  # 个性简介
    registered_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间
    uuid = db.Column(db.String(255), unique=True)  # 唯一标志符
    userlogs = db.relationship('Userlog', backref='user')  # 会员日志外键关系绑定
    comments = db.relationship('Comment', backref='user')  # 评论外键关系绑定
    moviecols = db.relationship('Moviecol', backref='user')  # 收藏外键关系绑定

    def __repr__(self):
        return '<注册用户 %r>' % self.name

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)


# 会员登入日志
class Userlog(db.Model):
    __tablename__ = 'userlog'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 会员
    ip = db.Column(db.String(100))  # 登入ip
    ip_area = db.Column(db.String(100))  # 登入ip
    sign_in_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 登入时间

    def __repr__(self):
        return '<登入日志 %r>' % self.name


# 标签
class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(100), unique=True)  # 标题
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    movies = db.relationship('Movie', backref='tag')  # 电影外键关系绑定

    def __repr__(self):
        return '<标签 %r>' % self.title


# 电影
class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    url = db.Column(db.String(255), unique=True)  # 地址
    info = db.Column(db.Text)  # 简介
    logo = db.Column(db.String(255), unique=True)  # 封面
    star = db.Column(db.SmallInteger)  # 星级
    playnum = db.Column(db.BigInteger)  # 播放量
    commentnum = db.Column(db.BigInteger)  # 评论量
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 所属标签
    area = db.Column(db.String(255))  # 上映地区
    release_time = db.Column(db.Date)  # 上映时间
    length = db.Column(db.String(100))  # 播放时间
    movie_head = db.Column(db.Integer)
    movie_tail = db.Column(db.Integer)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    comments = db.relationship('Comment', backref='movie')  # 评论外键关系绑定
    moviecols = db.relationship('Moviecol', backref='movie')  # 收藏外键关系绑定

    def __repr__(self):
        return '<电影 %r>' % self.title


# 预告
class Preview(db.Model):
    __tablename__ = 'preview'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)  # 封面
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return '<预告 %r>' % self.title


# 评论
class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    content = db.Column(db.String(255), unique=True)  # 内容
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return '<评论 %r>' % self.id


# 收藏
class Moviecol(db.Model):
    __tablename__ = 'moviecol'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return '<收藏 %r>' % self.id


# 权限
class Auth(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100))  # 名称
    url = db.Column(db.String(255))  # 地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return '<权限 %r>' % self.name


# 角色
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100))  # 名称
    auths = db.Column(db.String(600))  # 创作者
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    admins = db.relationship('Admin', backref='role')  # 管理员外键关系绑定

    def __repr__(self):
        return '<角色 %r>' % self.name


# 管理员
class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 管理员账号
    password = db.Column(db.String(100))  # 管理员密码
    is_super = db.Column(db.SmallInteger)  # 是否魏超级管理员，是为0
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # 所属角色
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    adminlogs = db.relationship('Adminlog', backref='admin')  # 管理员登入日志外键关系绑定
    oplogs = db.relationship('Oplog', backref='admin')  # 管理员操作日志外键关系绑定

    def __repr__(self):
        return '<管理员 %r>' % self.name

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password, password)


# 管理员登入日志
class Adminlog(db.Model):
    __tablename__ = 'adminlog'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登入ip
    sign_in_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 登入时间

    def __repr__(self):
        return '<管理员登入日志 %r>' % self.name



# 管理员操作日志
class Oplog(db.Model):
    __tablename__ = 'oplog'
    id = db.Column(db.Integer, primary_key=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属管理员
    ip = db.Column(db.String(100))  # 登入ip
    reason = db.Column(db.String(600))  # 操作原因
    sign_in_time = db.Column(db.DateTime, index=True, default=datetime.now)  # 登入时间

    def __repr__(self):
        return '<管理员操作日志 %r>' % self.name


if __name__ == "__main__":
    # db.create_all()
    pass
    '''role = Role(
        name='超级管理员',
        auths=''
    )
    db.session.add(role)
    db.session.commint()
    from werkzeug.security import generate_password_hash

    admin = Admin(
        name='',
        password=generate_password_hash('526891'),
        is_super=0,
        role_id=1
    )
    db.session.add(admin)
    db.session.commint()'''