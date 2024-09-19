from flask import render_template, request, redirect, url_for, session, flash
from uninotes import app, db
from models import Notes, Users
@app.route('/')
def index():
    note_list = Notes.query.order_by(Notes.note_id)
    return render_template('list.html', title='Minhas Notas', notes=note_list)

@app.route('/new')
def new():
    if'logged_user' not in session or session['logged_user'] is None:
        return redirect(url_for('login', proxima=url_for('new')))
    return render_template('new.html', title='Nova Nota')

@app.route('/create', methods=['POST',])
def create():
    title = request.form['title']
    content = request.form['content']

    new_note = Notes(title=title, content=content)
    db.session.add(new_note)
    db.session.commit()

    cover = request.files['cover']
    upload_path = app.config['UPLOAD_PATH']
    cover.save(f'{upload_path}/cover{new_note.note_id}.jpg')

    return redirect(url_for('index'))

@app.route('/edit/<int:note_id>')
def edit(note_id):
    if'logged_user' not in session or session['logged_user'] is None:
        return redirect(url_for('login', proxima=url_for('edit', id=note_id)))
    note = Notes.query.filter_by(note_id=note_id).first()
    return render_template('edit.html', title='Editando Nota', note=note)

@app.route('/update', methods=['POST',])
def update():
    note = Notes.query.filter_by(note_id=request.form['note_id']).first()
    note.title = request.form['title']
    note.content = request.form['content']

    db.session.add(note)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete/<int:note_id>')
def delete(note_id):
    if'logged_user' not in session or session['logged_user'] is None:
        return redirect(url_for('login', proxima=url_for('delete', id=note_id)))

    Notes.query.filter_by(note_id=note_id).delete()
    db.session.commit()
    flash('Nota deletada com sucesso!')

    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/authenticate', methods=['POST',])
def authenticate():
    user = Users.query.filter_by(nickname=request.form['nickname']).first()
    if user:
        if request.form['user_password'] == user.user_password:
            session['logged_user'] = user.nickname
            flash(f'{user.nickname} Logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina or url_for('index'))
    else:
        flash('Usuário não encontrado ou senha incorreta')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['logged_user', None]
    flash('Logout bem sucedido!')
    return redirect(url_for('index'))