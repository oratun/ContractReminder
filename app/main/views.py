from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response, session
from flask_login import login_required, current_user
from . import main
from .forms import PostForm, SearchForm, AttachForm
from .. import db
from ..models import Permission, Role, User, Post, Depart
from ..decorators import admin_required, permission_required
from werkzeug import secure_filename
import xlrd

@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = SearchForm()
    user_id = current_user.get_id()
    form.depart_id.choices = [(0,'')] + [(d.id, d.depart_name) for d in Depart.query.all()]
    if form.validate_on_submit():
        title = form.title.data
        summary = form.summary.data
        note = form.note.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        remind_date = form.remind_date.data
        depart_id = form.depart_id.data
        query = Post.query.filter(Post.author_id==user_id)
        if current_user.can(Permission.SEE_ALL):
            query = Post.query
        if title:
            query = query.filter(Post.title.like('%'+title+'%'))
        if summary:
            query = query.filter(Post.summary.like('%'+summary+'%'))
        if note:
            query = query.filter(Post.note.like('%'+note+'%'))
        if start_date:
            query = query.filter(Post.start_date==start_date)
        if end_date:
            query = query.filter(Post.end_date==end_date)
        if remind_date:
            query = query.filter(Post.remind_date==remind_date)
        if depart_id != 0:
            query = query.filter(Post.depart_id==depart_id)
        query = query.order_by(Post.end_date.desc())
        page = request.args.get('page', 1, type=int)
    # show_followed = False
    # query = Post.query.filter_by(author_id=user_id).order_by(Post.timestamp.desc())
        pagination = query.paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        posts = pagination.items
        return render_template('index.html', posts=posts, form=form,
                           pagination=pagination)
    # return redirect(url_for('main.index'))
    return render_template('index.html', form=form)



@main.route('/all', methods=['GET', 'POST'])
@login_required
def all():
    page = request.args.get('page', 1, type=int)
    # show_followed = False
    user_id = current_user.get_id()
    query = Post.query.filter_by(author_id=user_id).order_by(Post.timestamp.desc())
    if current_user.can(Permission.SEE_ALL):
        query = Post.query
    pagination = query.paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('all.html', posts=posts, pagination=pagination)


@main.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    form.depart_id.choices = [(0,'')] + [(d.id, d.depart_name)
        for d in Depart.query.all()]
    # form.depart_id.default = User.query.filter_by(id=session['user_id']).first().depart_id
    if current_user.can(Permission.WRITE) and form.validate_on_submit():
        post = Post(title=form.title.data, summary=form.summary.data,
                    note=form.note.data, start_date=form.start_date.data,
                    end_date=form.end_date.data, remind_date=form.remind_date.data,
                    author_id=session['user_id'],
                    depart_id=form.depart_id.data)
        db.session.add(post)
        flash('合同信息添加成功')
        return redirect(url_for('.new_post'))
    return render_template('new_post.html', form=form)

@main.route('/about', methods=['GET'])
@login_required
def about():
    return render_template('about.html')


@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])#, form=form)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.summary=form.summary.data
        post.note=form.note.data
        post.start_date=form.start_date.data
        post.end_date=form.end_date.data
        post.remind_date=form.remind_date.data
        post.author_id=session['user_id']
        post.depart_id=form.depart_id.data
        db.session.add(post)
        flash('合同信息更新成功')
        return redirect(url_for('.post', id=post.id))
    form.title.data = post.title
    form.summary.data = post.summary
    form.note.data = post.note
    form.start_date.data = post.start_date
    form.end_date.data = post.end_date
    form.remind_date.data = post.remind_date
    form.depart_id.choices = [(d.id, d.depart_name) for d in Depart.query.all()]
    return render_template('edit_post.html', form=form)


@main.route('/upload', methods=['GET', 'POSt'])
@login_required
def upload():
    form = AttachForm()
    if form.validate_on_submit():
        book = xlrd.open_workbook(form.attach.data)
        sh = book.sheet_by_index(0)
        total = []
        for row in range(1, sh.nrows):
            values = []
            for col in range(sh.ncols):
                values.append(sh.cell(row, col).value)
            totals.append(values)
        # filename = secure_filename(form.attach.data.filename)
        # form.attach.data.save('uploads/'+filename)
        flash('上传成功')
        return redirect(url_for('.upload'))
    return render_template('upload.html', form=form)



# @main.route('/user/<username>')
# @login_required
# def user(username):
#     user = User.query.filter_by(username=username).first_or_404()
#     page = request.args.get('page', 1, type=int)
#     pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
#         page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
#         error_out=False)
#     posts = pagination.items
#     return render_template('user.html', user=user, posts=posts,
#                            pagination=pagination)


