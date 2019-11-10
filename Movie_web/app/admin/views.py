# coding:utf8
import datetime
import os
import time
import urllib
import uuid
from lxml import etree
import requests
from selenium import webdriver
from sqlalchemy import or_
from werkzeug.utils import secure_filename
from app import db, app
from app.models import Admin, Tag, Role, Movie, Preview, User, Comment, Moviecol, Oplog, Adminlog, Userlog, Auth
from . import admin
from flask import render_template, redirect, url_for, flash, session, request, abort
from app.admin.forms import LoginForm, TagForm, RoleForm, AdminForm, MovieForm, PreviewForm, PasswordForm, AuthForm
from functools import wraps


# 获取当前时间
@admin.context_processor
def tpl_extra():
    data = dict(
        online_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )
    return data


# 登入装饰器
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            return redirect(url_for('admin.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


# 权限装饰器
def admin_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        admin = Admin.query.join(
            Role
        ).filter(
            Role.id == Admin.role_id,
            Admin.id == session['admin_id']
        ).first()
        auths = admin.role.auths
        auths = list(map(lambda v: int(v), auths.split(',')))
        auth_list = Auth.query.all()
        urls = ['/admin' + v.url for v in auth_list for val in auths if val == v.id]
        rule = request.url_rule
        # print(urls)
        # print(rule)
        if str(rule) not in urls:
            # abort(404)
            return redirect(url_for('admin.role_error'))
        return f(*args, **kwargs)

    return decorated_function


# 上传文件名
def change_filename(filename):
    fileinfo = filename.split('.')[-1]
    filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex) + '.' + fileinfo
    return filename


def Get_Html(url, flag):
    if flag == 1:
        chrome_options = 0
        #         #开启headless模式
        #         chrome_options = Options()
        #         chrome_options.add_argument('--headless')
        #         chrome_options.add_argument('--disable-gpu')
        #         chrome_options.add_argument("--no-sandbox")

        browser = webdriver.Chrome('/home/crazy696/Documents/work/Reptile/chromedriver70',
                                   chrome_options=chrome_options)
        browser.get(url)
        time.sleep(0.5)
        html = browser.page_source
        browser.__exit__()

    if flag == 2:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        html = requests.get(url, headers=headers).text
    return html


def Get_Info(movie_name):
    douban_html = Get_Html(
        'https://movie.douban.com/subject_search?search_text={}&cat=1002'.format(urllib.parse.quote(movie_name)), 1)
    douban_tree = etree.HTML(douban_html)
    mvoie_link = douban_tree.xpath('//div[@class="title"]//a/@href')
    movie_html = Get_Html(mvoie_link[0], 2)
    movie_tree = etree.HTML(movie_html)
    movie = {
        'movie_star': movie_tree.xpath('//strong/text()')[0],
        'movie_area': movie_tree.xpath('//div[@id="info"]/text()[10]')[0],
        'movie_release_time': movie_tree.xpath('//span[@property="v:initialReleaseDate"]/text()')[0].split('(')[0],
        'movie_length': movie_tree.xpath('//span[@property="v:runtime"]/@content')[0],
        'movie_info': ' '.join(movie_tree.xpath('//span[@property="v:summary"]/text()')).replace('\u3000', '').replace(
            ' ', '')
    }
    return movie


# 首页
@admin.route('/')
@admin_login_req
def index():
    return render_template('admin/index.html')


# 登入
@admin.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data['account']).first()
        if not admin.check_password(data['password']):
            flash('密码错误！', 'error')
            return redirect(url_for('admin.login'))
        session['admin'] = data['account']
        session['admin_id'] = admin.id
        adminlog = Adminlog(
            user_id=admin.id,
            ip=request.remote_addr
        )
        db.session.add(adminlog)
        db.session.commit()
        return redirect(request.args.get('next') or url_for('admin.index'))
    return render_template('admin/login.html', form=form)


# 退出
@admin.route('/logout/')
@admin_login_req
def logout():
    session.pop('admin', None)
    session.pop('admin_id', None)
    return redirect(url_for('admin.login'))


