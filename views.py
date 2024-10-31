from flask import render_template, request, redirect, url_for, session, flash, jsonify

from uninotes import app, db
from models import Notes, Users
from login_form import LoginForm
from flask_bcrypt import check_password_hash


# Página principal que exibe as notas do usuário logado
@app.route('/')
def index():
    # Verificação de autenticação
    if 'logged_user' not in session or session['logged_user'] is None:
        return redirect(url_for('login', proxima=url_for('index')))

    # Recuperar usuário logado
    user = Users.query.filter_by(user_id=session['logged_user']).first()

    if user is None:
        flash("Usuário não encontrado")
        return redirect(url_for('login'))

    # Obter as notas do usuário logado
    note_list = Notes.query.filter_by(user_id=user.user_id).order_by(Notes.timestamp).all()

    return render_template('app.html', notes=note_list, user=user)


# Rota para criar uma nova nota
@app.route('/create_note', methods=['POST'])
def create_note():
    if 'logged_user' not in session:
        return jsonify({'success': False, 'error': 'Usuário não autenticado'}), 403

    user = Users.query.filter_by(user_id=session['logged_user']).first()

    if user is None:
        return jsonify({'success': False, 'error': 'Usuário não encontrado'}), 404

    content = request.form.get('content')
    color = request.form.get('color', '#ffeb3b')  # Cor padrão: amarelo

    if content:
        new_note = Notes(content=content, color=color, user_id=user.user_id)
        db.session.add(new_note)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Nota criada com sucesso'}), 201

    return jsonify({'success': False, 'error': 'Conteúdo da nota não pode ser vazio'}), 400


# Rota para editar uma nota existente
@app.route('/edit_note/<int:note_id>', methods=['POST'])
def edit_note(note_id):
    if 'logged_user' not in session:
        return jsonify({'success': False, 'error': 'Usuário não autenticado'}), 403

    note = Notes.query.filter_by(note_id=note_id, user_id=session['logged_user']).first()

    if note:
        new_content = request.form.get('content')
        if new_content:
            note.content = new_content
            db.session.commit()
            return jsonify({'success': True, 'message': 'Nota atualizada com sucesso'}), 200
        return jsonify({'success': False, 'error': 'Conteúdo da nota não pode ser vazio'}), 400
    return jsonify({'success': False, 'error': 'Nota não encontrada'}), 404


# Rota para deletar uma nota
@app.route('/delete_note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    if 'logged_user' not in session:
        return jsonify({'success': False, 'error': 'Usuário não autenticado'}), 403

    note = Notes.query.filter_by(note_id=note_id, user_id=session['logged_user']).first()

    if note:
        db.session.delete(note)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Nota excluída com sucesso'}), 200
    return jsonify({'success': False, 'error': 'Nota não encontrada'}), 404


# Página de login
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    form = LoginForm()
    return render_template('login.html', proxima=proxima, form=form)


# Autenticação de usuário
@app.route('/authenticate', methods=['POST'])
def authenticate():
    form = LoginForm(request.form)
    # Verificar se o usuário existe
    if form.validate_on_submit():
        user = Users.query.filter_by(user_id=form.user_id.data).first()

        if user and check_password_hash(user.user_password, form.password.data):
            # Armazena o usuário na sessão
            session['logged_user'] = user.user_id
            flash(f'{user.nickname} logado com sucesso!')
            proxima_pagina = request.form.get('proxima')
            return redirect(proxima_pagina or url_for('index'))
        else:
            flash('Usuário não encontrado ou senha incorreta')
            return redirect(url_for('login'))

    flash('Erro ao realizar login. Tente novamente')
    return redirect(url_for('login'))
# Rota de logout
@app.route('/logout', methods=['POST'])
def logout():
    if request.method == 'POST':
        session.pop('logged_user', None)
        flash('Logout realizado com sucesso!')
        return redirect(url_for('login'))
    return redirect(url_for('login'))