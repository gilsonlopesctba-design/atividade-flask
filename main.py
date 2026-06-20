from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///livros.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Livro(db.Model):
    id              = db.Column(db.Integer,     primary_key=True)
    titulo          = db.Column(db.String(200), nullable=False)
    autor           = db.Column(db.String(200), nullable=False)
    issn            = db.Column(db.String(20),  nullable=False)
    data_publicacao = db.Column(db.DateTime,    nullable=False)
    paginas         = db.Column(db.Integer,     nullable=False)

    def to_dict(self):
        return {
            'id':              self.id,
            'titulo':          self.titulo,
            'autor':           self.autor,
            'issn':            self.issn,
            'data_publicacao': self.data_publicacao.strftime('%Y-%m-%d'),
            'paginas':         self.paginas
        }

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    integrantes = [
        'Nome Completo 1',  # <- coloque o nome real aqui
        'Nome Completo 2'   # <- coloque o nome real aqui
    ]
    return jsonify({'integrantes': integrantes})

@app.route('/livros', methods=['GET', 'POST'])
def livros():
    if request.method == 'GET':
        todos = Livro.query.all()
        return jsonify([livro.to_dict() for livro in todos])

    dados = request.get_json()
    novo_livro = Livro(
        titulo          = dados['titulo'],
        autor           = dados['autor'],
        issn            = dados['issn'],
        data_publicacao = datetime.strptime(dados['data_publicacao'], '%Y-%m-%d'),
        paginas         = dados['paginas']
    )
    db.session.add(novo_livro)
    db.session.commit()
    return jsonify(novo_livro.to_dict()), 201