from flask.helpers import flash
from wsgi import app, db
from flask import render_template, redirect, url_for, request
from wsgi.models import Link, User
from flask_login import login_user, logout_user, current_user, login_required




@app.route('/')
def index():
    return render_template('index.html', title='Citly')




@app.route('/user-registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        repeatpassword = request.form['repeatpassword']

        if password != repeatpassword:
            flash('Password must be same!', 'warning')
            return redirect(url_for('registration'))
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Successfully register!', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html', title="Citly Registration")




@app.route('/user-login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember_me = request.form.get('remember_me')

        user = User.query.filter_by(username=username).first()
        if user is None or  not user.check_password(password):
            flash('Invalid username or password!', 'warning')
            return redirect(url_for('login'))
        
        login_user(user, remember=remember_me)
        flash('Successfully login', 'success')
        return redirect(url_for('add_link'))

    return render_template('login.html', title="Citly Login")



@app.route('/logout')
def logout():
    logout_user()
    flash('Successfully logout!', 'success')
    return redirect(url_for('index'))



@app.route('/add-link', methods=['GET', 'POST'])
@login_required
def add_link():
    if not current_user.is_authenticated:
        flash('Please login to access this page!', 'warning')
        return redirect(url_for('login'))

    links = Link.query.filter_by(user_id=current_user.id).order_by(Link.date_create.desc()).all()[0:6]
    if request.method == 'POST':
        original_url = request.form['original_url']
        add_url = Link(original_url=original_url, user_id=current_user.id)
        db.session.add(add_url)
        db.session.commit()
        return redirect(url_for('add_link'))

    return render_template('add_link_and_state.html', links=links, title='Citly | Url Shotener')



@app.route('/<short_url>')
def redirect_to_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()
    if link:
        link.visite = link.visite + 1
        db.session.commit()
        return redirect(link.original_url)



@app.route('/remove_url/<id>')
@login_required
def remove_url(id):
    if not current_user.is_authenticated:
        flash('Please login to access this page!', 'warning')
        return redirect(url_for('login'))

    link = Link.query.filter_by(id=id).first_or_404()
    if link:
        db.session.delete(link)
        db.session.commit()
        return redirect(request.referrer)



@app.route('/list-of-links')
@login_required
def list_of_links():
    if not current_user.is_authenticated:
        flash('Please login to access this page!', 'warning')
        return redirect(url_for('login'))
        
    links = Link.query.filter_by(user_id=current_user.id).all()
    return render_template('list_of_links.html', title='Citly Links', links=links)



@app.errorhandler(404)
def page_not_found(e):
    return '<h1>Page Not Found - Plaease Enter a Vaild Url', 404
        