# 修改密码
@admin.route('/password/', methods=['GET', 'POST'])
@admin_login_req
def password():
    form = PasswordForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=session['admin']).first()
        from werkzeug.security import generate_password_hash
        admin.password = generate_password_hash(data['new_password'])
        db.session.add(admin)
        db.session.commit()
        flash('修改密码成功！', 'ok')
        return redirect(url_for('admin.logout'))
    return render_template('admin/password.html', form=form)


# 添加标签
@admin.route('/tag/add/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(title=data['name']).count()
        if tag == 1:
            flash('名称已经存在！', 'error')
            return redirect(url_for('admin.tag_add'))
        tag = Tag(
            title=data['name']
        )
        db.session.add(tag)
        db.session.commit()
        flash('添加标签成功', 'ok')
        oplog = Oplog(
            user_id=session['admin_id'],
            ip=request.remote_addr,
            reason='添加标签%s' % data['name']
        )
        db.session.add(oplog)
        db.session.commit()
    return render_template('admin/tag_add.html', form=form)


# 标签列表
@admin.route('/tag/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def tag_list(page=None):
    if page is None:
        page = 1
    page_data = Tag.query.order_by(
        Tag.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/tag_list.html', page_data=page_data)


# 删除标签
@admin.route('/tag/del/<int:id>/', methods=['GET'])
@admin_login_req
@admin_auth
def tag_delete(id=None):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash('删除标签成功！', 'ok')
    return redirect(url_for('admin.tag_list', page=1))


# 编辑标签
@admin.route('/tag/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def tag_edit(id=None):
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(title=data['name']).count()
        if tag.title != data['name'] and tag_count == 1:
            flash('名称已经存在！', 'error')
            return redirect(url_for('admin.tag_edit', id=id))
        tag.title = data['name']
        db.session.add(tag)
        db.session.commit()
        flash('添加标签成功', 'ok')
        redirect(url_for('admin.tag_edit', id=id))
    return render_template('admin/tag_edit.html', form=form, tag=tag)


# 搜索
@admin.route('/tag/list/search/<int:page>/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def tag_list_search(page=None):
    if page is None:
        page = 1
    key = request.args.get('key', '')
    key_num = Tag.query.filter(
        Tag.title.ilike('%' + key + '%')
    ).count()
    page_data = Tag.query.filter(
        Tag.title.ilike('%' + key + '%')
    ).order_by(
        Tag.addtime.desc()
    ).paginate(page=page, per_page=10)
    page_data.key = key
    return render_template('admin/tag_list_search.html', key=key, page_data=page_data, key_num=key_num)


# 添加电影
@admin.route('/movie/add/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():

        data = form.data
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(app.config['UP_DIR'] + 'Movie/' + url)
        form.logo.data.save(app.config['UP_DIR'] + 'Movie_Cover/' + logo)
        movie_info = Get_Info(data['title'])
        print(movie_info)
        movie = Movie(
            title=data['title'],
            url=url,
            info=movie_info['movie_info'],
            logo=logo,
            star=float(movie_info['movie_star']) * 10,
            playnum=0,
            commentnum=0,
            tag_id=data['tag_id'],
            area=movie_info['movie_area'],
            release_time=datetime.datetime.strptime(movie_info['movie_release_time'], "%Y-%m-%d"),
            length=movie_info['movie_length'],
            movie_head=60 * int(data['movie_head']),
            movie_tail=60 * int(data['movie_tail']),
        )
        db.session.add(movie)
        db.session.commit()
        flash('添加电影成功', 'ok')
        return redirect(url_for('admin.movie_add'))
    return render_template('admin/movie_add.html', form=form)


# 电影列表
@admin.route('/movie/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def movie_list(page=None):
    if page is None:
        page = 1
    page_data = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/movie_list.html', page_data=page_data)


# 删除电影
@admin.route('/movie/del/<int:id>/', methods=['GET'])
@admin_login_req
@admin_auth
def movie_delete(id=None):
    movie = Movie.query.filter_by(id=id).first_or_404()
    db.session.delete(movie)
    db.session.commit()
    flash('删除标签成功！', 'ok')
    return redirect(url_for('admin.movie_list', page=1))


# 编辑电影
@admin.route('/movie/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def movie_edit(id=None):
    form = MovieForm()
    form.url.validators = []
    form.logo.validators = []
    movie = Movie.query.get_or_404(id)
    if request.method == 'GET':
        # form.info.data = movie.info
        form.tag_id.data = movie.tag_id
        # form.star.data = movie.star
    if form.validate_on_submit():
        data = form.data
        movie_count = Movie.query.filter_by(title=data['title']).count()
        if movie.title != data['title'] and movie_count == 1:
            flash('片名已经存在！', 'error')
            return redirect(url_for('admin.movie_edit', id=id))

        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')
        if form.url.data.filename != '':
            file_url = secure_filename(form.url.data.filename)
            movie.url = change_filename(file_url)
            form.url.data.save(app.config['UP_DIR'] + 'Movie/' + movie.url)
        if form.logo.data.filename != '':
            file_logo = secure_filename(form.logo.data.filename)
            movie.logo = change_filename(file_logo)
            form.logo.data.save(app.config['UP_DIR'] + 'Movie_Cover/' + movie.logo)
        movie_info = Get_Info(data['title'])
        movie.title = data['title'],
        movie.info = movie_info['movie_info'],
        movie.star = float(movie_info['movie_star']) * 10,
        movie.tag_id = data['tag_id'],
        movie.area = movie_info['movie_area'],
        movie.release_time = datetime.datetime.strptime(movie_info['movie_release_time'], "%Y-%m-%d"),
        movie.length = movie_info['movie_length'],
        movie.movie_head = 60 * int(data['movie_head']),
        movie.movie_tail = 60 * int(data['movie_tail']),
        db.session.add(movie)
        db.session.commit()
        flash('添加电影成功', 'ok')
        return redirect(url_for('admin.movie_add'))
    return render_template('admin/movie_edit.html', form=form, movie=movie)


# 搜索
@admin.route('/movie/list/search/<int:page>/', methods=['GET', 'POST'])
@admin_login_req
# @admin_auth
def movie_list_search(page=None):
    if page is None:
        page = 1
    key = request.args.get('key', '')
    key_num = Movie.query.filter(or_(
        Movie.title.ilike('%' + key + '%'),
        Movie.area.ilike('%' + key + '%')
    )
    ).count()
    page_data = Movie.query.filter(or_(
        Movie.title.ilike('%' + key + '%'),
        Movie.area.ilike('%' + key + '%')
    )
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page, per_page=10)
    page_data.key = key
    return render_template('admin/movie_list_search.html', key=key, page_data=page_data, key_num=key_num)


# 添加预告
@admin.route('/preview/add/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def preview_add():
    form = PreviewForm()
    if form.validate_on_submit():
        data = form.data
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')
        logo = change_filename(file_logo)
        form.logo.data.save(app.config['UP_DIR'] + 'Preview_Cover/' + logo)
        preview = Preview(
            title=data['title'],
            logo=logo,
        )
        db.session.add(preview)
        db.session.commit()
        flash('添加预告成功', 'ok')
        return redirect(url_for('admin.preview_add'))
    return render_template('admin/preview_add.html', form=form)


# 预告列表
@admin.route('/preview/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def preview_list(page=None):
    if page is None:
        page = 1
    page_data = Preview.query.order_by(
        Preview.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/preview_list.html', page_data=page_data)


# 删除预告
@admin.route('/preview/del/<int:id>/', methods=['GET'])
@admin_login_req
@admin_auth
def preview_delete(id=None):
    preview = Preview.query.filter_by(id=id).first_or_404()
    db.session.delete(preview)
    db.session.commit()
    flash('删除标签成功！', 'ok')
    return redirect(url_for('admin.preview_list', page=1))


# 编辑预告
@admin.route('/preview/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def preview_edit(id=None):
    form = PreviewForm()
    form.logo.validators = []
    preview = Preview.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        preview_count = Preview.query.filter_by(title=data['title']).count()
        if preview.title != data['title'] and preview_count == 1:
            flash('预告名已经存在！', 'error')
            return redirect(url_for('admin.preview_edit', id=id))

        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config['UP_DIR'])
            os.chmod(app.config['UP_DIR'], 'rw')

        if form.logo.data.filename != '':
            file_logo = secure_filename(form.logo.data.filename)
            preview.logo = change_filename(file_logo)
            form.logo.data.save(app.config['UP_DIR'] + 'Preview_Cover/' + preview.logo)

        preview.title = data['title'],
        db.session.add(preview)
        db.session.commit()
        flash('添加电影成功', 'ok')
        return redirect(url_for('admin.preview_add'))
    return render_template('admin/preview_edit.html', form=form, preview=preview)


# 搜索
@admin.route('/preview/list/search/<int:page>/', methods=['GET', 'POST'])
@admin_login_req
# @admin_auth
def preview_list_search(page=None):
    if page is None:
        page = 1
    key = request.args.get('key', '')
    key_num = Preview.query.filter(
        Preview.title.ilike('%' + key + '%')
    ).count()
    page_data = Preview.query.filter(
        Preview.title.ilike('%' + key + '%')
    ).order_by(
        Preview.addtime.desc()
    ).paginate(page=page, per_page=10)
    page_data.key = key
    return render_template('admin/preview_list_search.html', key=key, page_data=page_data, key_num=key_num)


# 会员列表
@admin.route('/user/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def user_list(page=None):
    if page is None:
        page = 1
    page_data = User.query.order_by(
        User.registered_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/user_list.html', page_data=page_data)


# 会员详情页
@admin.route('/user/view/<int:id>/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def user_view(id=None):
    view_data = User.query.get_or_404(id)
    return render_template('admin/user_view.html', view_data=view_data)


# 删除会员
@admin.route('/user/del/<int:id>/', methods=['GET'])
@admin_login_req
@admin_auth
def user_delete(id=None):
    user = User.query.filter_by(id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    flash('删除评论成功！', 'ok')
    return redirect(url_for('admin.user_list', page=1))

# 搜索
@admin.route('/user/list/search/<int:page>/', methods=['GET', 'POST'])
@admin_login_req
# @admin_auth
def user_list_search(page=None):
    if page is None:
        page = 1
    key = request.args.get('key', '')
    key_num = User.query.filter(or_(
        User.name.ilike('%' + key + '%'),
        User.email.ilike('%' + key + '%'),
        User.phone.ilike('%' + key + '%')
    )
    ).count()
    page_data = User.query.filter(or_(
        User.name.ilike('%' + key + '%'),
        User.email.ilike('%' + key + '%'),
        User.phone.ilike('%' + key + '%')
    )
    ).order_by(
        User.registered_time.desc()
    ).paginate(page=page, per_page=10)
    page_data.key = key
    return render_template('admin/user_list_search.html', key=key, page_data=page_data, key_num=key_num)


# 评论列表
@admin.route('/comment/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def comment_list(page=None):
    if page is None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Comment.movie_id,
        User.id == Comment.user_id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/comment_list.html', page_data=page_data)


# 搜索
@admin.route('/comment/list/search/<int:page>/', methods=['GET', 'POST'])
@admin_login_req
# @admin_auth
def comment_list_search(page=None):
    if page is None:
        page = 1
    key = request.args.get('key', '')
    key_num = Comment.query.filter(or_(
        Comment.content.ilike('%' + key + '%'),
        Comment.movie_id.ilike('%' + key + '%'),
        Comment.user_id.ilike('%' + key + '%')
    )
    ).count()
    page_data = Comment.query.filter(or_(
        Comment.content.ilike('%' + key + '%'),
        Comment.movie_id.ilike('%' + key + '%'),
        Comment.user_id.ilike('%' + key + '%')
    )
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)
    page_data.key = key
    return render_template('admin/comment_list_search.html', key=key, page_data=page_data, key_num=key_num)


# 删除评论
@admin.route('/comment/del/<int:id>/', methods=['GET'])
@admin_login_req
@admin_auth
def comment_delete(id=None):
    comment = Comment.query.filter_by(id=id).first_or_404()
    db.session.delete(comment)
    db.session.commit()
    flash('删除评论成功！', 'ok')
    return redirect(url_for('admin.comment_list', page=1))


# 电影收藏
@admin.route('/moviecol/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def moviecol_list(page=None):
    if page is None:
        page = 1
    page_data = Moviecol.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Moviecol.movie_id,
        User.id == Moviecol.user_id
    ).order_by(
        Moviecol.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/moviecol_list.html', page_data=page_data)


# 编辑电影收藏
@admin.route('/moviecol/edit/<int:id>/', methods=['GET'])
@admin_login_req
@admin_auth
def moviecol_edit(id=None):
    return render_template('admin/moviecol_edit.html')


# 删除电影收藏
@admin.route('/moviecol/del/<int:id>/', methods=['GET'])
@admin_login_req
@admin_auth
def moviecol_delete(id=None):
    moviecol = Moviecol.query.filter_by(id=id).first_or_404()
    db.session.delete(moviecol)
    db.session.commit()
    flash('删除评论成功！', 'ok')
    return redirect(url_for('admin.moviecol_list', page=1))


# 搜索
@admin.route('/moviecol/list/search/<int:page>/', methods=['GET', 'POST'])
@admin_login_req
# @admin_auth
def moviecol_list_search(page=None):
    if page is None:
        page = 1
    key = request.args.get('key', '')
    key_num = Moviecol.query.filter(or_(
        Moviecol.movie_id.ilike('%' + key + '%'),
    )
    ).count()
    page_data = Moviecol.query.filter(or_(
        Moviecol.movie_id.ilike('%' + key + '%'),
    )
    ).order_by(
        Moviecol.addtime.desc()
    ).paginate(page=page, per_page=10)
    page_data.key = key
    return render_template('admin/moviecol_list_search.html', key=key, page_data=page_data, key_num=key_num)


# 操作电影日志
@admin.route('/oplog/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def oplog_list(page=None):
    if page is None:
        page = 1
    page_data = Oplog.query.join(
        Admin
    ).filter(
        Admin.id == Oplog.user_id
    ).order_by(
        Oplog.sign_in_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/oplog_list.html', page_data=page_data)


# 管理员登入日志
@admin.route('/adminloginlog/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def adminloginlog_list(page=None):
    if page is None:
        page = 1
    page_data = Adminlog.query.join(
        Admin
    ).filter(
        Admin.id == Adminlog.user_id
    ).order_by(
        Adminlog.sign_in_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/adminloginlog_list.html', page_data=page_data)


# 会员登入日志
@admin.route('/userloginlog/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def userloginlog_list(page=None):
    if page is None:
        page = 1
    page_data = Userlog.query.join(
        User
    ).filter(
        User.id == Userlog.user_id
    ).order_by(
        Userlog.sign_in_time.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/userloginlog_list.html', page_data=page_data)


# 添加权限
@admin.route('/auth/add/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def auth_add():
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        auth = Auth(
            name=data['name'],
            url=data['url']
        )
        db.session.add(auth)
        db.session.commit()
        flash('添加权限成功！', 'ok')
    return render_template('admin/auth_add.html', form=form)


# 权限列表
@admin.route('/auth/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def auth_list(page=None):
    if page is None:
        page = 1
    page_data = Auth.query.order_by(
        Auth.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/auth_list.html', page_data=page_data)


# 删除权限
@admin.route('/auth/del/<int:id>/', methods=['GET'])
@admin_login_req
@admin_auth
def auth_delete(id=None):
    auth = Auth.query.filter_by(id=id).first_or_404()
    db.session.delete(auth)
    db.session.commit()
    flash('删除权限成功！', 'ok')
    return redirect(url_for('admin.auth_list', page=1))


# 编辑权限
@admin.route('/auth/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def auth_edit(id=None):
    form = AuthForm()
    auth = Auth.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        auth.title = data['name'],
        auth.info = data['url'],
        db.session.add(auth)
        db.session.commit()
        flash('修改权限成功！', 'ok')
    return render_template('admin/auth_edit.html', form=form, auth=auth)


# 添加角色
@admin.route('/role/add/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def role_add():
    form = RoleForm()
    if form.validate_on_submit():
        data = form.data
        role = Role(
            name=data['name'],
            auths=','.join(map(lambda v: str(v), data['auths']))
        )
        db.session.add(role)
        db.session.commit()
        flash('添加角色成功！', 'ok')
    return render_template('admin/role_add.html', form=form)


# 角色列表
@admin.route('/role/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def role_list(page=None):
    if page is None:
        page = 1
    page_data = Role.query.order_by(
        Role.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/role_list.html', page_data=page_data)


# 删除角色
@admin.route('/role/del/<int:id>/', methods=['GET'])
@admin_login_req
@admin_auth
def role_delete(id=None):
    role = Role.query.filter_by(id=id).first_or_404()
    db.session.delete(role)
    db.session.commit()
    flash('删除权限成功！', 'ok')
    return redirect(url_for('admin.role_list', page=1))


# 编辑角色
@admin.route('/role/edit/<int:id>/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def role_edit(id=None):
    form = RoleForm()
    role = Role.query.get_or_404(id)
    if request.method == 'GET':
        form.auths.data = list(map(lambda v: int(v), role.auths.split(',')))
    if form.validate_on_submit():
        data = form.data
        role.name = data['name'],
        role.auths = ','.join(map(lambda v: str(v), data['auths']))
        db.session.add(role)
        db.session.commit()
        flash('修改权限成功！', 'ok')
    return render_template('admin/role_edit.html', form=form, role=role)


# 添加管理员
@admin.route('/admin/add/', methods=['GET', 'POST'])
@admin_login_req
@admin_auth
def admin_add():
    form = AdminForm()
    from werkzeug.security import generate_password_hash
    if form.validate_on_submit():
        data = form.data
        admin = Admin(
            name=data['name'],
            password=generate_password_hash(data['password']),
            is_super=data['is_super'],
            role_id=data['role']
        )
        db.session.add(admin)
        db.session.commit()
        flash('添加管理员成功！', 'ok')
    return render_template('admin/admin_add.html', form=form)


# 管理员列表
@admin.route('/admin/list/<int:page>/', methods=['GET'])
@admin_login_req
@admin_auth
def admin_list(page=None):
    if page is None:
        page = 1
    page_data = Admin.query.join(
        Role
    ).filter(
        Role.id == Admin.role_id
    ).order_by(
        Admin.addtime.desc()
    ).paginate(page=page, per_page=10)
    return render_template('admin/admin_list.html', page_data=page_data)


# 权限错误
@admin.route('/admin/role/error/', methods=['GET'])
# @admin_login_req
def role_error():
    return render_template('admin/role_error.html')

# # 添加电影备份
# @admin.route('/movie/add/', methods=['GET', 'POST'])
# @admin_login_req
# @admin_auth
# def movie_add():
#     form = MovieForm()
#     if form.validate_on_submit():
#         data = form.data
#         file_url = secure_filename(form.url.data.filename)
#         file_logo = secure_filename(form.logo.data.filename)
#         if not os.path.exists(app.config['UP_DIR']):
#             os.makedirs(app.config['UP_DIR'])
#             os.chmod(app.config['UP_DIR'], 'rw')
#         url = change_filename(file_url)
#         logo = change_filename(file_logo)
#         form.url.data.save(app.config['UP_DIR'] + 'Movie/' + url)
#         form.logo.data.save(app.config['UP_DIR'] + 'Movie_Cover/' + logo)
#         movie = Movie(
#             title=data['title'],
#             url=url,
#             info=data['info'],
#             logo=logo,
#             star=int(data['star']),
#             playnum=0,
#             commentnum=0,
#             tag_id=data['tag_id'],
#             area=data['area'],
#             release_time=data['release_time'],
#             length=data['length'],
#             movie_head=60*int(data['movie_head']),
#             movie_tail=60*int(data['movie_tail']),
#         )
#         db.session.add(movie)
#         db.session.commit()
#         flash('添加电影成功', 'ok')
#         return redirect(url_for('admin.movie_add'))
#     return render_template('admin/movie_add.html', form=form)
