from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import RegisterForm, LoginForm, ReservarForm
from app.models import User, Sala
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse


@app.route("/reservas", methods=['GET', 'POST'])
@login_required
def reservas():
	salas = Sala.query.all()

	return render_template("reservas.html", salas=salas)


@app.route("/reservar", methods=['GET', 'POST'])
@login_required
def reservar():
	form = ReservarForm()
	if form.validate_on_submit():
		sala = Sala.query.filter_by(fecha=form.fecha.data, hora=form.hour.data).first()
		if sala is not None:
			flash("esta sala ya esta reservada en esa fecha")
			return render_template("index.html")
		print(form.fecha.data.strftime('%Y-%m-%d'))
		sala = Sala(fecha=form.fecha.data, hora=form.hour.data, numero=form.numero.data, author=current_user)
		db.session.add(sala)
		db.session.commit()
		print(
			"Reservada exitosamente la sala " + form.numero.data + "en la fecha: " + form.fecha.data.__repr__() + "a las: " + form.hour.data)
		flash("Reservada exitosamente la sala " + form.numero.data + "en la fecha: " + form.fecha.data.__repr__() + "a las: " + form.hour.data)
		return render_template("index.html")
	salas = current_user.salas_reservadas(current_user.get_id())
	return render_template("reservar.html", form=form, salas=salas)


@app.route('/')
@app.route('/index')

def index():
	return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash("username o password incorrectos")
			return redirect(url_for("login"))
		login_user(user)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != ' ':
			return redirect(url_for('index'))
	return render_template("login.html", title='Entrar', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegisterForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, name=form.name.data, email=form.email.data, telefono=form.telefono.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash("Ahora eres un usuario registrado")
		return redirect(url_for('login'))
	return render_template("register.html", title='Registrase', form=form)


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('index'))



