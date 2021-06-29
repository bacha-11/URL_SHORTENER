from wsgi import app


@app.route('/')
def index():
    return 'this is home page'