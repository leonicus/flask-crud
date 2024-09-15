import logging

from flask import render_template, request, redirect
from app import app, db
from app.models import Entry

jedi = "of the jedi"

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S', filename="C:\\tmp\\flask.log", filemode="a")
@app.route('/')
@app.route('/index')
def index():
    # entries = [
    #     {
    #         'id' : 1,
    #         'title': 'test title 1',
    #         'description' : 'test desc 1',
    #         'status' : True
    #     },
    #     {
    #         'id': 2,
    #         'title': 'test title 2',
    #         'description': 'test desc 2',
    #         'status': False
    #     }
    # ]
    try:
        entries = Entry.query.all()
        return render_template('index.html', entries=entries)
    except Exception as e :
        logging.error(f'failed with {e}', stack_info=True)


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        form = request.form
        title = form.get('title')
        description = form.get('description')
        if not title or description:
            entry = Entry(title=title, description=description)
            db.session.add(entry)
            db.session.commit()
            return redirect('/')

    return "of the jedi"


@app.route('/update/<int:id>')
def updateRoute(id):
    if not id or id != 0:
        entry = Entry.query.get(id)
        if entry:
            return render_template('update.html', entry=entry)

    return "of the jedi"


@app.route('/update/<int:id>', methods=['POST', 'PUT'])
def update(id):
    if not id or id != 0:
        entry = Entry.query.get(id)
        if entry:
            form = request.form
            title = form.get('title')
            description = form.get('description')
            entry.title = title
            entry.description = description
            db.session.commit()
        else:
            return redirect('/', code=404)
        return redirect('/')

    return "of the jedi"


@app.route('/delete/<int:id>', methods=['GET', 'DELETE'])
def delete(id):
    if not id or id != 0:
        entry = Entry.query.get(id)
        if entry:
            db.session.delete(entry)
            db.session.commit()
        else:
            return redirect('/', code=404)
        return redirect('/')

    return "of the jedi"


@app.route('/turn/<int:id>')
def turn(id):
    if not id or id != 0:
        entry = Entry.query.get(id)
        if entry:
            entry.status = not entry.status
            db.session.commit()
        return redirect('/')

    return "of the jedi"


@app.route('/reset_db', methods=['DELETE'])
def reset_db():
    try:
        entries = Entry.query.all()
        for entry in entries:
            db.session.delete(entry)
        db.session.commit()
    except Exception as e:
        logging.error(e,stack_info=True)
    return redirect('/')


# @app.errorhandler(Exception)
# def error_page(e):
#     return "of the jedi"
