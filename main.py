from flask import Flask, render_template, redirect, abort, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from data import db_session
from data.cdel import CDEL
from data.users import User
from forms.cdel import CdelForm
from forms.user import RegisterForm, LoginForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/blogs.db")
    # app.register_blueprint(news_api.blueprint)
    app.run()


@app.route('/register',
           methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html',
                                   title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html',
                           title='Регистрация',
                           form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(CDEL).filter(
            (CDEL.user == current_user) | (CDEL.is_private == True))
    else:
        return redirect("/register")
    return render_template("index.html",
                           news=news)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login',
           methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user,
                       remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html',
                           title='Авторизация',
                           form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/cdel',
           methods=['GET', 'POST'])
@login_required
def add_news():
    form = CdelForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        cdel = CDEL()
        cdel.title = form.title.data
        cdel.content = form.content.data
        cdel.typef = form.typef.data
        cdel.is_private = form.is_private.data
        cdel.price = form.price.data
        cdel.price_type = form.price_type.data
        cdel.pr_fio = form.pr_fio.data
        cdel.po_fio = form.po_fio.data
        cdel.pr_data = form.pr_data.data
        cdel.po_data = form.po_data.data
        cdel.pr_cer = form.pr_cer.data
        cdel.pr_no = form.pr_no.data
        cdel.po_cer = form.po_cer.data
        cdel.po_no = form.po_no.data
        current_user.cdel.append(cdel)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('cdel.html',
                           title='Добавление сделки',
                           form=form)


@app.route('/cdel/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = CdelForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        cdel = db_sess.query(CDEL).filter(CDEL.id == id,
                                          CDEL.user == current_user
                                          ).first()
        if cdel:
            form.title.data = cdel.title
            form.content.data = cdel.content
            form.is_private.data = cdel.is_private
            form.typef.data = cdel.typef
            form.price.data = cdel.price
            form.price_type.data = cdel.price_type
            form.pr_fio.data = cdel.pr_fio
            form.po_fio.data = cdel.po_fio
            form.pr_data.data = cdel.pr_data
            form.po_data.data = cdel.po_data
            form.pr_cer.data = cdel.pr_cer
            form.pr_no.data = cdel.pr_no
            form.po_cer.data = cdel.po_cer
            form.po_no.data = cdel.po_no

        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        cdel = db_sess.query(CDEL).filter(CDEL.id == id,
                                          CDEL.user == current_user
                                          ).first()
        if cdel:
            cdel.title = form.title.data
            cdel.content = form.content.data
            cdel.is_private = form.is_private.data
            cdel.typef = form.typef.data
            cdel.price = form.price.data
            cdel.price_type = form.price_type.data
            cdel.pr_fio = form.pr_fio.data
            cdel.po_fio = form.po_fio.data
            cdel.pr_data = form.pr_data.data
            cdel.po_data = form.po_data.data
            cdel.pr_cer = form.pr_cer.data
            cdel.pr_no = form.pr_no.data
            cdel.po_cer = form.po_cer.data
            cdel.po_no = form.po_no.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('cdel.html',
                           title='Редактирование сделки',
                           form=form
                           )


@app.route('/cdel_view/<int:id>', methods=['GET', 'POST'])
@login_required
def view_news(id):
    form = CdelForm()
    db_sess = db_session.create_session()
    cdel = db_sess.query(CDEL).filter(CDEL.id == id,
                                          CDEL.user == current_user
                                          ).first()
    form.title.data = cdel.title
    form.content.data = cdel.content
    form.is_private.data = cdel.is_private
    form.typef.data = cdel.typef
    form.price.data = cdel.price
    form.price_type.data = cdel.price_type
    form.pr_fio.data = cdel.pr_fio
    form.po_fio.data = cdel.po_fio
    form.pr_data.data = cdel.pr_data
    form.po_data.data = cdel.po_data
    form.pr_cer.data = cdel.pr_cer
    form.pr_no.data = cdel.pr_no
    form.po_cer.data = cdel.po_cer
    form.po_no.data = cdel.po_no
    form.title.render_kw = {'disabled': 'disabled'}
    form.content.render_kw = {'disabled': 'disabled'}
    form.is_private.render_kw = {'disabled': 'disabled'}
    form.typef.render_kw = {'disabled': 'disabled'}
    form.price.render_kw = {'disabled': 'disabled'}
    form.price_type.render_kw = {'disabled': 'disabled'}
    form.pr_fio.render_kw = {'disabled': 'disabled'}
    form.po_fio.render_kw = {'disabled': 'disabled'}
    form.pr_data.render_kw = {'disabled': 'disabled'}
    form.po_data.render_kw = {'disabled': 'disabled'}
    form.pr_cer.render_kw = {'disabled': 'disabled'}
    form.pr_no.render_kw = {'disabled': 'disabled'}
    form.po_cer.render_kw = {'disabled': 'disabled'}
    form.po_no.render_kw = {'disabled': 'disabled'}
    if form.validate_on_submit():
            return redirect('/')
    return render_template('cdel.html',
                           title='Редактирование сделки',
                           form=form
                           )


@app.route('/cdel_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def news_delete(id):
    db_sess = db_session.create_session()
    cdel = db_sess.query(CDEL).filter(CDEL.id == id,
                                      CDEL.user == current_user
                                      ).first()
    if cdel:
        db_sess.delete(cdel)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


if __name__ == '__main__':
    main()
