from wsgi import app, db
from flask import render_template, redirect, url_for, request
from wsgi.models import Link


@app.route('/')
def index():
    return render_template('index.html', title='Citly')


@app.route('/add-link', methods=['GET', 'POST'])
def add_link():
    links = Link.query.all()[0:7]
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




# @app.errorhandler(404)
# def page_not_found(e):
#     return '<h1>Page Not Found - Plaease Enter a Vaild Url', 404
        