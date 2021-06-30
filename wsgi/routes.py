from wsgi import app, db
from flask import render_template, redirect, url_for, request
from wsgi.models import Link


@app.route('/', methods=['GET', 'POST'])
def index():

    links = Link.query.all()
    if request.method == 'POST':
        original_url = request.form['original_url']
        add_url = Link(original_url=original_url)
        db.session.add(add_url)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('index.html', links=links)


@app.route('/<short_url>')
def redirect_to_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first()
    if link:
        link.visite = link.visite + 1
        db.session.commit()
        return redirect(link.original_url)
        