# @main.route('/edit-profile', methods=['GET', 'POST'])
# @login_required
# def edit_profile():
#     form = EditProfileForm()
#     if form.validate_on_submit():
#         current_user.name = form.name.data
#         current_user.location = form.location.data
#         current_user.about_me = form.about_me.data
#         db.session.add(current_user)
#         flash('Your profile has been updated.')
#         return redirect(url_for('.user', username=current_user.username))
#     form.name.data = current_user.name
#     form.location.data = current_user.location
#     form.about_me.data = current_user.about_me
#     return render_template('edit_profile.html', form=form)


# @main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def edit_profile_admin(id):
#     user = User.query.get_or_404(id)
#     form = EditProfileAdminForm(user=user)
#     if form.validate_on_submit():
#         user.email = form.email.data
#         user.username = form.username.data
#         user.confirmed = form.confirmed.data
#         user.role = Role.query.get(form.role.data)
#         user.name = form.name.data
#         user.location = form.location.data
#         user.about_me = form.about_me.data
#         db.session.add(user)
#         flash('The profile has been updated.')
#         return redirect(url_for('.user', username=user.username))
#     form.email.data = user.email
#     form.username.data = user.username
#     form.confirmed.data = user.confirmed
#     form.role.data = user.role_id
#     form.name.data = user.name
#     form.location.data = user.location
#     form.about_me.data = user.about_me
#     return render_template('edit_profile.html', form=form, user=user)

# @main.route('/follow/<username>')
# @login_required
# @permission_required(Permission.FOLLOW)
# def follow(username):
#     user = User.query.filter_by(username=username).first()
#     if user is None:
#         flash('Invalid user.')
#         return redirect(url_for('.index'))
#     if current_user.is_following(user):
#         flash('You are already following this user.')
#         return redirect(url_for('.user', username=username))
#     current_user.follow(user)
#     flash('You are now following %s.' % username)
#     return redirect(url_for('.user', username=username))


# @main.route('/unfollow/<username>')
# @login_required
# @permission_required(Permission.FOLLOW)
# def unfollow(username):
#     user = User.query.filter_by(username=username).first()
#     if user is None:
#         flash('Invalid user.')
#         return redirect(url_for('.index'))
#     if not current_user.is_following(user):
#         flash('You are not following this user.')
#         return redirect(url_for('.user', username=username))
#     current_user.unfollow(user)
#     flash('You are not following %s anymore.' % username)
#     return redirect(url_for('.user', username=username))


# @main.route('/followers/<username>')
# def followers(username):
#     user = User.query.filter_by(username=username).first()
#     if user is None:
#         flash('Invalid user.')
#         return redirect(url_for('.index'))
#     page = request.args.get('page', 1, type=int)
#     pagination = user.followers.paginate(
#         page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
#         error_out=False)
#     follows = [{'user': item.follower, 'timestamp': item.timestamp}
#                for item in pagination.items]
#     return render_template('followers.html', user=user, title="Followers of",
#                            endpoint='.followers', pagination=pagination,
#                            follows=follows)


# @main.route('/followed-by/<username>')
# def followed_by(username):
#     user = User.query.filter_by(username=username).first()
#     if user is None:
#         flash('Invalid user.')
#         return redirect(url_for('.index'))
#     page = request.args.get('page', 1, type=int)
#     pagination = user.followed.paginate(
#         page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
#         error_out=False)
#     follows = [{'user': item.followed, 'timestamp': item.timestamp}
#                for item in pagination.items]
#     return render_template('followers.html', user=user, title="Followed by",
#                            endpoint='.followed_by', pagination=pagination,
#                            follows=follows)


# @main.route('/all')
# @login_required
# def show_all():
#     resp = make_response(redirect(url_for('.index')))
#     resp.set_cookie('show_followed', '', max_age=30*24*60*60)
#     return resp


# @main.route('/followed')
# @login_required
# def show_followed():
#     resp = make_response(redirect(url_for('.index')))
#     resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
#     return resp


# @main.route('/moderate')
# @login_required
# @permission_required(Permission.MODERATE_COMMENTS)
# def moderate():
#     page = request.args.get('page', 1, type=int)
#     pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
#         page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
#         error_out=False)
#     comments = pagination.items
#     return render_template('moderate.html', comments=comments,
#                            pagination=pagination, page=page)


# @main.route('/moderate/enable/<int:id>')
# @login_required
# @permission_required(Permission.MODERATE_COMMENTS)
# def moderate_enable(id):
#     comment = Comment.query.get_or_404(id)
#     comment.disabled = False
#     db.session.add(comment)
#     return redirect(url_for('.moderate',
#                             page=request.args.get('page', 1, type=int)))


# @main.route('/moderate/disable/<int:id>')
# @login_required
# @permission_required(Permission.MODERATE_COMMENTS)
# def moderate_disable(id):
#     comment = Comment.query.get_or_404(id)
#     comment.disabled = True
#     db.session.add(comment)
#     return redirect(url_for('.moderate',
#                             page=request.args.get('page', 1, type=int)))
