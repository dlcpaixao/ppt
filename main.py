from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizzaria.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração do upload de imagens
UPLOAD_FOLDER = 'static/img'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

# Função para verificar se a extensão do arquivo é permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Modelos
class Prato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Float, nullable=False)
    imagem = db.Column(db.String(120), nullable=True)

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cargo = db.Column(db.String(100), nullable=False)
    foto = db.Column(db.String(200), nullable=True)
    apresentacao = db.Column(db.Text, nullable=True)

# Rota para o menu de administração
@app.route('/admin')
def admin_menu():
    return render_template('adm/admin_menu.html')


# CRUD para Funcionários

# Rota para criar um novo funcionário (formulário)
@app.route('/funcionarios/novo', methods=['GET', 'POST'])
def criar_funcionario():
    if request.method == 'POST':
        nome = request.form['nome']
        cargo = request.form['cargo']
        apresentacao = request.form['apresentacao']
        
        # Processar o arquivo de foto
        foto = request.files.get('foto')
        if foto and allowed_file(foto.filename):
            filename = secure_filename(foto.filename)
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None
        
        novo_funcionario = Funcionario(nome=nome, cargo=cargo, apresentacao=apresentacao, foto=filename)
        db.session.add(novo_funcionario)
        db.session.commit()
        return redirect(url_for('listar_funcionarios'))
    return render_template('adm/create_funcionario.html')

# Rota para listar todos os funcionários
@app.route('/funcionarios', methods=['GET'])
def listar_funcionarios():
    funcionarios = Funcionario.query.all()
    return render_template('adm/list_funcionarios.html', funcionarios=funcionarios)

# Rota para editar um funcionário
@app.route('/funcionarios/<int:id>/edit', methods=['GET', 'POST'])
def editar_funcionario(id):
    funcionario = Funcionario.query.get_or_404(id)
    if request.method == 'POST':
        funcionario.nome = request.form['nome']
        funcionario.cargo = request.form['cargo']
        funcionario.apresentacao = request.form['apresentacao']
        
        foto = request.files.get('foto')
        if foto and allowed_file(foto.filename):
            filename = secure_filename(foto.filename)
            foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            funcionario.foto = filename
        
        db.session.commit()
        return redirect(url_for('listar_funcionarios'))
    return render_template('adm/update_funcionario.html', funcionario=funcionario)

# Rota para excluir um funcionário
@app.route('/funcionarios/<int:id>/delete', methods=['POST'])
def excluir_funcionario(id):
    funcionario = Funcionario.query.get_or_404(id)
    db.session.delete(funcionario)
    db.session.commit()
    return redirect(url_for('listar_funcionarios'))

# PRATOS

# Rota para criar um novo prato (formulário)
@app.route('/pratos/novo', methods=['GET', 'POST'])
def criar_prato():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = request.form['preco']
        
        # Processar o arquivo de imagem
        imagem = request.files.get('imagem')
        if imagem and allowed_file(imagem.filename):
            filename = secure_filename(imagem.filename)
            imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            filename = None
        
        novo_prato = Prato(nome=nome, descricao=descricao, preco=preco, imagem=filename)
        db.session.add(novo_prato)
        db.session.commit()
        return redirect(url_for('listar_pratos'))
    return render_template('adm/create_prato.html')

# Rota para listar todos os pratos
@app.route('/pratos', methods=['GET'])
def listar_pratos():
    pratos = Prato.query.all()
    return render_template('adm/list_pratos.html', pratos=pratos)

# Rota para atualizar um prato existente
@app.route('/pratos/<int:id>/edit', methods=['GET', 'POST'])
def atualizar_prato(id):
    prato = Prato.query.get_or_404(id)
    if request.method == 'POST':
        prato.nome = request.form['nome']
        prato.descricao = request.form['descricao']
        prato.preco = request.form['preco']
        
        imagem = request.files.get('imagem')
        if imagem and allowed_file(imagem.filename):
            filename = secure_filename(imagem.filename)
            imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            prato.imagem = filename
        
        db.session.commit()
        return redirect(url_for('listar_pratos'))
    return render_template('adm/update_prato.html', prato=prato)

# Rota para excluir um prato
@app.route('/pratos/<int:id>/delete', methods=['POST'])
def excluir_prato(id):
    prato = Prato.query.get_or_404(id)
    db.session.delete(prato)
    db.session.commit()
    return redirect(url_for('listar_pratos'))

# Inicializar o banco de dados
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


