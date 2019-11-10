# coding:utf8
import datetime
import json, requests, re
import os
import uuid
from functools import wraps
from flask import render_template, redirect, url_for, request, flash, session, Response
from werkzeug.utils import secure_filename
from app import db, app, rds
from . import home
from app.home.forms import RegistForm, LoginForm, UserdetailForm, PasswordForm, CommentForm
from app.models import User, Userlog, Comment, Movie, Moviecol, Preview, Tag
from werkzeug.security import generate_password_hash


# 登入装饰器
def user_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('home.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 上传文件名
def change_filename(filename):
    fileinfo = filename.split('.')[-1]
    filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex) + '.' + fileinfo
    return filename


# 查看会员是否登入
def user_login():
    user_login = None
    if ('user_id' in session):
        user_login = User.query.filter_by(id=session['user_id']).first()
    return user_login


# 查询ip地址所在的
def queryIpAddress(ipaddress):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    reaponse = requests.get("https://www.ip.cn/?ip={}".format(ipaddress), headers=headers).text
    address = re.findall('<p>所在地理位置：<code>(.*?)</code>', reaponse)[0].split(' ')[0]
    return address


# 首页
@home.route('/<int:page>/', methods=['GET'])
def index(page=None):
    tags = Tag.query.all()
    page_data = Movie.query

    title_id = request.args.get('title_id', 0)
    if int(title_id) != 0:
        page_data = page_data.filter_by(tag_id=int(title_id))

    star = request.args.get('star', 0)
    if star in ('一', '二', '三', '四', '五'):
        stars = {
            '一': '1',
            '二': '2',
            '三': '3',
            '四': '4',
            '五': '5'
        }
        page_data = page_data.filter_by(star=stars[star])

    time = request.args.get('time', 0)
    if time in ('1', '2019', '2018', '2018', '2'):
        if int(time) == 1:
            page_data = page_data.order_by(
                Movie.addtime.desc()
            )
        elif int(time) == 2:
            page_data = page_data.order_by(
                Movie.addtime.asc()
            )

    play_num = request.args.get('play_num', 0)
    if int(play_num) != 0:
        if int(play_num) == 1:
            page_data = page_data.order_by(
                Movie.playnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.playnum.asc()
            )

    comment_num = request.args.get('comment_num', 0)
    if int(comment_num) != 0:
        if int(comment_num) == 1:
            page_data = page_data.order_by(
                Movie.commentnum.desc()
            )
        else:
            page_data = page_data.order_by(
                Movie.commentnum.asc()
            )
    if page is None:
        page = 1
    page_data = page_data.paginate(page=page, per_page=10)

    movie_description = dict(
        title_id=title_id,
        star=star,
        time=time,
        play_num=play_num,
        comment_num=comment_num
    )
    return render_template('home/index.html', tags=tags, movie_description=movie_description, page_data=page_data,
                           user_login=user_login())


# 登入
@home.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data['name']).first()
        if not user.check_password(data['password']):
            flash('密码错误！', 'error')
            return redirect(url_for('home.login'))
        session['user'] = data['name']
        session['user_id'] = user.id
        userlog = Userlog(
            user_id=user.id,
            ip=request.remote_addr,
            ip_area=queryIpAddress(request.remote_addr)
        )
        db.session.add(userlog)
        db.session.commit()
        return redirect(request.args.get('next') or url_for('home.user'))
    return render_template('home/login.html', form=form)


# 退出
@home.route('/logout/')
@user_login_req
def logout():
    session.pop('user', None)
    session.pop('user_id', None)
    return redirect(url_for('home.login'))


# 搜索
@home.route('/search/<int:page>/', methods=['GET', 'POST'])
def search(page=None):
    if page is None:
        page = 1
    key = request.args.get('key', '')
    key_num = Movie.query.filter(
        Movie.title.ilike('%' + key + '%')
    ).count()
    page_data = Movie.query.filter(
        Movie.title.ilike('%' + key + '%')
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page, per_page=10)
    page_data.key = key
    return render_template('home/search.html', key=key, page_data=page_data, key_num=key_num, user_login=user_login())


# 注册
@home.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            password=generate_password_hash(data['password']),
            uuid=uuid.uuid4().hex
        )
        db.session.add(user)
        db.session.commit()
        flash('注册成功！', 'ok')
    return render_template('home/register.html', form=form)


# 用户
@home.route('/user/', methods=['GET', 'POST'])
@user_login_req
def user():
    form = UserdetailForm()
    form.face.validators = []
    user = User.query.get(session['user_id'])
    if request.method == 'GET':
        form.name.data = user.name
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
    if form.validate_on_submit():
        data = form.data
        # file_face = secure_filename(form.face.data.filename)
        # if not os.path.exists(app.config['FC_DIR']):
        #     os.makedirs(app.config['FC_DIR'])
        #     os.chmod(app.config['FC_DIR'], 'rw')
        if not os.path.exists(app.config['FC_DIR']):
            os.makedirs(app.config['FC_DIR'])
            os.chmod(app.config['FC_DIR'], 'rw')

        if form.face.data.filename != '':
            file_face = secure_filename(form.face.data.filename)
            user.face = change_filename(file_face)
            form.face.data.save(app.config['FC_DIR'] + user.face)

        # user.face = change_filename(file_face)
        # form.face.data.save(app.config['FC_DIR'] + user.face)

        name_count = User.query.filter_by(name=data['name']).count()
        if data['name'] != user.name and name_count == 1:
            flash('昵称已经存在！', 'error')
            return redirect(url_for('home.user'))
        email_count = User.query.filter_by(email=data['email']).count()
        if data['email'] != user.email and email_count == 1:
            flash('邮箱已经存在！', 'error')
            return redirect(url_for('home.user'))
        phone_count = User.query.filter_by(phone=data['phone']).count()
        if data['phone'] != user.phone and phone_count == 1:
            flash('电话号码已经存在！', 'error')
            return redirect(url_for('home.user'))

        user.name = data['name']
        user.email = data['email']
        user.phone = data['phone']
        user.info = data['info']
        db.session.add(user)
        db.session.commit()
        flash('修改资料成功', 'ok')
        return redirect(url_for('home.user'))
    return render_template('home/user.html', form=form, user=user, user_login=user_login())


