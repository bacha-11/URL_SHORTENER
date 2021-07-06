from wsgi import app, db
from flask import render_template, redirect, url_for, request
from wsgi.models import Link


@app.route('/')
def index():
    return render_template('index.html', title='Citly')


@app.route('/add-link', methods=['GET', 'POST'])
def add_link():
    links = Link.query.order_by(Link.date_create.desc()).all()[0:6]
    if request.method == 'POST':
        original_url = request.form['original_url']
        add_url = Link(original_url=original_url)
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
def remove_url(id):
    link = Link.query.filter_by(id=id).first_or_404()
    if link:
        db.session.delete(link)
        db.session.commit()
        return redirect(request.referrer)



@app.route('/list-of-links')
def list_of_links():
    links = Link.query.all()
    return render_template('list_of_links.html', title='Citly Links', links=links)



@app.errorhandler(404)
def page_not_found(e):
    return '<h1>Page Not Found - Plaease Enter a Vaild Url', 404
        