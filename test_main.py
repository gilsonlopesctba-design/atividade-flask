import pytest
import json
from main import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    with app.app_context():
        db.create_all()

    yield app.test_client()

    with app.app_context():
        db.drop_all()

# --- Testes GET / ---

def test_home_retorna_status_200(client):
    resposta = client.get('/')
    assert resposta.status_code == 200

def test_home_retorna_json(client):
    resposta = client.get('/')
    assert resposta.content_type == 'application/json'

def test_home_contem_integrantes(client):
    resposta = client.get('/')
    dados = json.loads(resposta.data)
    assert 'integrantes' in dados
    assert len(dados['integrantes']) > 0

# --- Testes GET /livros ---

def test_livros_get_status_200(client):
    resposta = client.get('/livros')
    assert resposta.status_code == 200

def test_livros_get_lista_vazia(client):
    resposta = client.get('/livros')
    dados = json.loads(resposta.data)
    assert dados == []

def test_livros_get_retorna_json(client):
    resposta = client.get('/livros')
    assert resposta.content_type == 'application/json'

# --- Testes POST /livros ---

def test_livros_post_status_201(client):
    livro = {
        'titulo': 'Python para Iniciantes',
        'autor': 'João Silva',
        'issn': '1234-5678',
        'data_publicacao': '2023-01-15',
        'paginas': 300
    }
    resposta = client.post('/livros', json=livro)
    assert resposta.status_code == 201

def test_livros_post_dados_corretos(client):
    livro = {
        'titulo': 'Flask na Prática',
        'autor': 'Maria Santos',
        'issn': '8765-4321',
        'data_publicacao': '2023-06-20',
        'paginas': 150
    }
    resposta = client.post('/livros', json=livro)
    dados = json.loads(resposta.data)
    assert dados['titulo'] == 'Flask na Prática'
    assert dados['paginas'] == 150

def test_livros_post_aparece_no_get(client):
    livro = {
        'titulo': 'DevOps para Todos',
        'autor': 'Carlos Lima',
        'issn': '1111-2222',
        'data_publicacao': '2024-01-01',
        'paginas': 200
    }
    client.post('/livros', json=livro)
    resposta = client.get('/livros')
    dados = json.loads(resposta.data)
    assert len(dados) == 1
    assert dados[0]['titulo'] == 'DevOps para Todos'