# 修改密码
@home.route('/password/', methods=['GET', 'POST'])
@user_login_req
def password():
    form = PasswordForm()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=session['user']).first()
        from werkzeug.security import generate_password_hash
        user.password = generate_password_hash(data['new_password'])
        db.session.add(user)
        db.session.commit()
        flash('修改密码成功！', 'ok')
        return redirect(url_for('home.logout'))
    return render_template('home/password.html', form=form, user_login=user_login())


# 评论
@home.route('/comments/<int:page>/', methods=['GET'])
@user_login_req
def comments(page=None):
    if page is None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Comment.movie_id,
        User.id == session['user_id']
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/comments.html', page_data=page_data, user_login=user_login())


# 登入记录
@home.route('/loginlog/<int:page>/', methods=['GET'])
@user_login_req
def loginlog(page=None):
    if page is None:
        page = 1
    page_data = Userlog.query.join(
        User
    ).filter(
        User.id == session['user_id']
    ).order_by(
        Userlog.sign_in_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/loginlog.html', page_data=page_data, user_login=user_login())


# 收藏
@home.route('/moviecol/<int:page>/', methods=['GET'])
@user_login_req
def moviecol(page=None):
    if page is None:
        page = 1
    page_data = Moviecol.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Moviecol.movie_id,
        User.id == session['user_id']
    ).order_by(
        Moviecol.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('home/moviecol.html', page_data=page_data, user_login=user_login())


# 添加收藏
@home.route('/moviecol/add/', methods=['GET'])
@user_login_req
def moviecol_add():
    uid = request.args.get('uid', '')
    mid = request.args.get('mid', '')
    moviecol = Moviecol.query.filter_by(
        user_id=int(uid),
        movie_id=int(mid)
    ).count()
    if moviecol == 1:
        data = dict(ok=0)
    if moviecol == 0:
        moviecol = Moviecol(
            user_id=int(uid),
            movie_id=int(mid)
        )
        db.session.add(moviecol)
        db.session.commit()
        data = dict(ok=1)
    return json.dumps(data)


@home.route('/animation/')
def animation():
    data = Preview.query.all()
    return render_template('home/animation.html', data=data)


# 播放页面
@home.route('/play/<int:id><int:page>', methods=['GET', 'POST'])
def play(id=None, page=None):
    movie = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id,
        Movie.id == int(id)
    ).first_or_404()
    movie.playnum += 1
    form = CommentForm()

    if page is None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == movie.id,
        # User.id == session['user_id']
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)

    if 'user' in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content=data['comment'],
            movie_id=movie.id,
            user_id=session['user_id']
        )
        db.session.add(comment)
        db.session.commit()
        flash('评论发布成功！', 'ok')
        movie.commentnum += 1
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('home.play', id=movie.id, page=1))
    db.session.add(movie)
    db.session.commit()
    return render_template('home/play.html', movie=movie, form=form, page_data=page_data)


# 播放页面
@home.route('/dplayer/<int:id>/<int:page>/', methods=['GET', 'POST'])
def dplayer(id=None, page=None):
    movie = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id,
        Movie.id == int(id)
    ).first_or_404()
    movie.playnum += 1
    form = CommentForm()

    if page is None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == movie.id,
        # User.id == session['user_id']
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)

    if 'user' in session and form.validate_on_submit():
        data = form.data
        comment = Comment(
            content=data['comment'],
            movie_id=movie.id,
            user_id=session['user_id']
        )
        db.session.add(comment)
        db.session.commit()
        flash('评论发布成功！', 'ok')
        movie.commentnum += 1
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for('home.dplayer', id=movie.id, page=1))
    db.session.add(movie)
    db.session.commit()
    print(movie.movie_head, movie.movie_tail)
    return render_template('home/dplayer.html', movie=movie, form=form, page_data=page_data, user_login=user_login())


@home.route('/barrage/v3/', methods=['GET', 'POST'])
def barrage():
    # 获取弹幕消息队列
    if request.method == 'GET':
        id = request.args.get('id')
        key = 'movie' + str(id)
        if rds.llen(key):
            msgs = rds.lrange(key, 0, 2999)
            res = {
                'code': 0,
                'data': [json.loads(v) for v in msgs]
            }
        else:
            res = {
                'code': 0,
                'data': []
            }
        resp = json.dumps(res)
    # 添加弹幕
    if request.method == 'POST':
        if 'user' not in session:
            flash('您还没有登入，请先登入再使用弹幕功能！', 'barrage')
        else:
            data = json.loads(request.get_data())
            msg = [
                data['time'],
                data['type'],
                data['color'],
                session['user_id'],
                data['text']
            ]
            res = {
                'code': 0,
                'data': msg
            }
            resp = json.dumps(res)
            rds.lpush('movie' + data['id'], json.dumps(msg))
    return Response(resp, mimetype='application/json')

@home.route('/test/', methods=['GET', 'POST'])
def test():

    return render_template('home/test.html')
