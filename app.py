from flask import Flask, render_template, redirect, request
import config
from data import db_session, invites_api
from data.users import User
from data.posts import Post
from data.scores import Score
from data.comments import Comment
from forms.login import LoginForm
from forms.register import RegisterForm
from forms.post import PostForm
from forms.comment import CommentForm
from forms.image import ImageForm
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret_key
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    db_sess.close()
    return db_sess.query(User).get(user_id)


def add_post(db_sess, user, content):
	post = Post(rating=0, content=content)
	user.posts.append(post)


def get_rating(id):
	db_sess = db_session.create_session()
	plus = len(db_sess.query(Score).filter(Score.post_id == id, Score.value == 1).all())
	minus = len(db_sess.query(Score).filter(Score.post_id == id, Score.value == -1).all())
	db_sess.close()
	return (plus - minus)


@app.route('/me')
def me():
	return redirect(f'/profile/{current_user.id}')

@app.route('/search')
def search():
	query = request.args['query']
	db_sess = db_session.create_session()
	posts = db_sess.query(Post).filter(Post.content.like(f'%{query}%')).all()[::-1]
	for post in posts:
		try:
			score = db_sess.query(Score).filter(Score.user_id == current_user.id, Score.post_id == post.id).first()
			post.score = score.value if score else 0
		except AttributeError:
			post.score = 0
		post.rating = get_rating(post.id)

	db_sess.close()
	return render_template('index.html', title='Главная', posts=posts, search=query)
@app.route('/post/delete/<id>')
@login_required
def delete_post(id):
	db_sess = db_session.create_session()
	post = db_sess.query(Post).filter(Post.id == id).first()
	scores = db_sess.query(Score).filter(Score.post_id == post.id).all()
	comments = db_sess.query(Comment).filter(Comment.post_id == post.id).all()
	if post.creator_id == current_user.id:
		db_sess.delete(post)
		for score in scores:
			db_sess.delete(score)
		for comment in comments:
			db_sess.delete(comment)
		db_sess.commit()
	db_sess.close()
	return redirect('/')

@app.route('/profile/<id>', methods=['GET', 'POST'])
def profile(id):
	form = ImageForm()
	if form.validate_on_submit():
		form.image.data.save(f'static/img/avatars/{current_user.id}.png')
	db_sess = db_session.create_session()
	data = db_sess.query(User).filter(User.id == id).first()
	data.created_date = str(data.created_date).split()[0]
	db_sess.close()
	return render_template('profile.html', data=data, form=form) 


@app.route('/post/<id>', methods=['GET', 'POST'])
def post(id):
	db_sess = db_session.create_session()
	form = CommentForm()
	data = db_sess.query(Post).filter(Post.id == id).first()
	data.rating = get_rating(data.id)
	try:
		score = db_sess.query(Score).filter(Score.user_id == current_user.id, Score.post_id == data.id).first()
		data.score = score.value if score else 0
	except AttributeError:
		data.score = 0
	if form.validate_on_submit():
		comment = Comment(content=form.content.data, user_id=current_user.id)
		data.comments.append(comment)
		db_sess.commit()
		db_sess.close()
		return redirect(f'/post/{id}')
	for comment in data.comments:
		comment.username = db_sess.query(User).filter(User.id == comment.user_id).first().username
	db_sess.close()
	return render_template('post.html', title=f'Пост #{data.id}', data=data, form=form)

@app.route('/api/minus/<id>')
def minus_rate(id):
	db_sess = db_session.create_session()
	query = db_sess.query(Score).filter(Score.user_id == current_user.id, Score.post_id == id, Score.value == -1)
	query_plus = db_sess.query(Score).filter(Score.user_id == current_user.id, Score.post_id == id, Score.value == 1)
	if query.first():
		colored = False
		db_sess.delete(query.first())
	elif query_plus.first():
		colored = False
		db_sess.delete(query_plus.first())
	else:
		colored = True
		score = Score(value=-1, post_id=id)
		user = db_sess.query(User).filter(User.id == current_user.id).first()
		user.scores.append(score)
	db_sess.commit()
	value = get_rating(id)
	db_sess.close()
	return {'user': current_user.username, 'colored': colored, 'new_value': value}


@app.route('/api/plus/<id>')
def plus_rate(id):
	db_sess = db_session.create_session()
	query = db_sess.query(Score).filter(Score.user_id == current_user.id, Score.post_id == id, Score.value == 1)
	query_minus = db_sess.query(Score).filter(Score.user_id == current_user.id, Score.post_id == id, Score.value == -1)
	if query.first():
		colored = False
		db_sess.delete(query.first())
	elif query_minus.first():
		colored = False
		db_sess.delete(query_minus.first())
	else:
		colored = True
		score = Score(value=1, post_id=id)
		user = db_sess.query(User).filter(User.id == current_user.id).first()
		user.scores.append(score)
	db_sess.commit()
	value = get_rating(id)
	db_sess.close()
	return {'user': current_user.username, 'colored': colored, 'new_value': value}

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
	form = PostForm()
	if form.validate_on_submit():
		db_sess = db_session.create_session()
		user = db_sess.query(User).filter(User.id == current_user.id).first()
		post = Post(content=form.content.data)
		user.posts.append(post)
		db_sess.commit()
		db_sess.close()
		return redirect('/')
	return render_template('create_post.html', title='Создать пост', form=form)


@app.route('/')
def index():
	db_sess = db_session.create_session()
	posts = db_sess.query(Post).all()[::-1]
	for post in posts:
		post.creator
		try:
			score = db_sess.query(Score).filter(Score.user_id == current_user.id, Score.post_id == post.id).first()
			post.score = score.value if score else 0
		except AttributeError:
			post.score = 0
		post.rating = get_rating(post.id)
	db_sess.close()
	return render_template('index.html', title='Главная', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		db_sess = db_session.create_session()
		user = db_sess.query(User).filter(User.username == form.username.data).first()
		db_sess.close()
		if user and user.check_password(form.password.data):
			login_user(user, remember=True)
			return redirect('/')
		return render_template('login.html', title='Войти', form=form, message="Неправильное имя пользователя или пароль")
	return render_template('login.html', title='Войти', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		if form.password.data != form.password_again.data:
			db_sess.close()
			return render_template('register.html', title='Регистрация', form=form, message='Пароли не совпадают')
		db_sess = db_session.create_session()
		if db_sess.query(User).filter(User.username == form.username.data).first():
			db_sess.close()
			return render_template('register.html', title='Регистрация', form=form, message='Имя пользователя занято')
		user = User(
			username=form.username.data
		)
		user.set_password(form.password.data)
		db_sess.add(user)
		db_sess.commit()
		db_sess.close()
		with open('static/img/avatar.png', 'rb') as input_file:
			with open(f'static/img/avatars/{user.id}.png', 'wb') as output_file:
				output_file.write(input_file.read())
		return redirect('/login')
	return render_template('register.html', title='Регистрация', form=form)



def main():
	db_session.global_init("db/server.db")
	# app.register_blueprint(invites_api.blueprint)
	app.run(debug=config.debug, host=config.host, port=config.port)


if __name__ == '__main__':
	main()